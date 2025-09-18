import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine, select

from app.configs import get_database_settings
from app.core.database.models import Companies, TimezoneDict, UserGroups, Users
from app.main import app

settings = get_database_settings()


engine = create_engine(settings.pg_dsn)

with Session(engine) as session:
    statement = select(Companies).where(Companies.id == 1)
    company = session.exec(statement).first()
    print(company)


ENDPOINT = "api/v1/users/"


def test_get_user():
    user_id = "1"
    with TestClient(app) as client:
        response = client.get(ENDPOINT + user_id)
    assert response.status_code == 200
    # assert response.json() == {"msg": "Hello World"}


def test_list_users():
    with TestClient(app) as client:
        response = client.get(ENDPOINT)
    assert response.status_code == 200
    assert response.json() != []
    response_json = response.json()
    assert isinstance(response_json, list)
    assert isinstance(response_json[0], dict)
    print(f"{response_json=}")


db_settings = get_database_settings()
engine = create_engine(db_settings.pg_dsn)


def _user_group():
    with Session(engine) as session:
        statement = select(UserGroups)
        user_group = session.exec(statement).first()
    print(f"{user_group=}")
    return user_group


@pytest.fixture()
def company_id():
    return _user_group().company_id


@pytest.fixture()
def user_group_id(company_id: int):
    return _user_group().id


@pytest.fixture()
def timezone_id():
    with Session(engine) as session:
        statement = select(TimezoneDict).where(
            TimezoneDict.timezone_name == "Asia/Krasnoyarsk"
        )
        time_zone = session.exec(statement).first()
    print(f"{time_zone=}")
    # id=286
    return time_zone.id


def test_create_delete_user(user_group_id: int, company_id: int, timezone_id: int):
    print(f"{user_group_id=}")
    user = Users(
        company_id=company_id,
        username="TEST USER",
        firtsname="John",
        lastname="Doe",
        password="veryStrongPassword",
        group_id=user_group_id,
        timezone_id=timezone_id,
    )
    with TestClient(app) as client:
        response = client.post(ENDPOINT, data=user.model_dump_json())
        assert response.status_code == 201
        response_json = response.json()
        assert isinstance(response_json, dict)
        print()
        print(f"{response_json=}")

    user_id = response_json["id"]
    with TestClient(app) as client:
        response = client.delete(ENDPOINT + str(user_id))
    assert response.status_code == 201
    response_json = response.json()
    print(f"{response_json=}")
