from fastapi import Request
from sqlalchemy.engine import Engine
from sqlmodel import Session


def get_session(engine: Engine):
    with Session(engine) as session:
        yield session


def get_db_connection(request: Request) -> Session:
    return next(request.state.db)
