from typing import TypeVar, Type, NoReturn, Protocol

from fastapi import Depends
from pydantic import BaseModel

from controller.dependencies.filter.base import FilterHandler
from controller.dependencies.pagination.base import Pagination
from models.storage.connection import get_db_connection

InputSchemaT = TypeVar("InputSchemaT", bound=Type[BaseModel])
UpdateSchemaT = TypeVar("UpdateSchemaT", bound=Type[BaseModel])
OutputSchemaT = TypeVar("OutputSchemaT", bound=Type[BaseModel])


class ModelProtocol(Protocol):
    id: int | None

    class Meta:
        table: str


ModelArgT = TypeVar("ModelArgT", bound=Type[ModelProtocol])


class DatabaseExecutorProtocol(Protocol):
    async def select(self, model: ModelArgT, _filter: FilterHandler, pagination: Pagination) -> list[...]:
        ...

    def select_by_id(self, model: ModelArgT, _id: int) -> ...:
        ...

    async def insert(self, model: ModelArgT, value: dict) -> ...:
        ...

    async def update(self, model: ModelArgT, _id: int, value: dict) -> ...:
        ...

    async def delete(self, model: ModelArgT, _id: int) -> bool:
        ...


class CRUDInterface:
    input_schema: InputSchemaT
    update_schema: UpdateSchemaT
    output_schema: OutputSchemaT

    def __init__(self, db_conn: DatabaseExecutorProtocol = Depends(get_db_connection)):
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
