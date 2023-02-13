from fastapi import APIRouter, Depends
from starlette import status
from starlette.responses import Response

from controller.dependencies.auth import AuthData, auth_only_permission
from controller.schemas.input import UserProfileInputSchema, UserProfileUpdateSchema
from controller.schemas.output import UserProfileOutputSchema
from model.services.crud.user import UserCRUD

router = APIRouter(prefix="/profile", tags=["User profile"])


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=UserProfileOutputSchema)
async def add_user(
    user_data: UserProfileInputSchema,
    response: Response,
    service: UserCRUD = Depends(),
):
    new_user = await service.create(user_data.dict())
    response.headers["UserId"] = str(new_user.id)
    return new_user


@router.get("/me", response_model=UserProfileOutputSchema)
async def get_user(
    service: UserCRUD = Depends(),
    user: AuthData = Depends(auth_only_permission),
):
    return await service.read_by_id(user.id)


@router.patch("/me", response_model=UserProfileOutputSchema)
async def edit_user(
    user_data: UserProfileUpdateSchema, service: UserCRUD = Depends(), user: AuthData = Depends(auth_only_permission)
):
    return await service.update_by_id(user.id, user_data.dict(exclude_none=True))


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(service: UserCRUD = Depends(), user: AuthData = Depends(auth_only_permission)):
    await service.delete_by_id(user.id)
