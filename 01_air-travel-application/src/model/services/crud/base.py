from typing import NoReturn

from fastapi import Depends

from controller.dependencies.filters import filter_map_typing
from controller.dependencies.pagination import Pagination
from model.services.dto import BaseDTO
from model.storage.base import BaseDatabaseHandler
from model.storage.connection import get_db_connection


class CRUDInterface:
    def __init__(self, db_conn: BaseDatabaseHandler = Depends(get_db_connection)):
        self.db_conn = db_conn

    async def create(self, data: dict) -> BaseDTO:
        raise NotImplementedError

    async def read(self, filter_map: filter_map_typing, pagination: Pagination) -> list[BaseDTO]:
        raise NotImplementedError

    async def read_by_id(self, _id: int) -> BaseDTO:
        raise NotImplementedError

    async def update_by_id(self, _id: int, data: dict) -> BaseDTO:
        raise NotImplementedError

    async def delete_by_id(self, _id: int) -> NoReturn:
        raise NotImplementedError
