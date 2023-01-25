from fastapi import FastAPI
import uvicorn

from models.storage.dependencies import connect_on_startup, disconnect_on_shutdown
from settings import settings
from controller.routers import api_routers

app = FastAPI(docs_url="/", servers=[{"url": settings.ADDRESS, "description": "Local server"}])

for router in api_routers:
    app.include_router(router)


@app.on_event("startup")
async def init_database_session():
    await connect_on_startup(app, settings)


@app.on_event("shutdown")
async def close_database_session():
    await disconnect_on_shutdown(app, settings)


if __name__ == "__main__":
    uvicorn.run("__main__:app", host=settings.HOST, port=settings.PORT, reload=True)
