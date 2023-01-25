from controller.dependencies.filter_dep import FilterHandler
from .interfaces import CRUDInterface
from typing import NoReturn

from controller.dependencies.pagination import Pagination
from ..database.models import CompanyModel
from ..schemas.input import CompanyInputSchema, CompanyUpdateSchema
from ..schemas.output import CompanyOutputSchema


class CompanyCRUD(CRUDInterface):
    input_schema = CompanyInputSchema
    update_schema = CompanyUpdateSchema
    output_schema = CompanyOutputSchema

    async def create(self, data: CompanyInputSchema) -> CompanyOutputSchema:
        return await self.db_conn.insert(CompanyModel, data.dict())

    async def read(self, _filter: FilterHandler, pagination: Pagination) -> list[CompanyOutputSchema]:
        return await self.db_conn.select(CompanyModel, _filter, pagination)

    async def read_by_id(self, _id: int) -> CompanyOutputSchema:
        return (await self.db_conn.select_by_id(CompanyModel, _id))[0]

    async def update_by_id(self, _id: int, data: CompanyUpdateSchema) -> CompanyOutputSchema:
        return await self.db_conn.update(CompanyModel, _id, data)

    async def delete_by_id(self, _id: int) -> NoReturn:
        await self.db_conn.delete(CompanyModel, _id)
