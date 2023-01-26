from collections import defaultdict
from dataclasses import dataclass
from typing import Any

from pydantic import BaseModel, Extra


class FilterArgsMap(BaseModel, extra=Extra.forbid):
    eq_: list[tuple[str, Any]] | None = None
    lt_: list[tuple[str, Any]] | None = None
    le_: list[tuple[str, Any]] | None = None
    gt_: list[tuple[str, Any]] | None = None
    ge_: list[tuple[str, Any]] | None = None
    in_: list[tuple[str, list[Any]]] | None = None
    like_: list[tuple[str, Any]] | None = None


class FilterHandler:
    def __init__(self, filter_data: dataclass):
        self.args_map: dict[str, list[tuple[str, Any]]] = self.parse_filter_args(filter_data)

    @staticmethod
    def parse_filter_args(filter_data) -> dict[str, list[tuple[str, Any]]]:
        filter_args_map = defaultdict(list)
        for dataclass_field in filter_data.__dataclass_fields__:
            if value := getattr(filter_data, dataclass_field):
                field, filter_type = dataclass_field.split("__")
                filter_args_map[filter_type + "_"].append((field, value))
        return FilterArgsMap(**filter_args_map).dict(exclude_none=True)
