from fastapi import FastAPI
import uvicorn

from settings import settings
from controller.routers import api_routers

app = FastAPI(docs_url="/", servers=[{"url": settings.ADDRESS, "description": "Local server"}])

for router in api_routers:
    app.include_router(router)


# @app.on_event("startup")
# def init_simple_storage():
#     app.state.storage = Storage.parse_file("storage.json")
#
#
# @app.on_event("shutdown")
# def save_simple_storage():
#     with open("models/storage/pythonic/storage.json", "w") as file:
#         file.write(app.state.storage.json(indent=4, ensure_ascii=False))
#
#
# def get_example_storage(request: Request) -> Storage:
#     return request.app.state.storage


if __name__ == "__main__":
    uvicorn.run("__main__:app", host=settings.HOST, port=settings.PORT, reload=True)
