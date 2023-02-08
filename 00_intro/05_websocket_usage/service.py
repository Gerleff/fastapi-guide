from collections import defaultdict
from typing import NamedTuple


STATUS_MAP = {
    "O": "Available",
    "$": "Ordered",
    "X": "Not available",
    "_": "Not exist",
}


class Row(NamedTuple):
    num: int
    seats: str


def generate_seat_map(print_map: bool = False):
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
    if print_map:
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
                seat_num = f"{literas[i]}{row.num}"
                initial_seat_map[seat_num] = {"rank": rank, "status": status, "id": seat_num}
    return {"seat_map": initial_seat_map, "literas": literas}


def parse_seat_map(seat_map: dict):
    literas, rows = list(seat_map["literas"]), defaultdict(lambda: [None] * len(literas))
    for seat, data in seat_map["seat_map"].items():
        litera, row = seat[0], seat[1:]
        rows[row][literas.index(litera)] = data

    return {"literas": literas, "rows": rows}
