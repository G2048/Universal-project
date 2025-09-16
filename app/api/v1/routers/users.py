import logging

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.api.models import UserCreate

router = APIRouter(prefix="/users", tags=["Users"])

logger = logging.getLogger("app.api.v1.routers.users")


@router.post("/")
def create_user(user: UserCreate):
    logger.debug(f"{user=}")
    return JSONResponse(content={"username": user.username}, status_code=200)
