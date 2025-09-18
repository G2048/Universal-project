import logging

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse, Response
from sqlmodel import select

from app.api.dependencies.db import Session, get_db_connection
from app.core.database.models import Settings, SettingsDict

router = APIRouter(prefix="/settings", tags=["Settings"])

logger = logging.getLogger("app.api.v1.routers.settings")


@router.post("/")
def add_setting(setting: Settings, session: Session = Depends(get_db_connection)):
    logger.debug(f"{setting=}")
    try:
        session.add(setting)
        session.commit()
        session.refresh(setting)
    except Exception as e:
        logger.error(e)
        session.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error")
    return JSONResponse(
        status_code=201,
        content={"id": f"{setting.id}"},
    )


@router.patch("/{setting_id}")
def update_setting(setting: Settings, session: Session = Depends(get_db_connection)):
    logger.debug(f"{setting=}")
    if setting.id is None:
        raise HTTPException(status_code=400, detail="Setting id is required to update")

    setting_exist = session.exec(
        select(Settings).where(Settings.id == setting.id)
    ).first()
    if not setting_exist:
        raise HTTPException(
            status_code=404, detail=f"Settings with id: {setting.id} not found"
        )
    try:
        setting_exist.code = setting.code
        setting_exist.name = setting.name
        session.add(setting_exist)
        session.commit()
        session.refresh(setting_exist)
    except Exception as e:
        logger.error(e)
        session.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error")
    return JSONResponse(
        status_code=202,
        content={"id": f"{setting_exist.id}"},
    )


@router.get("/dict")
def list_settings_dict(
    session: Session = Depends(get_db_connection),
) -> list[SettingsDict]:
    return session.exec(select(SettingsDict)).fetchall()


@router.get("/")
def list_settings(
    session: Session = Depends(get_db_connection),
) -> list[Settings]:
    return session.exec(select(Settings)).fetchall()


@router.get("/{settings_id}")
def get_settings(
    settings_id: int, session: Session = Depends(get_db_connection)
) -> Settings:
    settings = session.exec(select(Settings).where(Settings.id == settings_id)).first()
    if not settings:
        raise HTTPException(
            status_code=404, detail=f"Settings with id: {settings_id} not found"
        )
    return settings


@router.delete("/{setting_id}")
def delete_settings(
    setting_id: int,
    session: Session = Depends(get_db_connection),
):
    logger.debug(f"{setting_id=}")

    setting_exist = session.exec(
        select(Settings).where(Settings.id == setting_id)
    ).first()
    if not setting_exist:
        raise HTTPException(
            status_code=404, detail=f"Settings with id: {setting_id} not found"
        )
    session.delete(setting_exist)
    session.commit()
    return Response(status_code=204)
