from datetime import datetime

from pydantic import BaseModel, Field, SecretStr


class UserCreate(BaseModel):
    username: str
    firstname: str
    lastname: str
    patronymic: str | None = None
    created_date: datetime = Field(default_factory=datetime.now)
    password: SecretStr
    comment: str | None = None
