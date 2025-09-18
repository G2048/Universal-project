import logging

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from app.api.services import (
    JWT,
    ExpiredSignatureError,
    InvalidTokenError,
    JwtPayload,
)

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
