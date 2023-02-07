from typing import NamedTuple

import uvicorn
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from pydantic import constr
from starlette.websockets import WebSocketDisconnect


STATUS_MAP = {
    "O": "Available",
    "$": "Ordered",
    "X": "Not available",
    "_": "Not exist",
}


class Row(NamedTuple):
    num: int
    seats: str


def generate_seat_map():
    # Based on https://www.ana.co.jp/ru/ru/travel-information/seat-map/b787-10/
    literas = "ABCDEFGHJK"
    eazy_print_map = {
        "business_class": [
            Row(1, "O_X____O_X"),
            *(Row(_row, seats) for _row, seats in enumerate(["X_OXOXOX_O", "O_XOXOXO_X"] * 4, 2)),
            Row(10, "X_OXOXOX_O"),
        ],
        "premium_economy": [Row(_row, "O_OO_OOO_O") for _row in range(15, 18)],
        "economy_class": [
            Row(20, "___O_OO___"),
            *(Row(_row, "OOOO_OOOOO") for _row in range(21, 31)),
            *(Row(_row, "OOO____OOO") for _row in range(31, 34)),
            *(Row(_row, "OOOO_OOOOO") for _row in range(34, 47)),
            Row(47, "O_OO_OOO_O"),
        ]
    }
    print(literas)
    for rank, rows in eazy_print_map.items():
        print(rank)
        for row in rows:
            print(row.num, row.seats)
    initial_seat_map = {}
    for rank, rows in eazy_print_map.items():
        for row in rows:
            for i, seat in enumerate(row.seats):
                if (status := STATUS_MAP[seat]) in ("Not available", "Not exist"):
                    continue
                initial_seat_map[f"{literas[i]}{row.num}"] = {"rank": rank, "status": status}
    return initial_seat_map


app = FastAPI()


@app.on_event("startup")
def start_up():
    seat_map = {}
    app.state.seat_map = seat_map
    app.state.running = True


@app.on_event("shutdown")
def shut_down():
    app.state.running = False


html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8000/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@app.get("/")
async def get():
    return HTMLResponse(html)


# @app.websocket("/ws")
# async def ep_websocket(websocket: WebSocket):
#     """websocket"""
#     closed = False
#
#     await websocket.accept()
#     try:
#         while websocket.app.state.running:
#             message = await websocket.receive_json()
#
#             if message.get('event', None) == 'auth':
#                 auth_data = message.get('data', None)
#                 user = get_user(auth_data)
#
#                 if user.role == ConstUserRole.anonymous:
#                     await websocket.send_text(json.dumps({'event': 'auth', 'data': 'Auth fail'}))
#                     continue
#
#                 await websocket.send_text(json.dumps({'event': 'auth', 'data': 'Auth ok'}))
#                 add_message_handler(handler)
#     except WebSocketDisconnect:
#         closed = True
#
#     if not closed:
#         await websocket.close()


if __name__ == "__main__":
    print(generate_seat_map())
    # uvicorn.run("__main__:app", host="localhost", port=8000, reload=True)
