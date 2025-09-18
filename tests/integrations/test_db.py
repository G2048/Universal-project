from sqlmodel import Session, create_engine, select

from app.configs import get_database_settings
from app.core.database.models import Companies

settings = get_database_settings()


engine = create_engine(settings.pg_dsn)

with Session(engine) as session:
    statement = select(Companies).where(Companies.id == 1)
    company = session.exec(statement).first()
    print(company)
