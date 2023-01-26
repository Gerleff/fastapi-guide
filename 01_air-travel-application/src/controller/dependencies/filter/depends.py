from typing import Type

from fastapi import Depends

from models.storage.connection import DBSettingsProtocol
from settings import get_settings
from .base import FilterHandler
from .pythonic import PythonicFilterHandler
from .raw_sql import RawSQLFilterHandler


def get_filter_handler_class():
    settings: DBSettingsProtocol
    match get_settings().database_type:
        case "pythonic_storage":
            return PythonicFilterHandler
        case "sqlite":
            return RawSQLFilterHandler
        case _:
            raise NotImplementedError


def make_filter_dependency(filter_dataclass):
    def filter_dependency(
        _filter: filter_dataclass = Depends(), filter_cls: Type[FilterHandler] = Depends(get_filter_handler_class)
    ) -> FilterHandler:
        return filter_cls(_filter)

    return filter_dependency
