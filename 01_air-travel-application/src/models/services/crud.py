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
        return await self.db_conn.update(CompanyModel, _id, data.dict())

    async def delete_by_id(self, _id: int) -> NoReturn:
        await self.db_conn.delete(CompanyModel, _id)


class TripCRUD(CRUDInterface):
    input_schema = TripInputSchema
    update_schema = TripUpdateSchema
    output_schema = TripOutputSchema

    async def create(self, data: TripInputSchema) -> TripOutputSchema:
        return await self.db_conn.insert(TripModel, data.dict())

    async def read(self, _filter: FilterHandler, pagination: Pagination) -> list[TripOutputSchema]:
        return await self.db_conn.select(TripModel, _filter, pagination)

    async def read_by_id(self, _id: int) -> CompanyOutputSchema:
        return (await self.db_conn.select_by_id(TripModel, _id))[0]

    async def update_by_id(self, _id: int, data: TripUpdateSchema) -> TripOutputSchema:
        return await self.db_conn.update(TripModel, _id, data.dict())

    async def delete_by_id(self, _id: int) -> NoReturn:
        await self.db_conn.delete(TripModel, _id)


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
