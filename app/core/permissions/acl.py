from enum import StrEnum


class Scope(StrEnum):
    companies = "companies"
    users = "users"
    settings = "settings"
    groups = "groups"
    roles = "roles"


# TODO: по хорошему нужно брать данные правила динамии из БД
# Возможно стоит подумать над внедрением OPA...
class Functions(StrEnum):
    manage_all = "manage_all"
    read_users = "read_users"
    create_users = "create_users"
    delete_users = "delete_users"
    list_users = "list_users"
    manage_users = "manage_users"
    manage_companies = "manage_companies"
    manage_settings = "manage_settings"
    manage_groups = "manage_groups"
    manage_roles = "manage_roles"
    export_data = "export_data"
    import_data = "import_data"


ACL = {
    Scope.users: {
        Functions.manage_all,
        Functions.read_users,
        Functions.create_users,
        Functions.delete_users,
        Functions.list_users,
        Functions.manage_users,
    },
    Scope.companies: {
        Functions.manage_all,
        Functions.manage_companies,
        Functions.manage_settings,
        Functions.manage_groups,
        Functions.manage_roles,
        Functions.export_data,
        Functions.import_data,
    },
    Scope.settings: {
        Functions.manage_all,
        Functions.manage_settings,
    },
    Scope.groups: {
        Functions.manage_all,
        Functions.manage_groups,
    },
    Scope.roles: {
        Functions.manage_all,
        Functions.manage_roles,
    },
}
