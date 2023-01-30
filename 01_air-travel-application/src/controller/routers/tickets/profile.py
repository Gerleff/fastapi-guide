from dataclasses import dataclass

from fastapi import APIRouter, Depends, Query
from starlette import status

from controller.dependencies.auth import auth_only_permission, AuthData
from controller.dependencies.filters import BaseFilter, filter_map_typing
from controller.dependencies.pagination import page_size_pagination, Pagination
from controller.schemas.input import TicketProfileInputSchema
from controller.schemas.output import TicketProfileOutputSchema
from model.services.crud.ticket import TicketCRUD

router = APIRouter(prefix="/profile/tickets", tags=["Ticket profile"])


@dataclass
class ProfileTicketFilter(BaseFilter):
    place__eq: str | None = Query(None, description="filter by place", alias="place")

    def make_profile_filter_map(self, user_id: int) -> filter_map_typing:
        filter_map = self.make_filter_map()
        if filter_map.get("eq_"):
            filter_map["eq_"].append(("passenger", user_id))
        else:
            filter_map["eq_"] = [("passenger", user_id)]
        return filter_map


@router.get("", response_model=list[TicketProfileOutputSchema])
async def get_tickets(
    pagination: Pagination = Depends(page_size_pagination),
    _filter: ProfileTicketFilter = Depends(),
    service: TicketCRUD = Depends(),
    user: AuthData = Depends(auth_only_permission),
):
    return await service.read(_filter.make_profile_filter_map(user.id), pagination)


@router.get("/count", response_model=int)
async def get_tickets_count(
    pagination: Pagination = Depends(page_size_pagination),
    _filter: ProfileTicketFilter = Depends(),
    service: TicketCRUD = Depends(),
    user: AuthData = Depends(auth_only_permission),
):
    return len(await service.read(_filter.make_profile_filter_map(user.id), pagination))


@router.get("/{_id}", response_model=TicketProfileOutputSchema)
async def get_ticket(
    _id: int,
    service: TicketCRUD = Depends(),
    user: AuthData = Depends(auth_only_permission),
):
    return (await service.read({"eq_": [("passenger", user.id)]}))[0]


@router.post("", status_code=status.HTTP_201_CREATED, response_model=TicketProfileOutputSchema)
async def add_ticket(
    ticket_data: TicketProfileInputSchema,
    service: TicketCRUD = Depends(),
    user: AuthData = Depends(auth_only_permission),
):
    return await service.create({"passenger": user.id, **ticket_data.dict()})
