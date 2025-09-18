import logging

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlmodel import select

from app.api.dependencies.db import Session, get_db_connection
from app.core.database.models import Companies

router = APIRouter(prefix="/companies", tags=["Companies"])
logger = logging.getLogger("app.api.v1.routers.companies")


@router.post("/")
def create_company(company: Companies, session: Session = Depends(get_db_connection)):
    try:
        session.add(company)
        session.commit()
        session.refresh(company)
    except Exception as e:
        logger.error(e)
        session.rollback()
        raise
    return company


@router.get("/{company_id}")
def get_company(company_id: int, session: Session = Depends(get_db_connection)):
    logger.info(f"Getting company with id: {company_id}")
    statement = select(Companies).where(Companies.id == company_id)
    company = session.exec(statement).first()
    return company


@router.get("/")
def list_companies(session: Session = Depends(get_db_connection)):
    statement = select(Companies)
    company = session.exec(statement).fetchall()
    return company


# @router.put("/{company_id}")
# def update_company(
#     company_id: int, company: Companies, session: Session = Depends(get_db_connection)
# ):
#     logger.info(f"Updating company with id: {company_id}")
#     try:
#         session.add(company)
#         session.commit()
#         session.refresh(company)
#     except Exception as e:
#         logger.error(e)
#         session.rollback()
#         raise
#     return company


@router.delete("/{company_id}")
def delete_company(company_id: int, session: Session = Depends(get_db_connection)):
    logger.info(f"Deleting company with id: {company_id}")
    statement = select(Companies).where(Companies.id == company_id)
    company = session.exec(statement).first()
    if company:
        session.delete(company)
        session.commit()
    else:
        raise Exception(f"Company with id: {company_id}")
    return JSONResponse(
        status_code=201, content={"msg": f"Company {company_id} deleted successfully"}
    )
