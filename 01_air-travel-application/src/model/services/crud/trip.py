from typing import NoReturn

from controller.dependencies.filters import filter_map_typing
from controller.dependencies.pagination import Pagination
from model.db_entities.models import CompanyModel, TripModel
from model.services.crud.base import CRUDInterface
from model.services.dto import TripDTO


class TripCRUD(CRUDInterface):
    async def _get_company(self, company_id: int) -> CompanyModel:
        return await self.db_conn.select_by_id(CompanyModel, company_id)

    async def create(self, data: dict) -> TripDTO:
        company = await self._get_company(data["company"])
        inserted_trip = await self.db_conn.insert(TripModel, data)
        return TripDTO.from_database(inserted_trip, company)

    async def read(self, filter_map: filter_map_typing, pagination: Pagination) -> list[TripDTO]:
        result = []
        for trip in await self.db_conn.select(TripModel, filter_map, pagination):
            result.append(TripDTO.from_database(trip, await self._get_company(trip.company)))
        return result

    async def read_by_id(self, _id: int) -> TripDTO:
        trip = await self.db_conn.select_by_id(TripModel, _id)
        return TripDTO.from_database(trip, await self._get_company(trip.company))

    async def update_by_id(self, _id: int, data: dict) -> TripDTO:
        company = await self._get_company(data["company"]) if data.get("company") else None
        trip = await self.db_conn.update_by_id(TripModel, _id, data)
        return TripDTO.from_database(trip, company or await self._get_company(trip.company))

    async def delete_by_id(self, _id: int) -> NoReturn:
        await self.db_conn.delete_by_id(TripModel, _id)
