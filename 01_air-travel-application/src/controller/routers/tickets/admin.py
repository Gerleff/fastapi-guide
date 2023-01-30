from dataclasses import dataclass

from fastapi import APIRouter, Depends, Query
from starlette import status

from controller.dependencies.auth import admin_only_permission
from controller.dependencies.filters import BaseFilter
from controller.dependencies.pagination import page_size_pagination, Pagination
from controller.schemas.input import TicketAdminInputSchema, TicketAdminUpdateSchema
from controller.schemas.output import TicketAdminOutputSchema
from model.services.crud.ticket import TicketCRUD

router = APIRouter(prefix="/admin/tickets", tags=["Ticket Admin"], dependencies=[Depends(admin_only_permission)])


@dataclass
class AdminTicketFilter(BaseFilter):
    trip__eq: int | None = Query(None, description="filter by trip id", alias="trip")
    trip__in: list[int] | None = Query(None, description="filter by inclusion in trip id list", alias="trips")


@router.get("", response_model=list[TicketAdminOutputSchema])
async def get_tickets(
    pagination: Pagination = Depends(page_size_pagination),
    _filter: AdminTicketFilter = Depends(),
    service: TicketCRUD = Depends(),
):
    return await service.read(_filter.make_filter_map(), pagination)


@router.get("/count", response_model=int)
async def get_tickets_count(
    pagination: Pagination = Depends(page_size_pagination),
    _filter: AdminTicketFilter = Depends(),
    service: TicketCRUD = Depends(),
):
    return len(await service.read(_filter.make_filter_map(), pagination))


@router.get("/{_id}", response_model=TicketAdminOutputSchema)
async def get_ticket(_id: int, service: TicketCRUD = Depends()):
    return await service.read_by_id(_id)


@router.post("", status_code=status.HTTP_201_CREATED, response_model=TicketAdminOutputSchema)
async def add_ticket(ticket_data: TicketAdminInputSchema, service: TicketCRUD = Depends()):
    return await service.create(ticket_data.dict())


@router.patch("/{_id}", response_model=TicketAdminOutputSchema)
async def edit_ticket(_id: int, ticket_data: TicketAdminUpdateSchema, service: TicketCRUD = Depends()):
    return await service.update_by_id(_id, ticket_data.dict())


@router.delete("/{_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_ticket(_id: int, service: TicketCRUD = Depends()):
    await service.delete_by_id(_id)
