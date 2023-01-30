from dataclasses import dataclass

from fastapi import APIRouter, Depends, Query
from pydantic import constr
from starlette import status

from controller.dependencies.auth import admin_only_permission
from controller.dependencies.filters import BaseFilter
from controller.dependencies.pagination import page_size_pagination, Pagination
from controller.schemas.input import UserAdminInputSchema, UserAdminUpdateSchema
from controller.schemas.output import UserAdminOutputSchema
from model.enum import UserRoleEnum
from model.services.crud.user import UserCRUD

router = APIRouter(prefix="/admin/users", tags=["User admin"], dependencies=[Depends(admin_only_permission)])


@dataclass
class UserFilter(BaseFilter):
    role__eq: UserRoleEnum | None = Query(None, description="filter by role", alias="role")
    role__in: list[UserRoleEnum] | None = Query(None, description="filter by inclusion in role list", alias="roles")
    name__like: constr(min_length=1, max_length=64) | None = Query(None, description="filter by name", alias="name")


@router.get("", response_model=list[UserAdminOutputSchema])
async def get_users(
    pagination: Pagination = Depends(page_size_pagination),
    _filter: UserFilter = Depends(),
    service: UserCRUD = Depends(),
):
    return await service.read(_filter.make_filter_map(), pagination)


@router.get("/count", response_model=int)
async def get_users_count(
    pagination: Pagination = Depends(page_size_pagination),
    _filter: UserFilter = Depends(),
    service: UserCRUD = Depends(),
):
    return len(await service.read(_filter.make_filter_map(), pagination))


@router.get("/{_id}", response_model=UserAdminOutputSchema)
async def get_user(_id: int, service: UserCRUD = Depends()):
    return await service.read_by_id(_id)


@router.post("", status_code=status.HTTP_201_CREATED, response_model=UserAdminOutputSchema)
async def add_user(user_data: UserAdminInputSchema, service: UserCRUD = Depends()):
    return await service.create(user_data.dict())


@router.patch("/{_id}", response_model=UserAdminOutputSchema)
async def edit_user(_id: int, user_data: UserAdminUpdateSchema, service: UserCRUD = Depends()):
    return await service.update_by_id(_id, user_data.dict(exclude_none=True))


@router.delete("/{_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(_id: int, service: UserCRUD = Depends()):
    await service.delete_by_id(_id)
