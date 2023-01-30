import uvicorn

from config.settings import get_settings, Settings


def build_app(settings: Settings):
    from fastapi import FastAPI

    from controller.routers import api_routers
    from config.exception_handlers import exception_handlers

    from model.storage.connection import connect_on_startup, disconnect_on_shutdown

    app = FastAPI(docs_url="/", servers=[{"url": settings.app.ADDRESS, "description": "Local server"}])

    for exc, handler in exception_handlers:
        app.add_exception_handler(exc, handler)
    for router in api_routers:
        app.include_router(router)

    @app.on_event("startup")
    async def init_database_session():
        await connect_on_startup(app, settings.database)

    @app.on_event("shutdown")
    async def close_database_session():
        await disconnect_on_shutdown(app, settings.database)

    return app


if __name__ == "__main__":
    launch_settings = get_settings()
    web_app = build_app(launch_settings)
    uvicorn.run("__main__:web_app", host=launch_settings.app.HOST, port=launch_settings.app.PORT)
