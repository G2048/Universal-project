import logging

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlmodel import select

from app.api.dependencies.db import Session, get_db_connection
from app.api.services import PasswordHasher
from app.core.database.models import Users

router = APIRouter(prefix="/users", tags=["Users"])

logger = logging.getLogger("app.api.v1.routers.users")


@router.post("/")
def create_user(user: Users, session: Session = Depends(get_db_connection)):
    logger.debug(f"{user=}")
    user.password = PasswordHasher.hash_password(user.password)
    try:
        session.add(user)
        session.commit()
        session.refresh(user)
    except Exception as e:
        logger.error(e)
        session.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error")
    return JSONResponse(
        status_code=201,
        content={"id": f"{user.id}"},
    )


@router.get("/")
def list_users(session: Session = Depends(get_db_connection)):
    # Непонятна логика для Users.user_lock
    try:
        users = session.exec(select(Users)).fetchall()
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
    return users


@router.get("/{user_id}")
def get_user(user_id: int, session: Session = Depends(get_db_connection)) -> Users:
    # Непонятна логика для Users.user_lock
    logger.info(f"Getting user with id: {user_id}")
    statement = select(Users).where(Users.id == user_id)
    user = session.exec(statement).first()
    if not user:
        raise HTTPException(
            status_code=404, detail=f"User with id: {user_id} not found"
        )
    return user


@router.delete("/{user_id}")
def delete_user(user_id: int, session: Session = Depends(get_db_connection)):
    logger.info(f"Deleting user with id: {user_id}")
    statement = select(Users).where(Users.id == user_id)
    user = session.exec(statement).first()
    if user:
        session.delete(user)
        session.commit()
    else:
        raise HTTPException(
            status_code=404, detail=f"User with id: {user_id} not found"
        )
    return JSONResponse(
        status_code=201,
        content={"id": f"{user.id}"},
    )
