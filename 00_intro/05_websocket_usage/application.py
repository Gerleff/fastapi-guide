import asyncio
from asyncio import Queue
from collections import defaultdict
from contextlib import suppress
from pathlib import Path

import uvicorn
from fastapi import FastAPI, WebSocket
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from starlette.staticfiles import StaticFiles
from starlette.websockets import WebSocketDisconnect

from service import generate_seat_map, order_seat, OrderError
from settings import settings
from simple_queue import AsyncFanoutQueue

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory=Path("templates"))


@app.on_event("startup")
def start_up():
    seat_maps = defaultdict(generate_seat_map)
    app.state.seat_maps = seat_maps

    app.state.queue = AsyncFanoutQueue()
    app.state.running = True


@app.on_event("shutdown")
def shut_down():
    app.state.running = False


@app.get("/trips/{_id}")
async def get_trip(request: Request, _id: int):
    seat_map = request.app.state.seat_maps[_id]
    return templates.TemplateResponse(
        "seat_map.html", {"request": request, "id": _id, "settings": settings, "seat_map": seat_map}
    )


@app.websocket("/ws/{trip_id}")
async def ep_websocket(trip_id: int, websocket: WebSocket):
    """websocket"""
    closed = False

    await websocket.accept()
    fanout_queue: AsyncFanoutQueue = app.state.queue
    queue: Queue = fanout_queue.register()

    async def wait_queue():
        while True:
            queue_message = await queue.get()
            if queue_message["type"] == "finish":
                break
            if queue_message.get("trip_id") == trip_id:
                await websocket.send_json(queue_message)
        for task in queue._queue:
            task.cancel()

    asyncio.create_task(wait_queue())
    try:
        while websocket.app.state.running:
            message = await websocket.receive_json()
            if message["type"] == "order":
                try:
                    order_seat(websocket.app.state.seat_maps[trip_id], message["seat"])
                except OrderError as error:
                    await websocket.send_json({"type": "error", "descr": str(error)})
                else:
                    await fanout_queue.multicast({"type": "order", "seat": message["seat"], "trip_id": trip_id})
    except WebSocketDisconnect:
        closed = True

    if not closed:
        await websocket.close()
    await fanout_queue.unregister(queue)


if __name__ == "__main__":
    print(generate_seat_map(print_map=True))
    uvicorn.run("__main__:app", host="localhost", port=8000, reload=True)
