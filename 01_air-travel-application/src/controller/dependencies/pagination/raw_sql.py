from controller.dependencies.pagination.base import Pagination


class RawSQLPagination(Pagination):
    @property
    def sql(self) -> str:
        _expression = f"LIMIT {self.limit}"
        if self.offset:
            _expression += f" OFFSET {self.offset}"
        return _expression
