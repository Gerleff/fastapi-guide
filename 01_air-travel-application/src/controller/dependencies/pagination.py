from typing import NamedTuple


class Pagination(NamedTuple):
    limit: int = 10
    offset: int = 0

    @property
    def slice(self) -> slice:  # ToDo into Storage
        return slice(self.offset, self.offset + self.limit + 1)

    @property
    def sql(self) -> str:  # ToDo into Storage
        _expression = f"LIMIT {self.limit}"
        if self.offset:
            _expression += f" OFFSET {self.offset}"
        return _expression


def limit_offset_pagination(limit: int = 10, offset: int = 0) -> Pagination:
    return Pagination(limit=limit, offset=offset)


def page_size_pagination(page: int = 1, page_size: int = 10) -> Pagination:
    return Pagination(limit=page_size, offset=(page - 1) * page_size)
