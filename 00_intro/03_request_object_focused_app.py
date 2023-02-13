from collections import defaultdict
from enum import Enum
from typing import Literal, Callable, Iterable

import uvicorn
from fastapi import FastAPI, Depends
from fastapi.params import Body
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp, Scope, Receive, Send


def modify_response_header(response: Response):
    response.raw_headers.append((b"mountains", b"remember everything"))


web_app = FastAPI(docs_url="/", dependencies=[Depends(modify_response_header)])


# Simple middleware example
class SimpleMiddleware:
    def __init__(self, app: ASGIApp):  # named arg "app" cause of starlette.applications:103
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope.get("type") == "http":
            record = f"{scope['method']} {scope['path']}"
            if scope["query_string"]:
                record += f"?{scope['query_string'].decode('utf-8')}"
            scope["app"].state.user_history[scope["client"][0]].append(record)

        await self.app(scope, receive, send)
        return


# How middlewares are handled: starlette.applications.Starlette.build_middleware_stack
web_app.add_middleware(SimpleMiddleware)


# Request state example
# import time
# @web_app.middleware("http")  # That middleware usage is discouraged
# async def add_start_time_to_request_state(request: Request, call_next):
#     request.state.start_time = time.time()
#     response = await call_next(request)
#     return response


@web_app.on_event("startup")
def init_simple_storage():
    web_app.state.mountains = set()
    web_app.state.user_history = defaultdict(list)


def get_mountains_from_state(request: Request):
    return request.app.state.mountains


@web_app.get("/ping", response_model=Literal["pong"], tags=["healthcheck"])
async def healthcheck():
    return "pong"


@web_app.get("/v0/mountains", response_model=list[str], tags=["01_Simple"])
async def get_mountains(
    name_starts_with: str = None,
    name_contains: str = None,
    limit: int = 10,
    mountains: set = Depends(get_mountains_from_state),
):
    """
    name_starts_with, name_contains and limit are fastapi.params.Query by default.
    They have default values, so they are not required to use.
    Mountains stored in app db_conn are injected with Depends.
    """
    result = list(mountains)
    if name_starts_with:
        result[:] = [name for name in result if name.startswith(name_starts_with)]
    if name_contains:
        result[:] = [name for name in result if name_contains in name]
    return result[:limit]


@web_app.post("/v0/mountains", response_model=set[str], tags=["01_Simple"])
async def add_mountain(new_mountain: str, mountains: set = Depends(get_mountains_from_state)):
    """new_mountain is fastapi.params.Query by default. Let it be for learning purpose"""
    mountains.add(new_mountain)
    return mountains


@web_app.put("/v0/mountains", response_model=set[str], tags=["01_Simple"])
async def renew_mountains(new_mountains: set[str], mountains: set = Depends(get_mountains_from_state)):
    """new_mountains is fastapi.params.Body by default because it is container."""
    mountains.clear()
    mountains |= new_mountains
    return mountains


@web_app.patch("/v0/mountains/{name}", response_model=set[str], tags=["01_Simple"])
async def edit_mountain(
    name: str,
    new_name: str = Body(description="Mountain will be renamed, if it exists in database"),
    mountains: set = Depends(get_mountains_from_state),
):
    """name is fastapi.params.Path variable from url, new_name is enforced to be fastapi.params.Body"""
    try:
        mountains.remove(name)
    except KeyError:
        return mountains
    mountains.add(new_name)
    return mountains


class PaintersEnum(str, Enum):
    Leonardo_da_Vinci = "Leonardo da Vinci"
    Vincent_Van_Gogh = "/vincent Van Gogh"
    Michelangelo = "Michelangelo"
    Pablo_Picasso = "Pablo Picasso"
    Rembrandt = "Rembrandt"


@web_app.delete(
    "/v0/mountains/{name}",
    # Literal doesn't affect OpenApi much
    response_model=dict[Literal["remainders", "last_words", "painter"], str | list[str]],
    tags=["01_Simple"],
)
async def remove_mountain(
    name: str,
    last_words_to_mountain: str = Body(None, example="It will never be forgotten ..."),
    before_go_was_painted_by: PaintersEnum = Body(
        None,
        examples={
            "He went crazy for it": PaintersEnum.Vincent_Van_Gogh,
            "It charmed him so nicely": PaintersEnum.Michelangelo,
        },
    ),
    mountains: set = Depends(get_mountains_from_state),
):
    """Several fastapi.params.Body make endpoint expect body with several keys, named as args"""
    mountains.discard(name)
    return {"remainders": mountains, "last_words": last_words_to_mountain, "painter": before_go_was_painted_by}


# Filters
_filter_func_arg_typing = Iterable[str]
_filter_func_typing = Callable[[_filter_func_arg_typing], list[str]]


def create_filter_func(
    name_starts_with: str = None,
    name_contains: str = None,
    limit: int = 10,
) -> _filter_func_typing:
    """
    Depends func can use the same args as router func
    This dependancy can be used for any resource
    """

    def filter_func(query: _filter_func_arg_typing) -> list[str]:
        result = list(query)
        if name_starts_with:
            result[:] = [name for name in result if name.startswith(name_starts_with)]
        if name_contains:
            result[:] = [name for name in result if name_contains in name]
        return result[:limit]

    return filter_func


@web_app.get("/v1/mountains/", response_model=set[str], tags=["02_Filter"])
async def get_mountains_v1(
    mountains: set = Depends(get_mountains_from_state), filter_func: _filter_func_typing = Depends(create_filter_func)
):
    return filter_func(mountains)


@web_app.get("/v1/mountains/count", response_model=int, tags=["02_Filter"])
async def get_mountains_count_v1(
    mountains: set = Depends(get_mountains_from_state), filter_func: _filter_func_typing = Depends(create_filter_func)
):
    return len(filter_func(mountains))


# Pagination
def get_user_history(request: Request):
    return request.app.state.user_history[request.scope["client"][0]]


def limit_offset_pagination(limit: int = 10, offset: int = 0) -> tuple[int, int]:
    return offset, offset + limit + 1


def page_size_pagination(page: int = 1, page_size: int = 10) -> tuple[int, int]:
    offset = (page - 1) * page_size
    return offset, offset + page_size + 1


@web_app.get("/v0/history", response_model=list[str], tags=["03_Pagination"])
async def get_mountains_count_v1(
    pagination: tuple[int, int] = Depends(limit_offset_pagination), user_history: list[str] = Depends(get_user_history)
):
    return user_history[pagination[0] : pagination[1]]


@web_app.get("/v1/history", response_model=list[str], tags=["03_Pagination"])
async def get_mountains_count_v1(
    pagination: tuple[int, int] = Depends(page_size_pagination), user_history: list[str] = Depends(get_user_history)
):
    return user_history[pagination[0] : pagination[1]]


# How do dependencies resolve?
# Look into fastapi.routing.APIRoute.__init__() and fastapi.dependencies.utils.get_dependants().


if __name__ == "__main__":
    uvicorn.run("__main__:web_app", host="localhost", port=8000, reload=True)
