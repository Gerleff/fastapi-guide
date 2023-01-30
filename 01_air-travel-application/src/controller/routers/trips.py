from dataclasses import dataclass
from datetime import datetime

from fastapi import APIRouter, Depends, Query
from pydantic import constr
from starlette import status

from controller.dependencies.auth import admin_only_permission
from controller.dependencies.filters import BaseFilter
from controller.dependencies.pagination import page_size_pagination, Pagination
from controller.schemas.input import TripInputSchema, TripUpdateSchema
from controller.schemas.output import TripOutputSchema
from model.enum import PlaneEnum
from model.services.crud.trip import TripCRUD

router = APIRouter(prefix="/trips", tags=["Trip"])


@dataclass
class TripFilter(BaseFilter):
    company__eq: int | None = Query(None, description="filter by company id", alias="company")
    company__in: list[int] | None = Query(None, description="filter by inclusion in company id list", alias="companies")
    plane__eq: PlaneEnum | None = Query(None, description="filter by plane", alias="plane")
    plane__in: list[PlaneEnum] | None = Query(None, description="filter by planes", alias="planes")
    town_from__like: constr(min_length=1, max_length=64) | None = Query(
        None, description="filter by town_from", alias="town_from"
    )
    town_to__like: constr(min_length=1, max_length=64) | None = Query(
        None, description="filter by town_to", alias="town_to"
    )
    time_out__le: datetime | None = Query(None, description="filter by trips <= time_out", alias="time_out_le")
    time_out__ge: datetime | None = Query(None, description="filter by trips >= time_out", alias="time_out_ge")
    time_in__le: datetime | None = Query(None, description="filter by trips <= time_in", alias="time_in_le")
    time_in__ge: datetime | None = Query(None, description="filter by trips >= time_in", alias="time_in_ge")


@router.get("", response_model=list[TripOutputSchema])
async def get_trips(
    pagination: Pagination = Depends(page_size_pagination),
    _filter: TripFilter = Depends(),
    service: TripCRUD = Depends(),
):
    return await service.read(_filter.make_filter_map(), pagination)


@router.get("/count", response_model=int)
async def get_trips_count(
    pagination: Pagination = Depends(page_size_pagination),
    _filter: TripFilter = Depends(),
    service: TripCRUD = Depends(),
):
    return len(await service.read(_filter.make_filter_map(), pagination))


@router.get("/{_id}", response_model=TripOutputSchema)
async def get_trip(_id: int, service: TripCRUD = Depends()):
    return await service.read_by_id(_id)


@router.post("", status_code=status.HTTP_201_CREATED, response_model=TripOutputSchema)
async def add_trip(trip_data: TripInputSchema, service: TripCRUD = Depends(), __auth=Depends(admin_only_permission)):
    return await service.create(trip_data.dict())


@router.patch("/{_id}", response_model=TripOutputSchema)
async def edit_trip(
    _id: int, trip_data: TripUpdateSchema, service: TripCRUD = Depends(), __auth=Depends(admin_only_permission)
):
    return await service.update_by_id(_id, trip_data.dict(exclude_none=True))


@router.delete("/{_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_trip(_id: int, service: TripCRUD = Depends(), __auth=Depends(admin_only_permission)):
    await service.delete_by_id(_id)
