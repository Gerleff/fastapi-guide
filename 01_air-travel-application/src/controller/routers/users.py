from dataclasses import dataclass

from fastapi import APIRouter, Depends, Query
from pydantic import constr
from starlette import status

from controller.dependencies.auth import admin_only_permission
from controller.dependencies.filter.base import FilterHandler
from controller.dependencies.filter.depends import make_filter_dependency
from controller.dependencies.pagination.base import Pagination
from controller.dependencies.pagination.depends import page_size_pagination
from controller.schemas.input import UserInputSchema, UserUpdateSchema
from controller.schemas.output import UserOutputSchema
from model.enum import UserRoleEnum
from model.services.crud.user import UserCRUD

router = APIRouter(prefix="/users", tags=["User"])


@dataclass
class UserFilter:
    role__eq: UserRoleEnum | None = Query(None, description="filter by role", alias="role")
    role__in: list[UserRoleEnum] | None = Query(None, description="filter by inclusion in role list", alias="roles")
    name__like: constr(min_length=1, max_length=64) | None = Query(None, description="filter by name", alias="name")


@router.get("", response_model=list[UserOutputSchema])
async def get_users(
    pagination: Pagination = Depends(page_size_pagination),
    _filter: FilterHandler = Depends(make_filter_dependency(UserFilter)),
    service: UserCRUD = Depends(),
):
    return await service.read(_filter, pagination)


@router.get("/count", response_model=int)
async def get_users_count(
    pagination: Pagination = Depends(page_size_pagination),
    _filter: FilterHandler = Depends(make_filter_dependency(UserFilter)),
    service: UserCRUD = Depends(),
):
    return len(await service.read(_filter, pagination))


@router.get("/{_id}", response_model=UserOutputSchema)
async def get_user(_id: int, service: UserCRUD = Depends()):
    return await service.read_by_id(_id)


@router.post("", status_code=status.HTTP_201_CREATED, response_model=UserOutputSchema)
async def add_user(user_data: UserInputSchema, service: UserCRUD = Depends(), __auth=Depends(admin_only_permission)):
    return await service.create(user_data.dict())


@router.patch("/{_id}", response_model=UserOutputSchema)
async def edit_user(
    _id: int, user_data: UserUpdateSchema, service: UserCRUD = Depends(), __auth=Depends(admin_only_permission)
):
    return await service.update_by_id(_id, user_data.dict())


@router.delete("/{_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(_id: int, service: UserCRUD = Depends(), __auth=Depends(admin_only_permission)):
    await service.delete_by_id(_id)
