from typing import TypeVar, Type, NoReturn

from pydantic import BaseModel

from controller.dependencies.pagination import Pagination


InputSchemaT = TypeVar("InputSchemaT", bound=Type[BaseModel])
UpdateSchemaT = TypeVar("UpdateSchemaT", bound=Type[BaseModel])
OutputSchemaT = TypeVar("OutputSchemaT", bound=Type[BaseModel])


class CRUDInterface:
    input_schema: InputSchemaT
    update_schema: UpdateSchemaT
    output_schema: OutputSchemaT

    def __init__(self, storage):  # ToDO inject storage
        self.storage = storage

    async def create(self, data: "input_schema") -> "output_schema":
        ...

    async def read(self, _filter, pagination: Pagination) -> list["output_schema"]:
        ...

    async def read_by_id(self, _id: int) -> "output_schema":
        ...

    async def update_by_id(self, _id: int, data: "update_schema") -> "output_schema":
        ...

    async def delete_by_id(self, _id: int) -> NoReturn:
        ...
