from fastapi import APIRouter, Depends
from starlette import status

from controller.dependencies.auth import admin_only_permission
from controller.dependencies.pagination import Pagination, page_size_pagination
from models.services.crud import CompanyCRUD

router = APIRouter(prefix="/companies", tags=["Company"])


@router.get("", response_model=list[CompanyCRUD.output_schema])
async def get_companies(pagination: Pagination = Depends(page_size_pagination), service: CompanyCRUD = Depends()):
    return await service.read(None, pagination)


@router.get("/{_id}", response_model=CompanyCRUD.output_schema)
async def get_company(_id: int, service: CompanyCRUD = Depends()):
    return await service.read_by_id(_id)


@router.post("", status_code=status.HTTP_201_CREATED, response_model=CompanyCRUD.output_schema)
async def add_company(
    company_data: CompanyCRUD.input_schema, service: CompanyCRUD = Depends(), _=Depends(admin_only_permission)
):
    return await service.create(company_data)


@router.delete("/{_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_company(_id: int, service: CompanyCRUD = Depends(), _=Depends(admin_only_permission)):
    await service.delete_by_id(_id)
