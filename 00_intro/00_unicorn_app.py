"""From https://www.uvicorn.org/#quickstart"""
import traceback
import uvicorn
import asyncio


async def hello_world(scope, receive, send):
    """Simple showcase"""
    event = await receive()
    print(f"{scope = }\n{event = }")
    await send({
        'type': 'http.response.start',
        'status': 200,
        'headers': [
            [b'content-type', b'text/plain'],
        ],
    })
    await send({
        'type': 'http.response.body',
        'body': b'Hello, world!',
    })
    traceback.print_stack()


async def slow_body(scope, receive, send):
    """
    Send a slowly streaming HTTP response back to the client.
    """
    await send({
        'type': 'http.response.start',
        'status': 200,
        'headers': [
            [b'content-type', b'text/plain'],
        ]
    })
    for chunk in (b'Slow', b', ', b'world!'):
        await send({
            'type': 'http.response.body',
            'body': chunk,
            'more_body': True
        })
        await asyncio.sleep(1)
    await send({
        'type': 'http.response.body',
        'body': b'',
    })


async def app(scope, receive, send):
    assert scope['type'] == 'http'
    if "slow" in scope["path"]:
        return await slow_body(scope, receive, send)
    return await hello_world(scope, receive, send)

if __name__ == "__main__":
    uvicorn.run("__main__:app", host="localhost", port=8000, reload=True)