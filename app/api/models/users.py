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


class User(BaseModel):
    username: str
    firtsname: str
    lastname: str
    patronymic: str | None = None
    user_lock: bool | None = None


class UserLogin(BaseModel):
    username: str
    password: str
    grant_type: str = "password"

    def to_url_form(self):
        return f"grant_type={self.grant_type}&&username={self.username}&password={self.password}"


class ResponseToken(BaseModel):
    access_token: str
    token_type: str
