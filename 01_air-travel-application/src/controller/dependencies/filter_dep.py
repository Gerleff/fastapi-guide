import operator
from collections import defaultdict
from typing import Any, Callable

from fastapi import Depends
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
    def __init__(self, filter_data):
        self.args_map: dict[str, list[tuple[str, Any]]] = self.parse_filter_args(filter_data)

    @staticmethod
    def parse_filter_args(filter_data) -> dict[str, list[tuple[str, Any]]]:
        filter_args_map = defaultdict(list)
        for dataclass_field in filter_data.__dataclass_fields__:
            if value := getattr(filter_data, dataclass_field):
                field, filter_type = dataclass_field.split("__")
                filter_args_map[filter_type + "_"].append((field, value))
        return FilterArgsMap(**filter_args_map).dict(exclude_none=True)

    def filter_python_list(self, python_list: list) -> list:
        def like_func(a, b):
            return str(a).lower() in str(b).lower()
        _func_map: dict[str, Callable[[Any, Any], bool]] = {
            "eq_": operator.eq,
            "lt_": operator.lt,
            "le_": operator.le,
            "gt_": operator.gt,
            "ge_": operator.ge,
            "in_": operator.contains,
            "like_": like_func
        }
        new_list = python_list
        for filter_type, field_value_list_of_tuples in self.args_map.items():
            check_list, new_list = new_list, []
            filter_func = _func_map[filter_type]
            for elem in check_list:
                filtering_result = []
                for field, value in field_value_list_of_tuples:
                    filter_func_result = filter_func(value, getattr(elem, field, None))
                    filtering_result.append(filter_func_result)
                if all(filtering_result):
                    new_list.append(elem)

        return new_list

    @property
    def sql(self) -> str:
        if not self.args_map:
            return ""
        _stmt_map: dict[str, str] = {
            "eq_": "=",
            "lt_": "<",
            "le_": "<=",
            "gt_": ">",
            "ge_": ">=",
            "in_": "IN",  # TODO Check
            "like_": "ILIKE"  # TODO Check
        }
        _expressions = []
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
