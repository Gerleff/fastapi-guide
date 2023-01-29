import operator
from typing import Any, Callable

from controller.dependencies.filters import FilterArgsMapEnum, filter_map_typing
from controller.dependencies.pagination import Pagination


def _like_operator_func(a: Any, b: Any) -> bool:
    return str(a).lower() in str(b).lower()


_filter_func_map: dict[FilterArgsMapEnum, Callable[[Any, Any], bool]] = {
    "eq_": operator.eq,
    "lt_": operator.lt,
    "le_": operator.le,
    "gt_": operator.gt,
    "ge_": operator.ge,
    "in_": operator.contains,
    "like_": _like_operator_func,
}


def filter_python_list(filter_map: filter_map_typing, python_list: list) -> list:
    new_list = python_list
    for filter_type, field_value_list_of_tuples in filter_map.items():
        check_list, new_list = new_list, []
        filter_func = _filter_func_map[filter_type]
        for elem in check_list:
            filtering_result = []
            for field, value in field_value_list_of_tuples:
                filter_func_result = filter_func(value, getattr(elem, field, None))
                filtering_result.append(filter_func_result)
            if all(filtering_result):
                new_list.append(elem)

    return new_list


def make_pagination_slice(pagination: Pagination) -> slice:
    return slice(pagination.offset, pagination.offset + pagination.limit)
