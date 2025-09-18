import logging

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse, Response
from sqlmodel import select

from app.api.dependencies import Session, get_db_connection, validate_token
from app.api.services.jwt import JwtPayload
from app.core.database.models import FunctionsDict, RoleFunctions, RolesDict, UserRoles

router = APIRouter(prefix="/roles", tags=["Roles"])

logger = logging.getLogger("app.api.v1.routers.roles")


@router.post("/")
def assign_role_to_user(role: UserRoles, session: Session = Depends(get_db_connection)):
    logger.info(f"{role=}")
    try:
        session.add(role)
        session.commit()
        session.refresh(role)
    except Exception as e:
        logger.error(e)
        session.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error")
    return JSONResponse(
        status_code=201,
        content={"id": f"{role.id}"},
    )


@router.get("/{role_id}/functions")
def list_functions_of_role(
    role_id: int,
    session: Session = Depends(get_db_connection),
) -> list[FunctionsDict]:
    return session.exec(
        select(FunctionsDict)
        .join(RoleFunctions)
        .join(RolesDict, RolesDict.id == RoleFunctions.role_id)
        .where(RoleFunctions.role_id == role_id)
    ).fetchall()


@router.delete("/{role_id}/{function_id}")
def remove_user_role_to_function(
    role_id: int,
    function_id: int,
    session: Session = Depends(get_db_connection),
) -> Response:
    role_function = session.exec(
        select(RoleFunctions).where(
            (RoleFunctions.role_id == role_id)
            & (RoleFunctions.function_code_id == function_id)
        )
    ).first()
    session.delete(role_function)
    session.commit()
    return Response(status_code=204)


@router.patch(
    "/{role_id}",
    description="Назначить роли пользователя (Admin) права на функцю (manage_users - управление пользователей)",
)
def assign_user_role_to_function(
    role_id: int,
    function_id: int,
    session: Session = Depends(get_db_connection),
):
    role = session.exec(select(RolesDict).where(RolesDict.id == role_id)).first()
    if not role:
        raise HTTPException(status_code=404, detail=f"Role {role_id} not found")

    function = session.exec(
        select(FunctionsDict).where(FunctionsDict.id == function_id)
    ).first()
    if not function:
        raise HTTPException(status_code=404, detail=f"Function {function_id} not found")

    role_function = session.exec(
        select(RoleFunctions).where(
            (RoleFunctions.role_id == role.id)
            & (RoleFunctions.function_code_id == function.id)
        )
    ).first()
    if role_function:
        raise HTTPException(status_code=409, detail="Role already assigned")

    role_function = RoleFunctions(role_id=role_id, function_code_id=function_id)
    session.add(role_function)
    session.commit()
    session.refresh(role_function)
    return JSONResponse(
        status_code=201,
        content={"id": f"{role_function.id}"},
    )


@router.get("/my")
def list_my_roles(
    token: JwtPayload = Depends(validate_token),
    session: Session = Depends(get_db_connection),
) -> list[RolesDict]:
    return session.exec(
        select(RolesDict).join(UserRoles).where(UserRoles.user_id == token.user_id)
    ).fetchall()


@router.get("/")
def list_roles(session: Session = Depends(get_db_connection)) -> list[RolesDict]:
    return session.exec(select(RolesDict)).fetchall()


@router.get("/functions")
def list_functions(
    session: Session = Depends(get_db_connection),
) -> list[FunctionsDict]:
    return session.exec(select(FunctionsDict)).fetchall()
