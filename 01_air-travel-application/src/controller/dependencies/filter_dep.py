import operator
from collections import defaultdict
from typing import Iterable, Any, Callable

from fastapi import Depends
from pydantic import BaseModel, Extra


class FilterArgsMap(BaseModel, extra=Extra.forbid):
    _eq: list[tuple[str, Any]] | None = None
    _lt: list[tuple[str, Any]] | None = None
    _le: list[tuple[str, Any]] | None = None
    _gt: list[tuple[str, Any]] | None = None
    _ge: list[tuple[str, Any]] | None = None
    _in: list[tuple[str, Iterable]] | None = None


class FilterHandler:
    def __init__(self, filter_data):
        self.args_map: dict[str, list[tuple[str, Any]]] = self.parse_filter_args(filter_data)

    @staticmethod
    def parse_filter_args(filter_data) -> dict[str, list[tuple[str, Any]]]:
        filter_args_map = defaultdict(list)
        for dataclass_field in filter_data.__dataclass_fields__:
            if value := getattr(filter_data, dataclass_field):
                field, filter_type = filter_data.dataclass_field.split("__")
                filter_args_map["_" + filter_type].append((field, value))
        return FilterArgsMap.parse_obj(filter_args_map).dict(exclude_none=True)

    def filter_python_list(self, python_list: list) -> list:
        _func_map: dict[str, Callable[[Any, Any], bool]] = {
            "_eq": operator.eq,
            "_lt": operator.lt,
            "_le": operator.le,
            "_gt": operator.gt,
            "_ge": operator.ge,
            "_in": operator.contains,  # note reversed args
        }

        for filter_type, field_value_list in self.args_map.items():
            filter_func = _func_map[filter_type]
            python_list[:] = [
                elem
                for elem in python_list
                if all(
                    tuple(
                        filter_func(value, getattr(elem, field, None))
                        for field, value in field_value_list
                        if value is not None
                    )
                )
            ]
        return python_list

    @property
    def sql(self) -> str:
        if not self.args_map:
            return ""
        _expressions = []
        _stmt_map: dict[str, str] = {
            "_eq": "=",
            "_lt": "<",
            "_le": "<=",
            "_gt": ">",
            "_ge": ">=",
            "_in": "IN",  # TODO Check
        }
        for filter_type, field_value_list in self.args_map.items():
            _operator = _stmt_map[filter_type]
            for field, value in field_value_list:
                if value is not None:
                    _expressions.append(f"{field}{_operator}{value}")
        return " WHERE " + ",".join(_expressions)


def make_filter_dependancy(filter_dataclass):
    def filter_dependency(_filter: filter_dataclass = Depends()) -> FilterHandler:
        return FilterHandler(_filter)
    return filter_dependency
