import os
from datetime import datetime

import uvicorn
from fastapi import FastAPI
from starlette import status
from starlette.requests import Request

# You can use markdown for description formatting
app_description = """
My first FastAPI app

## Healthcheck

You can **check health**.

## Misc

You can use them to:

* **Check current server time**;
* **Debug your request data**.
"""
app_tags_description = [
    {
        "name": "healthcheck",
        "description": "Check **health** of your sevice in sporty way.",
    },
    {
        "name": "misc",
        "description": "Some misc to _show off_.",
        "externalDocs": {
            "description": "Misc external docs",
            "url": "https://fastapi.tiangolo.com/",
        },
    },
]
APP_HOST = os.environ.get("APP_HOST", "localhost")
APP_PORT = int(os.environ.get("APP_PORT", "8000"))
# To investigate how OpenAPI docs built visit <module fastapi.application> <class FastAPI> <method openapi()>
app = FastAPI(
    title="My first FastAPI app",
    description=app_description,
    openapi_tags=app_tags_description,
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Ger Goltz",
        "url": "https://www.linkedin.com/in/gerleff/",
        "email": "gerleffx2@gmail.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
    servers=[{"url": f"http://{APP_HOST}:{APP_PORT}", "description": "Local development server"}],
    docs_url="/",  # Not recomended, used in learning purpose
)


@app.get("/ping", tags=["healthcheck"], status_code=status.HTTP_200_OK, response_description="Server is healthy")
async def healthcheck():
    """If server is healthy, response 'pong' will be sent immediately.
    \f
    That description is only shown in code.
    """
    return "pong"


@app.get(
    "/time",
    tags=["misc", "healthcheck"],
    description="Shows current server time.",
    status_code=status.HTTP_200_OK,
)
async def get_server_time():
    return datetime.now()


@app.get(
    "/req_debug",
    tags=["misc"],
    include_in_schema=bool(os.environ.get("DEBUG", True)),
    deprecated=bool(os.environ.get("REQ_DEBUG_DEPRECATED", False)),
    responses={
        status.HTTP_200_OK: {"description": "Request metadata"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": str, "description": "Error during parsing request"},
    },
)
async def parse_request(request: Request):
    req_dict = vars(request)
    for attr_causing_recursion_error in ("app", "router", "route"):
        del req_dict["scope"][attr_causing_recursion_error]
    return req_dict


# Some extra info: https://fastapi.tiangolo.com/advanced/path-operation-advanced-configuration/
if __name__ == "__main__":
    uvicorn.run("__main__:app", host=APP_HOST, port=APP_PORT, reload=True)
