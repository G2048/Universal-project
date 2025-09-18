from collections.abc import Callable
from contextlib import asynccontextmanager
from typing import Any

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlmodel import create_engine
from starlette.middleware.cors import CORSMiddleware

from app.api.dependencies.db import get_session
from app.api.v1 import routers as routers_v1
from app.configs import LogConfig, get_appsettings, get_database_settings, get_logger

logger = get_logger()

settings = get_appsettings()
db_settings = get_database_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # For activation of connections, creds and etc...
    app.state.db_engine = create_engine(db_settings.pg_dsn)
    yield


app = FastAPI(
    title=settings.appname.capitalize(),
    lifespan=lifespan,
    version=settings.appversion,
    swagger_ui_parameters={"syntaxHighlight": {"theme": "obsidian"}},
)


@app.middleware("http")
def db_session_middleware(request: Request, call_next: Callable[[Request], Any]) -> Any:
    try:
        request.state.db = get_session(request.app.state.db_engine)
        response = call_next(request)
    except Exception as e:
        logger.error(e)
        raise RuntimeError(e) from e
    return response


app.include_router(routers_v1.companies, prefix="/api/v1")
app.include_router(routers_v1.users, prefix="/api/v1")
app.include_router(routers_v1.auth, prefix="/api/v1")
app.include_router(routers_v1.settings, prefix="/api/v1")


@app.get("/health", tags=["health check"])
def health():
    return JSONResponse(content={"status": "ok"}, status_code=200)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def main():
    logger.info("Starting web app...")
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_config=LogConfig,
        reload=False,
    )


if __name__ == "__main__":
    main()
