from dataclasses import dataclass
from datetime import datetime

from fastapi import APIRouter, Depends, Query
from pydantic import constr
from starlette import status

from controller.dependencies.auth import admin_only_permission
from controller.dependencies.filter.base import FilterHandler
from controller.dependencies.filter.depends import make_filter_dependency
from controller.dependencies.pagination.base import Pagination
from controller.dependencies.pagination.depends import page_size_pagination
from models.enum import PlaneEnum
from models.services.crud import TripCRUD

router = APIRouter(prefix="/trips", tags=["Trip"])


@dataclass
class TripFilter:
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


@router.get("", response_model=list[TripCRUD.output_schema])
async def get_trips(
    pagination: Pagination = Depends(page_size_pagination),
    _filter: FilterHandler = Depends(make_filter_dependency(TripFilter)),
    service: TripCRUD = Depends(),
):
    return await service.read(_filter, pagination)


@router.get("/count", response_model=int)
async def get_trips_count(
    pagination: Pagination = Depends(page_size_pagination),
    _filter: FilterHandler = Depends(make_filter_dependency(TripFilter)),
    service: TripCRUD = Depends(),
):
    return len(await service.read(_filter, pagination))


@router.get("/{_id}", response_model=TripCRUD.output_schema)
async def get_trip(_id: int, service: TripCRUD = Depends()):
    return await service.read_by_id(_id)


@router.post("", status_code=status.HTTP_201_CREATED, response_model=TripCRUD.output_schema)
async def add_trip(
    company_data: TripCRUD.input_schema, service: TripCRUD = Depends(), __auth=Depends(admin_only_permission)
):
    return await service.create(company_data)


@router.delete("/{_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_trip(_id: int, service: TripCRUD = Depends(), __auth=Depends(admin_only_permission)):
    await service.delete_by_id(_id)
