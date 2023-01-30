from typing import NoReturn

from controller.dependencies.filters import filter_map_typing
from controller.dependencies.pagination import Pagination
from model.db_entities.models import CompanyModel
from model.services.crud.base import CRUDInterface
from model.services.dto import CompanyDTO


class CompanyCRUD(CRUDInterface):
    async def create(self, data: dict) -> CompanyDTO:
        return CompanyDTO.from_database(await self.db_conn.insert(CompanyModel, data))

    async def read(self, filter_map: filter_map_typing, pagination: Pagination) -> list[CompanyDTO]:
        return [
            CompanyDTO.from_database(row) for row in await self.db_conn.select(CompanyModel, filter_map, pagination)
        ]

    async def read_by_id(self, _id: int) -> CompanyDTO:
        return CompanyDTO.from_database(await self.db_conn.select_by_id(CompanyModel, _id))

    async def update_by_id(self, _id: int, data: dict) -> CompanyDTO:
        return CompanyDTO.from_database(await self.db_conn.update_by_id(CompanyModel, _id, data))

    async def delete_by_id(self, _id: int) -> NoReturn:
        await self.db_conn.delete_by_id(CompanyModel, _id)
