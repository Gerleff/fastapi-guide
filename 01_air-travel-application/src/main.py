import uvicorn
from fastapi import FastAPI

from controller.routers import api_routers
from models.storage.connection import connect_on_startup, disconnect_on_shutdown
from settings import get_settings, Settings


def build_app(settings: Settings):
    app = FastAPI(docs_url="/", servers=[{"url": settings.ADDRESS, "description": "Local server"}])

    for router in api_routers:
        app.include_router(router)

    @app.on_event("startup")
    async def init_database_session():
        await connect_on_startup(app, settings)

    @app.on_event("shutdown")
    async def close_database_session():
        await disconnect_on_shutdown(app, settings)

    return app


if __name__ == "__main__":
    launch_settings = get_settings()
    web_app = build_app(launch_settings)
    uvicorn.run("__main__:web_app", host=launch_settings.HOST, port=launch_settings.PORT)
