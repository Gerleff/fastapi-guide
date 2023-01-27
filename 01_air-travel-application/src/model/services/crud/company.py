from typing import NoReturn

from controller.dependencies.filter.base import FilterHandler
from controller.dependencies.pagination.base import Pagination
from model.db_entities.models import CompanyModel
from model.services.crud.base import CRUDInterface
from model.services.dto import CompanyDTO


class CompanyCRUD(CRUDInterface):
    async def create(self, data: dict) -> CompanyDTO:
        return CompanyDTO.from_database(await self.db_conn.insert(CompanyModel, data))

    async def read(self, _filter: FilterHandler, pagination: Pagination) -> list[CompanyDTO]:
        return [CompanyDTO.from_database(row) for row in await self.db_conn.select(CompanyModel, _filter, pagination)]

    async def read_by_id(self, _id: int) -> CompanyDTO:
        return CompanyDTO.from_database(await self.db_conn.select_by_id(CompanyModel, _id))

    async def update_by_id(self, _id: int, data: dict) -> CompanyDTO:
        return CompanyDTO.from_database(await self.db_conn.update_by_id(CompanyModel, _id, data))

    async def delete_by_id(self, _id: int) -> NoReturn:
        await self.db_conn.delete_by_id(CompanyModel, _id)
