from typing import NoReturn

from controller.dependencies.filters import filter_map_typing
from controller.dependencies.pagination import Pagination
from model.db_entities.models import CompanyModel, TripModel, PassInTripModel
from model.services.crud.base import CRUDInterface
from model.services.dto import TicketDTO


class TicketCRUD(CRUDInterface):
    async def _get_company(self, company_id: int) -> CompanyModel:
        return await self.db_conn.select_by_id(CompanyModel, company_id)

    async def _get_trip(self, trip_id: int) -> TripModel:
        return await self.db_conn.select_by_id(TripModel, trip_id)

    async def create(self, data: dict) -> TicketDTO:
        trip = await self._get_trip(data["trip"])
        company = await self._get_company(trip.company)
        # ToDO user
        inserted_ticket = await self.db_conn.insert(PassInTripModel, data)
        return TicketDTO.from_database(inserted_ticket, trip, company)

    async def read(self, filter_map: filter_map_typing, pagination: Pagination) -> list[TicketDTO]:
        result = []
        for ticket in await self.db_conn.select(PassInTripModel, filter_map, pagination):
            result.append(
                TicketDTO.from_database(
                    ticket, trip := await self._get_trip(ticket.trip), await self._get_company(trip.company)
                )
            )
        return result

    async def read_by_id(self, _id: int) -> TicketDTO:
        ticket = await self.db_conn.select_by_id(PassInTripModel, _id)
        return TicketDTO.from_database(
            ticket, trip := await self._get_trip(ticket.trip), await self._get_company(trip.company)
        )

    async def update_by_id(self, _id: int, data: dict) -> TicketDTO:
        trip = await self._get_trip(data["trip"]) if data.get("trip") else None
        # ToDO user
        # user = await self._get_trip(data["user"]) if data.get("user") else None
        ticket = await self.db_conn.update_by_id(PassInTripModel, _id, data)
        if not trip:
            trip = await self.db_conn.select_by_id(TripModel, ticket.trip)
        company = await self.db_conn.select_by_id(CompanyModel, trip.company)
        return TicketDTO.from_database(ticket, trip, company)

    async def delete_by_id(self, _id: int) -> NoReturn:
        await self.db_conn.delete_by_id(PassInTripModel, _id)
