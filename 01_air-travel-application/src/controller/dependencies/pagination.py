from typing import NamedTuple


class Pagination(NamedTuple):
    limit: int = 10
    offset: int = 0


one_elem = Pagination(1, 0)


def limit_offset_pagination(limit: int = 10, offset: int = 0) -> Pagination:
    return Pagination(limit=limit, offset=offset)


def page_size_pagination(page: int = 1, page_size: int = 10) -> Pagination:
    return Pagination(limit=page_size, offset=(page - 1) * page_size)
