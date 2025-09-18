import logging
from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestFormStrict
from sqlmodel import select

from app.api.dependencies import (
    Session,
    get_db_connection,
    validate_token,
)
from app.api.models.users import ResponseToken
from app.api.services import (
    JWT,
    JwtPayload,
    PasswordHasher,
)
from app.core.database.models import Users

router = APIRouter(
    prefix="/auth",
    tags=["Authorization"],
)

logger = logging.getLogger("app.api.v1.routers.auth")


def get_user(session: Session, username: str) -> Users | None:
    statement = select(Users).where(Users.username == username)
    return session.exec(statement).first()


def authenticate_user(session: Session, username: str, password: str) -> Users | None:
    user = get_user(session, username)
    if not user:
        return None
    if not PasswordHasher.verify_password(password, user.password):
        return None
    return user


@router.post("/")
def get_token(
    body: Annotated[OAuth2PasswordRequestFormStrict, Depends()],
    session: Session = Depends(get_db_connection),
) -> ResponseToken:
    logger.debug(f"Body: {body=}")
    username = body.username.partition("@")[0]
    logger.info(f"Username: {username=}")
    user_exist = authenticate_user(session, username, body.password)
    if not user_exist:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    token = JWT.generate_token(JwtPayload(sub=username))
    return ResponseToken(access_token=token, token_type="bearer")


@router.get("/")
def check_login(username: str = Depends(validate_token)):
    logged_in = True
    status_code = HTTPStatus.OK
    return JSONResponse(content={"logged_in": logged_in}, status_code=status_code)


async def get_current_active_user(
    session: Session = Depends(get_db_connection),
    username: str = Depends(validate_token),
):
    statement = select(Users).where(Users.username == username)
    user = session.exec(statement).first()
    if user and user.user_lock:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user


@router.get("/me/", response_model=Users)
def read_users_me(
    current_user: Annotated[Users, Depends(get_current_active_user)],
):
    return current_user
