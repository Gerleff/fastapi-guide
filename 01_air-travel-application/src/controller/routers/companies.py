from fastapi import APIRouter, Depends, Query
from dataclasses import dataclass
from starlette import status

from controller.dependencies.auth import admin_only_permission
from controller.dependencies.filter_dep import make_filter_dependancy, FilterHandler
from controller.dependencies.pagination import Pagination, page_size_pagination
from models.services.crud import CompanyCRUD

router = APIRouter(prefix="/companies", tags=["Company"])


@dataclass
class CompanyFilter:
    id__eq: int | None = Query(None, description="filter by id", alias="id")
    id__in: list[int] | None = Query(None, description="filter by inclusion in id list", alias="ids")
    name__like: str | None = Query(None, description="filter by name", alias="name")


@router.get("", response_model=list[CompanyCRUD.output_schema])
async def get_companies(
    pagination: Pagination = Depends(page_size_pagination),
    _filter: FilterHandler = Depends(make_filter_dependancy(CompanyFilter)),
    service: CompanyCRUD = Depends(),
):
    return await service.read(_filter, pagination)


@router.get("/count", response_model=int)
async def get_companies_count(
    pagination: Pagination = Depends(page_size_pagination),
    _filter: FilterHandler = Depends(make_filter_dependancy(CompanyFilter)),
    service: CompanyCRUD = Depends(),
):
    return len(await service.read(_filter, pagination))


@router.get("/{_id}", response_model=CompanyCRUD.output_schema)
async def get_company(_id: int, service: CompanyCRUD = Depends()):
    return await service.read_by_id(_id)


@router.post("", status_code=status.HTTP_201_CREATED, response_model=CompanyCRUD.output_schema)
async def add_company(
    company_data: CompanyCRUD.input_schema, service: CompanyCRUD = Depends(), __auth=Depends(admin_only_permission)
):
    return await service.create(company_data)


@router.delete("/{_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_company(_id: int, service: CompanyCRUD = Depends(), __auth=Depends(admin_only_permission)):
    await service.delete_by_id(_id)
