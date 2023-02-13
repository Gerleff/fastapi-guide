from typing import Callable, Union, Protocol

import uvicorn
from fastapi import FastAPI
from starlette.types import Scope, Receive, Send

web_app = FastAPI(docs_url="/")


@web_app.get("/ping")  # Place debug breakpoint on the end of fastapi.routing.APIRouter.add_api_route() to inspect
async def healthcheck():
    """Healthcheck"""
    return "pong"


@web_app.get("/debug")  # Place debug breakpoint on the end of fastapi.routing.APIRouter.add_api_route() to inspect
async def debug(a: int = 2, b: int = 2):
    """Place debug breakpoint on the end of func to inspect
    \f
    Request path from Uvicorn -> ASGI ->:
    1) middlewares calls
    2) route matching in router: defined here - starlette.routing.Router.__call__, called by fastapi.routing.APIRouter
    3) fastapi.routing.APIRoute.__call__ :
        function, stored in attribute fastapi.routing.APIRoute.app is created on appending APIRoute into APIRouter,
        when fastapi.routing.APIRouter.add_api_route() is called
        function works as described below:
        a) route handling init: defined here - starlette.routing.Route.handle(), called by fastapi.routing.APIRouter
        b) starlette.routing.request_response() returns ASGIApp async function
        c) MAIN ENDPOINT LOGIC: fastapi.routing.get_request_handler() returns async def app():
            - solves all affecting dependencies: fastapi.dependencies.utils.solve_dependencies()
            - runs this function passing expected arguments: fastapi.routing.run_endpoint_function()
            - fastapi.routing.serialize_response()
    """
    # import traceback; traceback.print_stack()  # Uncomment to check trace without debugger
    return a * b


class ASGIAppProtocol(Protocol):
    """Common ASGI Protocol"""

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        ...


class WebAppProtocol(ASGIAppProtocol):
    """
    On __init__ app must set up middlewares and routes in router
    On __call__ app must:
     1) handle request with middlewares,
     2) define by router, which route to use,
     3) call route endpoint function and return serialized response
    """

    middlewares: list["MiddlewareProtocol"]
    router: "RouterProtocol"


class MiddlewareProtocol(ASGIAppProtocol):
    """
    Middlewares behave as singly linked list to be processed before Router
    Place debug breakpoint on the end of fastapi.applications.FastAPI.build_middleware_stack() to inspect
    """

    app: Union["MiddlewareProtocol", "RouterProtocol"] | ASGIAppProtocol


class RouterProtocol(ASGIAppProtocol):
    """During __call__ it looks for path-matching Route and calls it"""

    routes: list["RouteProtocol"]


class RouteProtocol(ASGIAppProtocol):
    """app attribute is async function to handle request, endpoint"""

    app: Callable


if __name__ == "__main__":
    uvicorn.run("__main__:web_app", host="localhost", port=8000)
