from pydantic import BaseModel

from app.core.database.models import Companies, UserGroups


class CreateCompany(BaseModel):
    company: Companies
    user_group: UserGroups | None = None
