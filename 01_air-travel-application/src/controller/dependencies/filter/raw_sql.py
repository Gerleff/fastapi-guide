from controller.dependencies.filter.base import FilterHandler


class RawSQLFilterHandler(FilterHandler):
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
            "like_": "ILIKE",  # TODO Check
        }
        _expressions = []
        for filter_type, field_value_list in self.args_map.items():
            _operator = _stmt_map[filter_type]
            for field, value in field_value_list:
                if value is not None:
                    _expressions.append(f"{field}{_operator}{value}")
        return " WHERE " + ",".join(_expressions)
