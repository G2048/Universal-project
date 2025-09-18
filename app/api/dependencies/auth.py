import logging

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session, select

from app.api.services import (
    JWT,
    ExpiredSignatureError,
    InvalidTokenError,
    JwtPayload,
)
from app.core.database.models import Users

from .db import get_db_connection

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/")
logger = logging.getLogger("app.api.dependencies.auth")


def validate_token(token: str = Depends(oauth2_scheme)) -> JwtPayload:
    logger.debug(f"Token: {token=}")
    payload = JWT.payload(token)
    error = False
    if token:
        try:
            JWT.validate(token)
        except ExpiredSignatureError:
            logger.info(f"Token expired: {payload=}")
            detail = "Token expired"
            error = True
        except InvalidTokenError:
            logger.info(f"Token invalid: {payload=}")
            detail = "Invalid token"
            error = True
        if error:
            raise HTTPException(
                status_code=401,
                detail=detail,
                headers={"WWW-Authenticate": "Bearer"},
            )
    return payload


def validate_user(
    session: Session = Depends(get_db_connection),
    token: JwtPayload = Depends(validate_token),
) -> int:
    statement = select(Users).where(Users.id == token.user_id)
    user = session.exec(statement).first()
    if user and user.user_lock:
        raise HTTPException(status_code=400, detail="Inactive user")
    return token.user_id
