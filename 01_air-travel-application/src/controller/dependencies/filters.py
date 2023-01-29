from collections import defaultdict
from dataclasses import dataclass
from enum import Enum
from typing import Any, Protocol

from pydantic import BaseModel, Extra


class FilterMap(BaseModel, extra=Extra.forbid):
    eq_: list[tuple[str, Any]] | None = None
    lt_: list[tuple[str, Any]] | None = None
    le_: list[tuple[str, Any]] | None = None
    gt_: list[tuple[str, Any]] | None = None
    ge_: list[tuple[str, Any]] | None = None
    in_: list[tuple[str, list[Any]]] | None = None
    like_: list[tuple[str, Any]] | None = None


FilterArgsMapEnum = Enum.__call__("FilterArgsMapEnum", {field: field for field in FilterMap.__fields__}, type=str)
filter_map_typing = dict[FilterArgsMapEnum, list[tuple[str, Any]]]


class IsDataclass(Protocol):
    __dataclass_fields__: dict


@dataclass
class BaseFilter:
    # ToDO validate fields based on OutputSchema
    def make_filter_map(self: IsDataclass) -> filter_map_typing:
        filter_map = defaultdict(list)
        for dataclass_field in self.__dataclass_fields__:
            if value := getattr(self, dataclass_field):
                field, filter_type = dataclass_field.split("__")
                filter_map[filter_type + "_"].append((field, value))
        return FilterMap(**filter_map).dict(exclude_none=True)

    class Meta:
        schema = None
