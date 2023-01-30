from dataclasses import dataclass

from fastapi import APIRouter, Depends, Query
from starlette import status

from controller.dependencies.auth import admin_only_permission
from controller.dependencies.filters import BaseFilter
from controller.dependencies.pagination import Pagination, page_size_pagination
from controller.schemas.input import CompanyInputSchema, CompanyUpdateSchema
from controller.schemas.output import CompanyOutputSchema
from model.services.crud.company import CompanyCRUD

router = APIRouter(prefix="/companies", tags=["Company"])


@dataclass
class CompanyFilter(BaseFilter):
    id__eq: int | None = Query(None, description="filter by id", alias="id")
    id__in: list[int] | None = Query(None, description="filter by inclusion in id list", alias="ids")
    name__like: str | None = Query(None, description="filter by name", alias="name")


@router.get("", response_model=list[CompanyOutputSchema])
async def get_companies(
    pagination: Pagination = Depends(page_size_pagination),
    _filter: CompanyFilter = Depends(),
    service: CompanyCRUD = Depends(),
):
    return await service.read(_filter.make_filter_map(), pagination)


@router.get("/count", response_model=int)
async def get_companies_count(
    pagination: Pagination = Depends(page_size_pagination),
    _filter: CompanyFilter = Depends(),
    service: CompanyCRUD = Depends(),
):
    return len(await service.read(_filter.make_filter_map(), pagination))


@router.get("/{_id}", response_model=CompanyOutputSchema)
async def get_company(_id: int, service: CompanyCRUD = Depends()):
    return await service.read_by_id(_id)


@router.post("", status_code=status.HTTP_201_CREATED, response_model=CompanyOutputSchema)
async def add_company(
    company_data: CompanyInputSchema, service: CompanyCRUD = Depends(), __auth=Depends(admin_only_permission)
):
    return await service.create(company_data.dict())


@router.patch("/{_id}", response_model=CompanyOutputSchema)
async def edit_company(
    _id: int, company_data: CompanyUpdateSchema, service: CompanyCRUD = Depends(), __auth=Depends(admin_only_permission)
):
    return await service.update_by_id(_id, company_data.dict(exclude_none=True))


@router.delete("/{_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_company(_id: int, service: CompanyCRUD = Depends(), __auth=Depends(admin_only_permission)):
    await service.delete_by_id(_id)
