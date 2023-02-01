"""Inspired by https://www.uvicorn.org/#quickstart"""
import os

import uvicorn
import asyncio

from starlette.types import ASGIApp, Scope, Receive, Send


async def hello_world(scope: Scope, receive: Receive, send: Send):
    """Simple showcase with pid"""
    event = await receive()
    print(f"{scope = }\n{event = }")
    await send(
        {
            "type": "http.response.start",
            "status": 200,
            "headers": [
                [b"content-type", b"text/plain"],
            ],
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
            "headers": [
                [b"content-type", b"text/plain"],
            ],
        }
    )
    for chunk in (b"Slow", b", ", b"world!"):
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


if __name__ == "__main__":
    """
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
        c) tick
        
    On request, handled by h11_impl http protocol:
    7) asyncio.selector_events._SelectorSocketTransport._read_ready__data_received -> self._protocol.data_received(data)
    8) uvicorn.protocols.http.h11_impl.RequestResponseCycle.run_asgi
    9) uvicorn.middleware.proxy_headers.ProxyHeadersMiddleware.__call__
    10) app =)
    """
    uvicorn.run(
        "__main__:app",
        host="localhost",
        port=8000,
        workers=3,
        # reload=True
    )
