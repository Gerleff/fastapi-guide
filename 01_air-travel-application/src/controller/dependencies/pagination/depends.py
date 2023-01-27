from typing import Type

from fastapi import Depends

from .base import Pagination
from .pythonic import PythonicPagination
from .raw_sql import RawSQLPagination
from config.settings import get_settings


def get_pagination_class():
    match get_settings().database_type:
        case "pythonic_storage":
            return PythonicPagination
        case "sqlite":
            return RawSQLPagination
        case _:
            raise NotImplementedError


def limit_offset_pagination(
    limit: int = 10, offset: int = 0, pagination_cls: Type[Pagination] = Depends(get_pagination_class)
) -> Pagination:
    return pagination_cls(limit=limit, offset=offset)


def page_size_pagination(
    page: int = 1, page_size: int = 10, pagination_cls: Type[Pagination] = Depends(get_pagination_class)
) -> Pagination:
    return pagination_cls(limit=page_size, offset=(page - 1) * page_size)
