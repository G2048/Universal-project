from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware

from app.api.v1 import routers as routers_v1
from app.configs import LogConfig, get_appsettings, get_logger

logger = get_logger()

settings = get_appsettings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # For activation of connections, creds and etc...
    yield


app = FastAPI(
    title=settings.appname.capitalize(),
    lifespan=lifespan,
    version=settings.appversion,
    swagger_ui_parameters={"syntaxHighlight": {"theme": "obsidian"}},
)

app.include_router(routers_v1.users, prefix="/api/v1")


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
