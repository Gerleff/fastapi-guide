"""Inspired by https://www.uvicorn.org/#quickstart"""
import os
from typing import Protocol

import uvicorn
import asyncio

from starlette.types import ASGIApp, Scope, Receive, Send


async def echo(scope: Scope, receive: Receive, send: Send):
    """Simple showcase"""
    event = await receive()
    print(f"{scope = }\n{event = }")
    await send(
        {
            "type": "http.response.start",
            "status": 200,
            "headers": [[b"content-type", b"text/plain"]],
        }
    )
    await send(
        {
            "type": "http.response.body",
            "body": event.get("body", b""),
        }
    )


async def hello_world(scope: Scope, receive: Receive, send: Send):
    """Hello world app"""
    await send(
        {
            "type": "http.response.start",
            "status": 200,
            "headers": [[b"content-type", b"text/plain"]],
        }
    )
    await send(
        {
            "type": "http.response.body",
            "body": f"Hello, world! pid: {os.getpid()}".encode('utf-8'),
        }
    )
    # traceback.print_stack()


async def slow_body(scope: Scope, receive: Receive, send: Send):
    """
    Send a slowly streaming HTTP response back to the client.
    """
    await send(
        {
            "type": "http.response.start",
            "status": 200,
            "headers": [[b"content-type", b"text/plain"]],
        }
    )
    for chunk in (b"Slow", b", ", b"world!", f"{os.getpid()}".encode('utf-8')):
        await send({"type": "http.response.body", "body": chunk, "more_body": True})
        await asyncio.sleep(1)
    await send(
        {
            "type": "http.response.body",
            "body": b"",
        }
    )


async def app(scope: Scope, receive: Receive, send: Send):
    """
    So all the requirements to web framework is to define async function, which suits well for ASGIApp protocol.
    """
    assert scope["type"] == "http"
    if "slow" in scope["path"]:
        return await slow_body(scope, receive, send)
    return await hello_world(scope, receive, send)


app: ASGIApp


class ASGIAppProtocol(Protocol):
    """Common ASGI Protocol"""
    def __call__(self, scope: Scope, receive: Receive, send: Send):
        ...


if __name__ == "__main__":
    """
    TLDR: uvicorn creates server, handling requests according provided ASGIApp.
    
    The main goal of uvicorn is to run asyncio.get_running_loop().create_server() 
        with optimal and application's target oriented arguments.
        The most defining arg is protocol fabric function -
            on call it must return instance of child asyncio.Protocol class, which maintains application logic
    Resulting server is powerful enough to handle requests according transferred ASGIApp and handle errors
    All what is left for developer is 
        to provide async app function according ASGI protocol and choose suitable server options 
    
    Deeps on launch uvicorn.run():
    1) construct uvicorn.config.Config  # Just preparation and storing configs
    2) choose run strategy (Reload, Multiprocess, "simple")
    3) do uvicorn.server.Server.run  # launcher and target for Processes
    4) do uvicorn.server.Server.serve  #  launcher after loop preparation
    5) do uvicorn.config.Config.load:  # final preparation: load 3rd party and standart modules, setup middlewares
        a) load ssl
        b) import correct http_protocol_class, ws_protocol_class, lifespan_class
        c) import our app (loaded_app)
        d) middlewares installation into loaded_app
    6) do uvicorn.server.Server.startup  # MAIN LOGIC
        a) do lifespan.startup  # make loaded_app.__call__, sending {'type': 'lifespan.startup'}
        b) make fabric create_protocol and pass it into asyncio.get_running_loop().create_server()
        created protocol also contains our loaded_app and ws_protocol 
        
    On request, handled by h11_impl http protocol:
    1) asyncio.selector_events._SelectorSocketTransport._read_ready__data_received 
            -> self._protocol.data_received(data)                            # using protocol data handling logic
    2) uvicorn.protocols.http.h11_impl.RequestResponseCycle.run_asgi         # launch app
    3) uvicorn.middleware.proxy_headers.ProxyHeadersMiddleware.__call__      # launch middleware before app
    4) app =)                                                                # launch provided app(scope, receive, send)
    5) uvicorn.protocols.http.h11_impl.RequestResponseCycle.receive          # call send callable to receive event data
    6) uvicorn.protocols.http.h11_impl.RequestResponseCycle.send             # call send callable to send response
    """
    uvicorn.run(
        "__main__:echo",
        # "__main__:app",
        host="localhost",
        port=8000,
        # workers=3,
        # reload=True
    )
