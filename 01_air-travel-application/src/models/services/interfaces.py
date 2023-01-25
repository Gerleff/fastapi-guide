from typing import TypeVar, Type, NoReturn

from fastapi import Depends
from pydantic import BaseModel

from controller.dependencies.filter_dep import FilterHandler
from controller.dependencies.pagination import Pagination
from models.storage.dependencies import get_db_connection
from models.storage.protocol import DatabaseProtocol

InputSchemaT = TypeVar("InputSchemaT", bound=Type[BaseModel])
UpdateSchemaT = TypeVar("UpdateSchemaT", bound=Type[BaseModel])
OutputSchemaT = TypeVar("OutputSchemaT", bound=Type[BaseModel])


class CRUDInterface:
    input_schema: InputSchemaT
    update_schema: UpdateSchemaT
    output_schema: OutputSchemaT

    def __init__(self, db_conn: DatabaseProtocol = Depends(get_db_connection)):  # ToDO inject db_conn
        self.db_conn = db_conn

    async def create(self, data: "input_schema") -> "output_schema":
        raise NotImplementedError

    async def read(self, _filter: FilterHandler, pagination: Pagination) -> list["output_schema"]:
        raise NotImplementedError

    async def read_by_id(self, _id: int) -> "output_schema":
        raise NotImplementedError

    async def update_by_id(self, _id: int, data: "update_schema") -> "output_schema":
        raise NotImplementedError

    async def delete_by_id(self, _id: int) -> NoReturn:
        raise NotImplementedError
