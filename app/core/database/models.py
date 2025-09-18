from datetime import date, time
from typing import Optional

from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    Date,
    ForeignKeyConstraint,
    Index,
    Integer,
    PrimaryKeyConstraint,
    SmallInteger,
    String,
    Text,
    Time,
    UniqueConstraint,
    text,
)
from sqlmodel import Field, Relationship, SQLModel


class FunctionsDict(SQLModel, table=True):
    __tablename__ = "functions_dict"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="pk_functions"),
        {"comment": "Таблица справочник ролевых функций"},
    )

    id: int | None = Field(
        default=None, sa_column=Column("id", SmallInteger, primary_key=True)
    )
    code: str = Field(sa_column=Column("code", String(30)))
    version: int = Field(sa_column=Column("version", SmallInteger))

    role_functions: list["RoleFunctions"] = Relationship(back_populates="function_code")


class Modules(SQLModel, table=True):
    __table_args__ = (
        PrimaryKeyConstraint("id", name="pk_modules"),
        Index("idx_modules_code", "code"),
        {"comment": "Таблица дополнительных модулей"},
    )

    id: int = Field(sa_column=Column("id", Integer, primary_key=True))
    code: str = Field(sa_column=Column("code", String(30)))
    name: str = Field(sa_column=Column("name", String(60)))

    module_company_links: list["ModuleCompanyLinks"] = Relationship(
        back_populates="module"
    )


class PropertyCodeDict(SQLModel, table=True):
    __tablename__ = "property_code_dict"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="pk_property_code_dict"),
        Index("idx_property_code_dict_code", "code"),
        Index("idx_property_code_dict_group_code_code", "group_code", "code"),
        {
            "comment": "Таблица справочник кодов для свойств пользователя\n"
            "PROFILE_IMAGE - путь до картинки с профилем пользователя\n"
            "USER_MOBILE - телефон пользователя\n"
            "USER_NUMVER - индиыидуальный номер пользователя"
        },
    )

    id: int | None = Field(
        default=None, sa_column=Column("id", SmallInteger, primary_key=True)
    )
    group_code: str = Field(sa_column=Column("group_code", String(30)))
    code: str = Field(sa_column=Column("code", String(30)))
    name: str | None = Field(default=None, sa_column=Column("name", String(100)))

    companies: list["Companies"] = Relationship(back_populates="property")
    company_properties: list["CompanyProperties"] = Relationship(
        back_populates="property_code"
    )
    user_properties: list["UserProperties"] = Relationship(
        back_populates="property_code"
    )


class Reports(SQLModel, table=True):
    __table_args__ = (
        PrimaryKeyConstraint("id", name="pk_reports"),
        Index("idx_reports_code", "code"),
        Index("idx_reports_code_version", "code", "version"),
        {"comment": "Таблица справочник отчетов"},
    )

    id: int = Field(sa_column=Column("id", Integer, primary_key=True))
    code: str = Field(sa_column=Column("code", String(30)))
    name: str = Field(sa_column=Column("name", String))
    version: int = Field(sa_column=Column("version", Integer))

    user_report_links: list["UserReportLinks"] = Relationship(back_populates="report")


class RolesDict(SQLModel, table=True):
    __tablename__ = "roles_dict"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="pk_roles_dict"),
        {"comment": "Таблица справочник ролей пользователя"},
    )

    id: int | None = Field(
        default=None, sa_column=Column("id", SmallInteger, primary_key=True)
    )
    code: str = Field(sa_column=Column("code", String(30)))
    name: str = Field(sa_column=Column("name", String(60)))

    role_functions: list["RoleFunctions"] = Relationship(back_populates="role")
    user_roles: list["UserRoles"] = Relationship(back_populates="role")


class SettingsDict(SQLModel, table=True):
    __tablename__ = "settings_dict"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="pk_settings_dict"),
        Index("idx_settings_dict_code", "code"),
        {"comment": "Таблица справочник кодов системы"},
    )

    id: int | None = Field(
        default=None, sa_column=Column("id", SmallInteger, primary_key=True)
    )
    code: str = Field(sa_column=Column("code", String(30)))
    name: str = Field(sa_column=Column("name", String(255)))

    settings: list["Settings"] = Relationship(back_populates="setting_code")


class ShablonDict(SQLModel, table=True):
    __tablename__ = "shablon_dict"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="pk_shablon_dict"),
        Index("idx_shablon_dict_code", "code"),
        {"comment": "Таблици справочник шаблонов"},
    )

    id: int = Field(sa_column=Column("id", Integer, primary_key=True))
    code: str = Field(sa_column=Column("code", String(30)))
    name: str = Field(sa_column=Column("name", String(255)))
    value: str | None = Field(default=None, sa_column=Column("value", Text))


class StatusDict(SQLModel, table=True):
    __tablename__ = "status_dict"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="pk_status_dict"),
        Index("idx_status_dict_code", "code"),
    )

    id: int = Field(sa_column=Column("id", Integer, primary_key=True))
    code: str = Field(sa_column=Column("code", String(16)))
    name: str = Field(sa_column=Column("name", String(60)))

    user_sendings: list["UserSendings"] = Relationship(back_populates="status")


class TimezoneDict(SQLModel, table=True):
    __tablename__ = "timezone_dict"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="pk_timezone_dict"),
        {"comment": "Таблица с справчоник таймзон"},
    )

    id: int | None = Field(
        default=None, sa_column=Column("id", SmallInteger, primary_key=True)
    )
    timezone_name: str | None = Field(
        default=None, sa_column=Column("timezone_name", String(255))
    )
    timezone: time | None = Field(
        default=None, sa_column=Column("timezone", Time(True))
    )

    users: list["Users"] = Relationship(back_populates="timezone")


class Companies(SQLModel, table=True):
    __table_args__ = (
        ForeignKeyConstraint(
            ["property_id"],
            ["property_code_dict.id"],
            name="companies_property_id_fkey",
        ),
        PrimaryKeyConstraint("id", name="pk_companies"),
        Index("idx_companies_bic", "bic"),
        Index("idx_companies_inn", "inn"),
        Index("idx_companies_kpp", "kpp"),
        Index("idx_companies_ogrn", "ogrn"),
        Index("idx_companies_property_id", "property_id"),
        {"comment": "Таблица с компаниями"},
    )

    id: int | None = Field(
        default=None, sa_column=Column("id", BigInteger, primary_key=True)
    )
    property_id: int = Field(sa_column=Column("property_id", BigInteger))
    name: str = Field(sa_column=Column("name", String(255)))
    created_date: date = Field(
        sa_column=Column("created_date", Date),
        default_factory=date.today,
    )
    inn: str = Field(sa_column=Column("inn", String(16)))
    kpp: str = Field(sa_column=Column("kpp", String(9)))
    ogrn: str | None = Field(default=None, sa_column=Column("ogrn", String(13)))
    bic: str | None = Field(default=None, sa_column=Column("bic", String(9)))

    property: Optional["PropertyCodeDict"] = Relationship(back_populates="companies")
    company_properties: list["CompanyProperties"] = Relationship(
        back_populates="company"
    )
    departments: list["Departments"] = Relationship(back_populates="company")
    license: list["License"] = Relationship(back_populates="company")
    module_company_links: list["ModuleCompanyLinks"] = Relationship(
        back_populates="company"
    )
    user_groups: list["UserGroups"] = Relationship(back_populates="company")
    users: list["Users"] = Relationship(back_populates="company")


class RoleFunctions(SQLModel, table=True):
    __tablename__ = "role_functions"
    __table_args__ = (
        ForeignKeyConstraint(
            ["function_code_id"],
            ["functions_dict.id"],
            name="role_functions_function_code_id_fkey",
        ),
        ForeignKeyConstraint(
            ["role_id"], ["roles_dict.id"], name="role_functions_role_id_fkey"
        ),
        PrimaryKeyConstraint("id", name="pk_role_functions"),
        Index("idx_role_functions_function_code_id", "function_code_id"),
        Index("idx_role_functions_role_id", "role_id"),
        {"comment": "Таблица с ролевыми функциями"},
    )

    id: int | None = Field(
        default=None, sa_column=Column("id", SmallInteger, primary_key=True)
    )
    role_id: int = Field(sa_column=Column("role_id", SmallInteger))
    function_code_id: int = Field(sa_column=Column("function_code_id", SmallInteger))

    function_code: Optional["FunctionsDict"] = Relationship(
        back_populates="role_functions"
    )
    role: Optional["RolesDict"] = Relationship(back_populates="role_functions")


class Settings(SQLModel, table=True):
    __table_args__ = (
        ForeignKeyConstraint(
            ["setting_code_id"],
            ["settings_dict.id"],
            name="settings_setting_code_id_fkey",
        ),
        PrimaryKeyConstraint("id", name="pk_settings"),
        Index("idx_settings_active_from", "active_from"),
        Index("idx_settings_active_from_active_to", "active_from", "active_to"),
        Index("idx_settings_active_to", "active_to"),
        Index(
            "idx_settings_property_code_id_active_from_active_to",
            "setting_code_id",
            "active_from",
            "active_to",
        ),
        Index("idx_settings_setting_code_id", "setting_code_id"),
        Index("idx_settings_setting_code_id_active_to", "setting_code_id", "active_to"),
        {"comment": "Таблица общих свойст"},
    )

    id: int | None = Field(
        default=None, sa_column=Column("id", SmallInteger, primary_key=True)
    )
    setting_code_id: int = Field(sa_column=Column("setting_code_id", SmallInteger))
    value: str = Field(sa_column=Column("value", String(255)))
    active_from: date = Field(sa_column=Column("active_from", Date))
    active_to: date | None = Field(default=None, sa_column=Column("active_to", Date))

    setting_code: Optional["SettingsDict"] = Relationship(back_populates="settings")


class CompanyProperties(SQLModel, table=True):
    __tablename__ = "company_properties"
    __table_args__ = (
        ForeignKeyConstraint(
            ["company_id"], ["companies.id"], name="company_properties_company_id_fkey"
        ),
        ForeignKeyConstraint(
            ["property_code_id"],
            ["property_code_dict.id"],
            name="company_properties_property_code_id_fkey",
        ),
        PrimaryKeyConstraint("id", name="pk_company_properties"),
        Index("idx_company_properties_company_id", "company_id"),
        Index(
            "idx_company_properties_company_id_property_code_id",
            "company_id",
            "property_code_id",
        ),
        Index(
            "idx_company_properties_property_code_id", "property_code_id", unique=True
        ),
        {"comment": "Таблица свойств компаний"},
    )

    id: int | None = Field(
        default=None, sa_column=Column("id", BigInteger, primary_key=True)
    )
    company_id: int = Field(sa_column=Column("company_id", BigInteger))
    property_code_id: int = Field(sa_column=Column("property_code_id", SmallInteger))
    value: str | None = Field(default=None, sa_column=Column("value", String(255)))

    company: Optional["Companies"] = Relationship(back_populates="company_properties")
    property_code: Optional["PropertyCodeDict"] = Relationship(
        back_populates="company_properties"
    )


class Departments(SQLModel, table=True):
    __table_args__ = (
        ForeignKeyConstraint(
            ["company_id"], ["companies.id"], name="departments_company_id_fkey"
        ),
        PrimaryKeyConstraint("id", name="pk_departments"),
        Index("idx_departments_code", "code"),
        Index("idx_departments_company_id", "company_id"),
        {"comment": "Таблица с подраздлений"},
    )

    id: int | None = Field(
        default=None, sa_column=Column("id", BigInteger, primary_key=True)
    )
    company_id: int = Field(sa_column=Column("company_id", BigInteger))
    code: int = Field(sa_column=Column("code", BigInteger))
    name: str = Field(sa_column=Column("name", String(255)))
    created_date: date = Field(sa_column=Column("created_date", Date))

    company: Optional["Companies"] = Relationship(back_populates="departments")


class License(SQLModel, table=True):
    __table_args__ = (
        ForeignKeyConstraint(
            ["company_id"], ["companies.id"], name="license_company_id_fkey"
        ),
        PrimaryKeyConstraint("id", name="pk_license"),
        Index("idx_license_active_from_active_to", "active_from", "active_to"),
        Index("idx_license_company_id", "company_id"),
        Index("idx_license_company_id_active_from", "company_id", "active_from"),
        Index(
            "idx_license_company_id_active_from_active_to",
            "company_id",
            "active_from",
            "active_to",
        ),
        {"comment": "Таблица с лицензиями"},
    )

    id: int | None = Field(
        default=None, sa_column=Column("id", BigInteger, primary_key=True)
    )
    company_id: int = Field(sa_column=Column("company_id", BigInteger))
    lisense_key: str = Field(sa_column=Column("lisense_key", String(1000)))
    active_from: date = Field(sa_column=Column("active_from", Date))
    active_to: date = Field(sa_column=Column("active_to", Date))

    company: Optional["Companies"] = Relationship(back_populates="license")


class ModuleCompanyLinks(SQLModel, table=True):
    __tablename__ = "module_company_links"
    __table_args__ = (
        ForeignKeyConstraint(
            ["company_id"],
            ["companies.id"],
            name="module_company_links_company_id_fkey",
        ),
        ForeignKeyConstraint(
            ["module_id"], ["modules.id"], name="module_company_links_module_id_fkey"
        ),
        PrimaryKeyConstraint("id", name="pk_module_company_links"),
        Index("idx_module_company_links_active_from", "active_from"),
        Index("idx_module_company_links_active_to", "active_to"),
        Index("idx_module_company_links_company_id", "company_id"),
        Index(
            "idx_module_company_links_company_id_active_from_active_to",
            "company_id",
            "active_from",
            "active_to",
        ),
        Index("idx_module_company_links_module_id", "module_id"),
        {"comment": "Таблица связей модулей и компаний"},
    )

    id: int | None = Field(
        default=None, sa_column=Column("id", BigInteger, primary_key=True)
    )
    module_id: int = Field(sa_column=Column("module_id", Integer))
    company_id: int = Field(sa_column=Column("company_id", BigInteger))
    position: int = Field(sa_column=Column("position", Integer))
    active_from: date = Field(sa_column=Column("active_from", Date))
    active_to: date | None = Field(default=None, sa_column=Column("active_to", Date))

    company: Optional["Companies"] = Relationship(back_populates="module_company_links")
    module: Optional["Modules"] = Relationship(back_populates="module_company_links")


class UserGroups(SQLModel, table=True):
    __tablename__ = "user_groups"
    __table_args__ = (
        ForeignKeyConstraint(
            ["company_id"], ["companies.id"], name="user_groups_company_id_fkey"
        ),
        PrimaryKeyConstraint("id", name="pk_user_groups"),
        Index("idx_user_groups_company_id", "company_id"),
        {"comment": "Таблица групп пользователей"},
    )

    id: int | None = Field(
        default=None, sa_column=Column("id", BigInteger, primary_key=True)
    )
    company_id: int = Field(sa_column=Column("company_id", BigInteger))
    group_name: str = Field(sa_column=Column("group_name", String(255)))
    comment: str | None = Field(default=None, sa_column=Column("comment", String(1000)))

    company: Optional["Companies"] = Relationship(back_populates="user_groups")
    users: list["Users"] = Relationship(back_populates="group")


class Users(SQLModel, table=True):
    __table_args__ = (
        ForeignKeyConstraint(
            ["company_id"], ["companies.id"], name="users_company_id_fkey"
        ),
        ForeignKeyConstraint(
            ["group_id"], ["user_groups.id"], name="users_group_id_fkey"
        ),
        ForeignKeyConstraint(
            ["timezone_id"], ["timezone_dict.id"], name="users_timezone_id_fkey"
        ),
        PrimaryKeyConstraint("id", name="pk_users"),
        Index("idx_users_company_id", "company_id"),
        Index("idx_users_company_id_group_id", "company_id", "group_id"),
        Index("idx_users_group_id", "group_id"),
        Index("idx_users_id_company_id", "id", "company_id"),
        Index("idx_users_id_group_id", "id", "group_id"),
        Index("idx_users_id_property_id", "id"),
        Index("idx_users_timezone_id", "timezone_id"),
        Index("idx_users_username", "username"),
        Index("idx_users_username_user_lock", "username", "user_lock"),
        {"comment": "Таблица пользователей"},
    )

    id: int | None = Field(
        default=None, sa_column=Column("id", BigInteger, primary_key=True)
    )
    company_id: int = Field(sa_column=Column("company_id", BigInteger))
    group_id: int = Field(sa_column=Column("group_id", BigInteger))
    timezone_id: int = Field(sa_column=Column("timezone_id", SmallInteger))
    username: str = Field(sa_column=Column("username", String(60)))
    firtsname: str = Field(sa_column=Column("firtsname", String(60)))
    lastname: str = Field(sa_column=Column("lastname", String(60)))
    created_date: date = Field(
        sa_column=Column("created_date", Date), default_factory=date.today
    )
    user_lock: bool = Field(
        sa_column=Column(
            "user_lock", Boolean, server_default=text("false"), default=False
        )
    )
    password: str = Field(sa_column=Column("password", String(255)))
    patronymic: str | None = Field(
        default=None, sa_column=Column("patronymic", String(60))
    )
    comment: str | None = Field(default=None, sa_column=Column("comment", String(1000)))

    company: Optional["Companies"] = Relationship(back_populates="users")
    group: Optional["UserGroups"] = Relationship(back_populates="users")
    timezone: Optional["TimezoneDict"] = Relationship(back_populates="users")
    user_properties: list["UserProperties"] = Relationship(back_populates="user")
    user_report_links: list["UserReportLinks"] = Relationship(back_populates="user")
    user_roles: list["UserRoles"] = Relationship(back_populates="user")
    user_sendings: Optional["UserSendings"] = Relationship(
        sa_relationship_kwargs={"uselist": False}, back_populates="user"
    )


class UserProperties(SQLModel, table=True):
    __tablename__ = "user_properties"
    __table_args__ = (
        ForeignKeyConstraint(
            ["property_code_id"],
            ["property_code_dict.id"],
            name="user_properties_property_code_id_fkey",
        ),
        ForeignKeyConstraint(
            ["user_id"], ["users.id"], name="user_properties_user_id_fkey"
        ),
        PrimaryKeyConstraint("id", name="pk_user_properties"),
        Index("idx_user_properties_property_code_id", "property_code_id", unique=True),
        Index("idx_user_properties_property_id", "user_id"),
        Index(
            "idx_user_properties_property_id_property_code_id",
            "user_id",
            "property_code_id",
        ),
        {"comment": "Таблица свойств пользователей"},
    )

    id: int | None = Field(
        default=None, sa_column=Column("id", BigInteger, primary_key=True)
    )
    user_id: int = Field(sa_column=Column("user_id", BigInteger))
    property_code_id: int = Field(sa_column=Column("property_code_id", SmallInteger))
    value: str | None = Field(default=None, sa_column=Column("value", String(255)))

    property_code: Optional["PropertyCodeDict"] = Relationship(
        back_populates="user_properties"
    )
    user: Optional["Users"] = Relationship(back_populates="user_properties")


class UserReportLinks(SQLModel, table=True):
    __tablename__ = "user_report_links"
    __table_args__ = (
        ForeignKeyConstraint(
            ["report_id"], ["reports.id"], name="user_report_links_report_id_fkey"
        ),
        ForeignKeyConstraint(
            ["user_id"], ["users.id"], name="user_report_links_user_id_fkey"
        ),
        PrimaryKeyConstraint("id", name="pk_user_report_links"),
        Index("idx_user_report_links_acive_from", "acive_from"),
        Index("idx_user_report_links_acive_from_active_to", "acive_from", "active_to"),
        Index("idx_user_report_links_active_to", "active_to"),
        Index("idx_user_report_links_created_date", "created_date"),
        Index("idx_user_report_links_id", "id"),
        Index("idx_user_report_links_report_id", "report_id"),
        Index("idx_user_report_links_user_id", "user_id"),
        Index(
            "idx_user_report_links_user_id_acive_from_active_to",
            "user_id",
            "acive_from",
            "active_to",
        ),
        Index("idx_user_report_links_user_id_active_to", "user_id", "active_to"),
        {"comment": "Таблица связей отчетов и пользователей"},
    )

    id: int | None = Field(
        default=None, sa_column=Column("id", BigInteger, primary_key=True)
    )
    user_id: int = Field(sa_column=Column("user_id", BigInteger))
    report_id: int = Field(sa_column=Column("report_id", Integer))
    created_date: date = Field(sa_column=Column("created_date", Date))
    acive_from: date = Field(sa_column=Column("acive_from", Date))
    active_to: date | None = Field(default=None, sa_column=Column("active_to", Date))

    report: Optional["Reports"] = Relationship(back_populates="user_report_links")
    user: Optional["Users"] = Relationship(back_populates="user_report_links")


class UserRoles(SQLModel, table=True):
    __tablename__ = "user_roles"
    __table_args__ = (
        ForeignKeyConstraint(
            ["role_id"], ["roles_dict.id"], name="user_roles_role_id_fkey"
        ),
        ForeignKeyConstraint(["user_id"], ["users.id"], name="user_roles_user_id_fkey"),
        PrimaryKeyConstraint("id", name="pk_user_roles"),
        Index("idx_user_roles_active_from", "active_from"),
        Index("idx_user_roles_active_to", "active_to"),
        Index("idx_user_roles_role_id", "role_id"),
        Index("idx_user_roles_user_id", "user_id"),
        Index(
            "idx_user_roles_user_id_role_id_active_to",
            "user_id",
            "role_id",
            "active_to",
        ),
        {"comment": "Таблица ролей пользователей"},
    )

    id: int = Field(sa_column=Column("id", Integer, primary_key=True))
    user_id: int = Field(sa_column=Column("user_id", BigInteger))
    role_id: int = Field(sa_column=Column("role_id", SmallInteger))
    active_from: date = Field(
        sa_column=Column("active_from", Date), default_factory=date.today
    )
    active_to: date | None = Field(default=None, sa_column=Column("active_to", Date))

    role: Optional["RolesDict"] = Relationship(back_populates="user_roles")
    user: Optional["Users"] = Relationship(back_populates="user_roles")


class UserSendings(SQLModel, table=True):
    __tablename__ = "user_sendings"
    __table_args__ = (
        ForeignKeyConstraint(
            ["status_id"], ["status_dict.id"], name="user_sendings_status_id_fkey"
        ),
        ForeignKeyConstraint(
            ["user_id"], ["users.id"], name="user_sendings_user_id_fkey"
        ),
        PrimaryKeyConstraint("id", name="pk_user_sendings"),
        UniqueConstraint("user_id", name="user_sendings_key"),
        Index("idx_user_sendings_created_date", "created_date"),
        Index("idx_user_sendings_status_id", "status_id"),
        Index("idx_user_sendings_user_id", "user_id"),
        Index(
            "idx_user_sendings_user_id_status_id_created_date",
            "user_id",
            "status_id",
            "created_date",
        ),
        {"comment": "Таблица рассылки сообщений по пользователям"},
    )

    id: int | None = Field(
        default=None, sa_column=Column("id", BigInteger, primary_key=True)
    )
    user_id: int = Field(sa_column=Column("user_id", BigInteger))
    status_id: int = Field(sa_column=Column("status_id", Integer))
    created_date: date = Field(sa_column=Column("created_date", Date))
    message: str = Field(sa_column=Column("message", String(4000)))

    status: Optional["StatusDict"] = Relationship(back_populates="user_sendings")
    user: Optional["Users"] = Relationship(back_populates="user_sendings")
