import os
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.websocket import api_v1_websocket
from app.core.settings import Settings, get_settings
from app.api.routers import get_api_v1_router
from app.server.init import init
from app.server.schedule import lifespan

settings: Settings = get_settings()


def get_ready() -> None:
    init()
    os.makedirs("media/", exist_ok=True)
    os.makedirs("static/", exist_ok=True)


def get_app() -> FastAPI:
    get_ready()

    app = FastAPI(
        title=settings.PROJECT_NAME,
        description=settings.PROJECT_DESCRIPTION,
        version=settings.PROJECT_VERSION,
        docs_url="/",
        lifespan=lifespan,
    )

    app.include_router(get_api_v1_router(), prefix=settings.API_V1_STR)
    app.include_router(api_v1_websocket, prefix=settings.API_V1_STR)
    return app


def create_app() -> CORSMiddleware:
    app = get_app()
    return CORSMiddleware(
        app,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
