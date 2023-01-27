from dataclasses import dataclass

from fastapi import APIRouter, Depends, Query
from starlette import status

from controller.dependencies.auth import admin_only_permission
from controller.dependencies.filter.base import FilterHandler
from controller.dependencies.filter.depends import make_filter_dependency
from controller.dependencies.pagination.base import Pagination
from controller.dependencies.pagination.depends import page_size_pagination
from controller.schemas.input import TicketInputSchema, TicketUpdateSchema
from controller.schemas.output import TicketOutputSchema
from model.services.crud.ticket import TicketCRUD

router = APIRouter(prefix="/tickets", tags=["Ticket"])


@dataclass
class TicketFilter:
    trip__eq: int | None = Query(None, description="filter by trip id", alias="trip")
    trip__in: list[int] | None = Query(None, description="filter by inclusion in trip id list", alias="trips")


@router.get("", response_model=list[TicketOutputSchema])
async def get_tickets(
    pagination: Pagination = Depends(page_size_pagination),
    _filter: FilterHandler = Depends(make_filter_dependency(TicketFilter)),
    service: TicketCRUD = Depends(),
):
    return await service.read(_filter, pagination)


@router.get("/count", response_model=int)
async def get_tickets_count(
    pagination: Pagination = Depends(page_size_pagination),
    _filter: FilterHandler = Depends(make_filter_dependency(TicketFilter)),
    service: TicketCRUD = Depends(),
):
    return len(await service.read(_filter, pagination))


@router.get("/{_id}", response_model=TicketOutputSchema)
async def get_ticket(_id: int, service: TicketCRUD = Depends()):
    return await service.read_by_id(_id)


@router.post("", status_code=status.HTTP_201_CREATED, response_model=TicketOutputSchema)
async def add_ticket(
    ticket_data: TicketInputSchema, service: TicketCRUD = Depends(), __auth=Depends(admin_only_permission)
):
    return await service.create(ticket_data.dict())


@router.patch("/{_id}", response_model=TicketOutputSchema)
async def edit_ticket(
    _id: int, ticket_data: TicketUpdateSchema, service: TicketCRUD = Depends(), __auth=Depends(admin_only_permission)
):
    return await service.update_by_id(_id, ticket_data.dict())


@router.delete("/{_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_ticket(_id: int, service: TicketCRUD = Depends(), __auth=Depends(admin_only_permission)):
    await service.delete_by_id(_id)
