from dotenv import load_dotenv
from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

from .log_settings import set_appname, set_appversion, set_debug_level
from .pyproject import ParserPyproject

load_dotenv()


class AppSettings(BaseSettings):
    appname: str = ParserPyproject.name
    appversion: str = ParserPyproject.version
    debug: bool = False
    cors_origins: list[str] = ["*"]

    @computed_field(return_type=str)
    def appname_log(self) -> str:
        return self.appname.lower().replace(" ", "_")


class DataBaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="PG_")

    host: str = "localhost"
    port: str = "5432"
    user: str
    dbname: str
    password: str
    engine: str = "psycopg"

    @computed_field(return_type=str)
    def pg_dsn(self) -> str:
        return f"postgresql+{self.engine}://{self.user}:{self.password}@{self.host}:{self.port}/{self.dbname}"


_app_settings = AppSettings()

set_debug_level(_app_settings.debug)
set_appname(_app_settings.appname_log)
set_appversion(_app_settings.appversion)


def get_appsettings():
    return _app_settings


def get_database_settings():
    return DataBaseSettings()
