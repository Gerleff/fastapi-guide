from typing import Type, Any

from controller.dependencies.filters import filter_map_typing, FilterArgsMapEnum
from controller.dependencies.pagination import Pagination
from model.storage.base import ModelVar

_sql_statement_map: dict[FilterArgsMapEnum, str] = {
    "eq_": "=",
    "lt_": "<",
    "le_": "<=",
    "gt_": ">",
    "ge_": ">=",
    "in_": "IN",
    "like_": "LIKE",
}


def _adapt_value(filter_type: FilterArgsMapEnum, value: Any) -> str:
    match filter_type:
        case FilterArgsMapEnum.in_:
            list_value = ", ".join(tuple(f"\"{element}\"" for element in value))
            return f"({list_value})"
        case FilterArgsMapEnum.like_:
            return f"\"%{value}%\""
        case _:
            return f"\"{value}\""


def make_sql_from_filter_map(filter_map: filter_map_typing) -> str:
    if not filter_map:
        return ""
    _expressions = []
    for filter_type, field_value_list in filter_map.items():
        _operator = _sql_statement_map[filter_type]
        for field, value in field_value_list:
            _expressions.append(f"{field} {_operator} {_adapt_value(filter_type, value)}")
    return " WHERE " + "AND ".join(_expressions)


def make_pagination_sql(pagination: Pagination) -> str:
    _expression = f" LIMIT {pagination.limit}"
    if pagination.offset:
        _expression += f" OFFSET {pagination.offset}"
    return _expression


def parse_db_record_into_model(record: tuple, model: Type[ModelVar]) -> ModelVar:
    return model.parse_obj(zip(model.__fields__, record))
