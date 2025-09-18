import logging

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from sqlmodel import select

from app.api.dependencies.db import Session, get_db_connection
from app.api.models.companies import CreateCompany
from app.core.database.models import Companies, UserGroups

router = APIRouter(prefix="/companies", tags=["Companies"])
logger = logging.getLogger("app.api.v1.routers.companies")


@router.post("/")
def create_company(
    create: CreateCompany,
    session: Session = Depends(get_db_connection),
) -> Companies:
    logger.info(f"Creating company with data: {create}")
    try:
        session.add(create.company)
        session.commit()
        session.refresh(create.company)
    except Exception as e:
        logger.error(e)
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))

    if create.user_group is None:
        create.user_group = UserGroups(
            company_id=create.company.id,
            group_name=create.company.name,
            comment="Default group",
        )
    logger.info(f"{create.user_group=}")
    try:
        session.add(create.user_group)
        session.commit()
    except Exception as e:
        logger.error(e)
        session.rollback()
        session.delete(create.company)
        session.commit()
        raise HTTPException(status_code=500, detail=str(e))
    session.refresh(create.company)
    return create.company


@router.get("/{company_id}")
def get_company(
    company_id: int, session: Session = Depends(get_db_connection)
) -> Companies:
    logger.info(f"Getting company with id: {company_id}")
    statement = select(Companies).where(Companies.id == company_id)
    company = session.exec(statement).first()
    if not company:
        raise HTTPException(
            status_code=404, detail=f"Company with id: {company_id} not found"
        )
    return company


@router.get("/")
def list_companies(session: Session = Depends(get_db_connection)) -> list[Companies]:
    statement = select(Companies)
    companies = session.exec(statement).fetchall()
    return companies


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
        raise HTTPException(
            status_code=404, detail=f"Company with id: {company_id} not found"
        )
    return Response(status_code=204)
