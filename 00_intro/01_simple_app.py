from typing import Callable, Union

from fastapi import FastAPI
import uvicorn
from starlette.types import Scope, Receive, Send

web_app = FastAPI(docs_url="/")


@web_app.get("/ping")  # Place debug breakpoint on the end of fastapi.routing.APIRouter.add_api_route() to inspect
async def healthcheck():
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
    return "pong"


class ASGIAppInterface:
    """Common ASGI interface"""
    def __call__(self, scope: Scope, receive: Receive, send: Send):
        ...


class MiddlewareInterface(ASGIAppInterface):
    """
    Middlewares behave as singly linked list to be processed before Router
    Place debug breakpoint on the end of fastapi.applications.FastAPI.build_middleware_stack() to inspect
    """
    app: Union["MiddlewareInterface", "RouterInterface"]


class RouterInterface(ASGIAppInterface):
    """During __call__ it looks for path-matching Route and calls it"""
    routes: list["RouteInterface"]


class RouteInterface(ASGIAppInterface):
    """app attribute is async function to handle request, endpoint"""
    app: Callable


if __name__ == "__main__":
    uvicorn.run("__main__:web_app", host="localhost", port=8000, reload=True)
