from .interfaces import CRUDInterface
from typing import NoReturn

from controller.dependencies.pagination import Pagination
from ..schemas.input import CompanyInputSchema, CompanyUpdateSchema
from ..schemas.output import CompanyOutputSchema


class CompanyCRUD(CRUDInterface):
    input_schema = CompanyInputSchema
    update_schema = CompanyUpdateSchema
    output_schema = CompanyOutputSchema

    async def create(self, data: "input_schema") -> "output_schema":
        await self.storage.insert(data.dict())

    async def read(self, _filter, pagination: Pagination) -> list["output_schema"]:
        return await self.storage.filter(_filter, pagination)

    async def read_by_id(self, _id: int) -> "output_schema":
        return await self.storage.select(_id)

    async def update_by_id(self, _id: int, data: "update_schema") -> "output_schema":
        return await self.storage.update(_id, data)

    async def delete_by_id(self, _id: int) -> NoReturn:
        await self.storage.delete(_id)
