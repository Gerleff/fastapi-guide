from typing import NamedTuple


class Pagination(NamedTuple):
    limit: int = 10
    offset: int = 0

    @property
    def sql(self) -> str:  # ToDo into Storage
        _expression = f"LIMIT {self.limit}"
        if self.offset:
            _expression += f" OFFSET {self.offset}"
        return _expression
