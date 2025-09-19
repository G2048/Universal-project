## 0.2.0 (2025-09-19)

### Feat

- **app/api/v1/routers/groups.py**: add check user ACL
- **app/api/v1/routers/roles.py**: add check user ACL
- **app/api/v1/routers/settings.py**: add check user ACL
- **app/api/v1/routers/companies.py**: add check user ACL
- **app/api/v1/routers/users.py**: add acl check for every /api/v1/users routers exclude create_user() handler
- **app/api/dependencies/roles.py**: add the check_permissions() function for acl matching
- **app/core/permissions/acl.py**: declare enum of Scopes by every router, Function from database and ACL dict
- **app/api/v1/routers/roles.py**: add handler list_my_roles() manage endpoint /api/v1/groups/my
- **app/api/services/jwt.py**: save in jwt token user_id
- **app/api/v1/routers/roles.py**: add new routers /api/v1/roles
- **app/api/v1/routers/groups.py**: add /api/v1/groups endpoints
- **app/api/v1/routers/settings.py**: add CRUD /api/v1/settings/ endpoints
- **app/api/v1/routers/auth.py**: add /api/v1/auth endpoints for authorization via OAuth2 style
- **app/api/dependencies/auth.py**: add oauth2_scheme and validate_token() - jwt; it is helping functions for routers /auth
- **app/api/services/jwt.py**: add class JWT for generation of jwt token; JwtRefreshTokenPayloadfor refresh token; JwtPayload for description of jwt token
- **app/configs/settings.py**: add JwtSettings env structure
- **app/api/v1/routers/users.py**: add endpoints /api/v1/users/ for manipulation of users
- **app/api/v1/routers/companies.py**: create default group with company in create_company() handler
- **app/api/v1/routers/companies.py**: add raise HTTPExceptions if company not found; for everyone routers except list_companies() and create_company()
- **app/main.py**: add middleware for getting db session include routers of companies
- **app/api/v1/routers/companies.py**: add api CRUD for companies
- **app/api/dependencies/db.py**: add dependencies for getting session of database
- **app/core/database/models.py**: Companies.created_date default_factory=date.today
- **app/core/database/models.py**: declare tables of database on sqlmodel classes
- **app/api/v1/routers/users.py**: add empty handler create_user()
- **app/core/database/schema.sql**: add database sql scheme
- **app/main.py**: add empty server with one the /health handler
- **app/configs/**: add log config, app and database env settings
- **project**: init project

### Fix

- **app/api/v1/routers/roles.py**: channge Scope.settings to Scope.roles for check_permissions() func
- **build/create_database_psql.sh**: add autoincrement for user_roles.id in database
- **app/core/database/models.py**: Users.created_date and Users.user_lock - default values
- **app/configs/log_settings.py**: TypeError: 'str' object does not support item assignment; for set_debug_level() func

### Refactor

- **build/create_database_psql.sh**: ppretty write USER= and PASSWORD= in .create_user.log
- **app/api/v1/routers/users.py**: forward imports from app.api.dependencies
- **app/api/dependencies/**: from .roles import Scope, check_permissions
- **app/api/dependencies/auth.py**: add validate_user() function for checking what uses is not locking; return user_id
- **app/api/v1/routers/groups.py**: change list_my_groups() handler: get user_id from jwt token; rename router to /api/v1/groups/my
- **app/api/dependencies/auth.py**: validate_token() return JwtPayload structure
- **app/api/v1/routers/auth.py**: remove unnecessary checking user_lock is True in get_current_active_user()
- **app/api/v1/routers/settings.py**: add settings_id to PATCH endpoint
- **app/services/**: remove package
- **app/api/v1/routers/**: change response on 204 status for routers delete
- **app/core/database/models.py**: add default value for UserRoles.active_from
- **app/api/v1/routers/users.py**: change response dict with only user_id for create_user() and delete_user() handlers
- **app/api/v1/routers/users.py**: change response to only user.id for create_user() handler
- **app/api/services/hashing.py**: add new class PasswordHasher; remove old app/api/dependencies/hashing.py module
- **app/configs/settings.py**: init DataBaseSettings env structure by import
- **app/api/dependencies/hashing.py**: change hash function in hash_password()
- **app/api/v1/routers/companies.py**: add return types to routers
- **build/**: move create_database_psql.sh to build/
- **app/configs/settings.py**: add to the computed field pg_dsn of DataBaseSettings engine
- **app/configs/settings.py**: remove unnecessary the project_parser var
