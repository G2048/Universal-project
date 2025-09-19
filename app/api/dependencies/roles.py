from sqlmodel import Session, select
from starlette.exceptions import HTTPException

from app.core.database.models import FunctionsDict, RoleFunctions, RolesDict, UserRoles
from app.core.permissions.acl import ACL, Scope

# SELECT rd.*,fd.* FROM user_roles ur
# JOIN roles_dict rd ON rd.id=ur.role_id
# JOIN role_functions rf ON rf.role_id=rd.id
# JOIN functions_dict fd ON rf.function_code_id=fd.id
# WHERE ur.user_id=12;


def check_permissions(
    user_id: int,
    current_scope: Scope,
    session: Session,
):
    statement = (
        select(FunctionsDict)
        .select_from(UserRoles)
        .join(RolesDict, RolesDict.id == UserRoles.role_id)
        .join(RoleFunctions, RoleFunctions.role_id == RolesDict.id)
        .join(FunctionsDict, FunctionsDict.id == RoleFunctions.function_code_id)
        .where(UserRoles.user_id == user_id)
    )
    functions_dict = session.exec(statement).fetchall()
    for fun_dict in functions_dict:
        if fun_dict.code in ACL[current_scope]:
            return True

    raise HTTPException(
        status_code=403,
        detail=f"User {user_id} doesn't have permission to {current_scope}",
    )
