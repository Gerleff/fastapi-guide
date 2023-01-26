import operator
from typing import Callable, Any

from .base import FilterHandler


def _like_operator_func(a, b):
    return str(a).lower() in str(b).lower()


_func_map: dict[str, Callable[[Any, Any], bool]] = {
    "eq_": operator.eq,
    "lt_": operator.lt,
    "le_": operator.le,
    "gt_": operator.gt,
    "ge_": operator.ge,
    "in_": operator.contains,
    "like_": _like_operator_func,
}


class PythonicFilterHandler(FilterHandler):
    def filter_python_list(self, python_list: list) -> list:
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
