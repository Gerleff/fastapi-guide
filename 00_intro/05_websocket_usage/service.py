from typing import NamedTuple

from pydantic import BaseModel, constr

STATUS_MAP = {
    "O": "Available",
    "$": "Ordered",
    "X": "Not available",
    "_": "Not exist",
}


class OrderError(Exception):
    ...


class AlreadyOrderedError(OrderError):
    def __init__(self, *args, **kwargs):
        super().__init__("Seat is already oredered!")


class NotFoundError(OrderError):
    def __init__(self, *args, **kwargs):
        super().__init__("Seat is not available")


class Row(NamedTuple):
    num: int
    seats: str


class SeatMapBlock(BaseModel):
    label: str
    literas: str
    rows_range: constr(regex=r"\d{,2}-\d{,2}")
    rows: list[Row]


def order_seat(seat_map: list[SeatMapBlock], seat: str):
    litera, row = seat[0], int(seat[1:])
    for block in seat_map:
        row_from, row_to = block.rows_range.split("-")
        if int(row_from) <= row <= int(row_to):
            for i, map_litera in enumerate(block.literas):
                if litera == map_litera:
                    for j, _row in enumerate(block.rows):
                        if _row.num == row:
                            if _row.seats[i] == "O":
                                new_row = _row.seats[:i] + "$" + _row.seats[i+1:]
                                block.rows[j] = Row(row, new_row)
                                return
                            if _row.seats[i] == "$":
                                raise AlreadyOrderedError()
    raise NotFoundError()


def generate_seat_map(print_map: bool = False):
    # Based on https://www.ana.co.jp/ru/ru/travel-information/seat-map/b787-10/
    seat_map = [
        SeatMapBlock(
            label="business_class",
            literas="ACDEFGHK",
            rows_range="1-10",
            rows=[
                Row(1, "OX____OX"),
                *(Row(_row, seats) for _row, seats in enumerate(["XOXOXOXO", "OXOXOXOX"] * 4, 2)),
                Row(10, "XOXOXOXO"),
            ]
        ),
        SeatMapBlock(
            label="premium_economy",
            literas="ACDFGHK",
            rows_range="15-18",
            rows=[Row(_row, "OOOOOOO") for _row in range(15, 18)]
        ),
        SeatMapBlock(
            label="economy_class",
            literas="ABCDFGHJK",
            rows_range="20-47",
            rows=[
                Row(20, "___OOO___"),
                *(Row(_row, "OOOOOOOOO") for _row in range(21, 31)),
                *(Row(_row, "OOO___OOO") for _row in range(31, 34)),
                *(Row(_row, "OOOOOOOOO") for _row in range(34, 47)),
                Row(47, "O_OOOOO_O"),
            ]
        )
    ]
    if print_map:
        for block in seat_map:
            print("=" * 10)
            print(block.label)
            print("x ", block.literas)
            for row in block.rows:
                print(row.num if row.num // 10 else f"0{row.num}", row.seats)
    return seat_map
