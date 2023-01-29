from controller.dependencies.filters import filter_map_typing, FilterArgsMapEnum
from controller.dependencies.pagination import Pagination

_sql_statement_map: dict[FilterArgsMapEnum, str] = {
    "eq_": "=",
    "lt_": "<",
    "le_": "<=",
    "gt_": ">",
    "ge_": ">=",
    "in_": "IN",  # TODO Check
    "like_": "ILIKE",  # TODO Check
}


def get_sql_from_filter_map(filter_map: filter_map_typing) -> str:
    if not filter_map:
        return ""
    _expressions = []
    for filter_type, field_value_list in filter_map.items():
        _operator = _sql_statement_map[filter_type]
        for field, value in field_value_list:
            _expressions.append(f"{field}{_operator}{value}")
    return " WHERE " + ",".join(_expressions)


def make_pagination_sql(pagination: Pagination) -> str:
    _expression = f"LIMIT {pagination.limit}"
    if pagination.offset:
        _expression += f" OFFSET {pagination.offset}"
    return _expression
