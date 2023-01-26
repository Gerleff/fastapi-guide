from controller.dependencies.filter_dep import FilterHandler
from .interfaces import CRUDInterface
from typing import NoReturn

from controller.dependencies.pagination import Pagination
from ..database.models import CompanyModel, TripModel, PassInTripModel, UserModel
from ..schemas.input import (
    CompanyInputSchema,
    CompanyUpdateSchema,
    TripInputSchema,
    TripUpdateSchema,
    TicketInputSchema,
    TicketUpdateSchema,
)
from ..schemas.output import CompanyOutputSchema, TripOutputSchema, TicketOutputSchema


class NotFoundError(BaseException):
    message = None
    message_format = "Entity with id {} is not found in table {}"

    def __init_(self, table: str, _id: int):
        self.message = self.message_format.format(_id, table)


class CompanyCRUD(CRUDInterface):
    input_schema = CompanyInputSchema
    update_schema = CompanyUpdateSchema
    output_schema = CompanyOutputSchema

    async def create(self, data: CompanyInputSchema) -> CompanyOutputSchema:
        return await self.db_conn.insert(CompanyModel, data.dict())

    async def read(self, _filter: FilterHandler, pagination: Pagination) -> list[CompanyOutputSchema]:
        return await self.db_conn.select(CompanyModel, _filter, pagination)

    async def read_by_id(self, _id: int) -> CompanyOutputSchema:
        if result := await self.db_conn.select_by_id(CompanyModel, _id):
            return result
        else:
            raise NotFoundError(CompanyModel, _id)

    async def update_by_id(self, _id: int, data: CompanyUpdateSchema) -> CompanyOutputSchema:
        if result := await self.db_conn.update(CompanyModel, _id, data.dict()):
            return result
        else:
            raise NotFoundError(CompanyModel, _id)

    async def delete_by_id(self, _id: int) -> NoReturn:
        if not await self.db_conn.delete(CompanyModel, _id):
            raise NotFoundError(CompanyModel, _id)


class TripCRUD(CRUDInterface):
    input_schema = TripInputSchema
    update_schema = TripUpdateSchema
    output_schema = TripOutputSchema

    async def _get_company(self, company_id: int) -> CompanyModel:
        if not (trip_company := await self.db_conn.select_by_id(CompanyModel, company_id)):
            raise NotFoundError(CompanyModel, company_id)
        return trip_company

    def _serialize_output(self, trip: TripModel, company: CompanyModel) -> TripOutputSchema:
        return self.output_schema(company=company, **trip.dict(exclude={"company"}))

    async def create(self, data: TripInputSchema) -> TripOutputSchema:
        trip_company = await self._get_company(data.company)
        inserted_trip = await self.db_conn.insert(TripModel, data.dict())
        return self._serialize_output(inserted_trip, trip_company)

    async def read(self, _filter: FilterHandler, pagination: Pagination) -> list[TripOutputSchema]:
        result = []
        for trip in await self.db_conn.select(TripModel, _filter, pagination):
            result.append(self._serialize_output(trip, await self._get_company(trip.company)))
        return result

    async def read_by_id(self, _id: int) -> TripOutputSchema:
        if not (trip := await self.db_conn.select_by_id(TripModel, _id)):
            raise NotFoundError(TripModel, _id)
        company = await self._get_company(trip.company)
        return self._serialize_output(trip, company)

    async def update_by_id(self, _id: int, data: TripUpdateSchema) -> TripOutputSchema:
        await self._get_company(data.company)
        if result := await self.db_conn.update(TripModel, _id, data.dict()):
            return result
        else:
            raise NotFoundError(TripModel, _id)

    async def delete_by_id(self, _id: int) -> NoReturn:
        if not await self.db_conn.delete(TripModel, _id):
            raise NotFoundError(TripModel, _id)


class TicketCRUD(CRUDInterface):
    input_schema = CompanyInputSchema
    update_schema = CompanyUpdateSchema
    output_schema = CompanyOutputSchema

    async def create(self, data: CompanyInputSchema) -> CompanyOutputSchema:
        return await self.db_conn.insert(PassInTripModel, data.dict())

    async def read(self, _filter: FilterHandler, pagination: Pagination) -> list[CompanyOutputSchema]:
        return await self.db_conn.select(PassInTripModel, _filter, pagination)

    async def read_by_id(self, _id: int) -> CompanyOutputSchema:
        return (await self.db_conn.select_by_id(PassInTripModel, _id))[0]

    async def update_by_id(self, _id: int, data: CompanyUpdateSchema) -> CompanyOutputSchema:
        return await self.db_conn.update(PassInTripModel, _id, data.dict())

    async def delete_by_id(self, _id: int) -> NoReturn:
        await self.db_conn.delete(PassInTripModel, _id)


class UserCRUD(CRUDInterface):
    input_schema = TicketInputSchema
    update_schema = TicketUpdateSchema
    output_schema = TicketOutputSchema

    async def create(self, data: TicketInputSchema) -> TicketOutputSchema:
        return await self.db_conn.insert(UserModel, data.dict())

    async def read(self, _filter: FilterHandler, pagination: Pagination) -> list[TicketOutputSchema]:
        return await self.db_conn.select(UserModel, _filter, pagination)

    async def read_by_id(self, _id: int) -> TicketOutputSchema:
        return (await self.db_conn.select_by_id(UserModel, _id))[0]

    async def update_by_id(self, _id: int, data: TicketUpdateSchema) -> TicketOutputSchema:
        return await self.db_conn.update(UserModel, _id, data.dict())

    async def delete_by_id(self, _id: int) -> NoReturn:
        await self.db_conn.delete(UserModel, _id)
