import logging

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlmodel import select

from app.api.dependencies.db import Session, get_db_connection
from app.core.database.models import Companies, UserGroups, Users

router = APIRouter(prefix="/groups", tags=["Groups"])

logger = logging.getLogger("app.api.v1.routers.groups")


@router.post("/")
def create_user_group(group: UserGroups, session: Session = Depends(get_db_connection)):
    logger.info(f"{group=}")
    company_exists = session.exec(
        select(Companies).where(Companies.id == group.company_id)
    ).first()
    if not company_exists:
        raise HTTPException(
            status_code=404, detail=f"Company with id: {group.company_id} not found"
        )
    try:
        session.add(group)
        session.commit()
        session.refresh(group)
    except Exception as e:
        logger.error(e)
        session.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error")
    return JSONResponse(
        status_code=201,
        content={"id": f"{group.id}"},
    )


@router.get("/")
def list_user_groups(session: Session = Depends(get_db_connection)) -> list[UserGroups]:
    return session.exec(select(UserGroups)).fetchall()


@router.get("/{user_id}")
def list_my_groups(
    user_id: int, session: Session = Depends(get_db_connection)
) -> list[UserGroups]:
    return session.exec(
        select(UserGroups).join(Users).where(Users.id == user_id)
    ).fetchall()


@router.put("/{user_id}")
def add_user_to_group(
    user_id: int, group_id: int, session: Session = Depends(get_db_connection)
):
    logger.info(f"Adding user with id: {user_id} to group with id: {group_id}")

    statement = select(UserGroups).where(UserGroups.id == group_id)
    group = session.exec(statement).first()
    if not group:
        raise HTTPException(
            status_code=404, detail=f"Group with id: {group_id} not found"
        )
    if group.company_id is None:
        raise HTTPException(
            status_code=400, detail="Group does not belong to a company"
        )
    # statement = select(UserGroups).where(
    # (UserGroups.company_id == group.company_id)
    # & (UserGroups.group_name == group.group_name)
    # & (UserGroups.id != group_id)
    # )
    # other_group = session.exec(statement).first()
    # if other_group:
    #     raise HTTPException(
    #         status_code=409, detail=f"User already in group: {other_group.group_name}"
    #     )

    user = session.exec(select(Users).where(Users.id == user_id)).first()
    logger.info(f"{user=}")
    if not user:
        raise HTTPException(
            status_code=404, detail=f"User with id: {user_id} not found"
        )
    user.group_id = group_id
    try:
        session.add(user)
        session.commit()
    except Exception as e:
        logger.error(e)
        session.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error")
    return JSONResponse(
        status_code=201,
        content={"id": f"{group.id}"},
    )
