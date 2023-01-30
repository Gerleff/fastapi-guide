from typing import Collection, NamedTuple, Callable

from fastapi import Security, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette import status

from model.enum import UserRoleEnum
from model.services.crud.user import UserCRUD
from model.storage.exceptions import EntityNotFoundError


class AuthData(NamedTuple):
    id: int
    role: UserRoleEnum


_description = "Primitive auth schema. Credential format: id"
_auth_error = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authenticated")


async def get_auth_data(
    security: HTTPAuthorizationCredentials = Security(HTTPBearer(description=_description)),
    user_service: UserCRUD = Depends(),
) -> AuthData:
    _id = security.credentials
    try:
        user_from_db = await user_service.read_by_id(int(_id))
    except (ValueError, EntityNotFoundError) as error:
        raise _auth_error from error

    return AuthData(user_from_db.id, user_from_db.role)


def make_auth_dependency(allowed_roles: Collection[UserRoleEnum] = None) -> Callable[[AuthData], AuthData]:
    def auth_dependency(auth_data: AuthData = Depends(get_auth_data)) -> AuthData:
        if allowed_roles and auth_data.role not in allowed_roles:
            raise _auth_error
        return auth_data

    return auth_dependency


auth_only_permission = make_auth_dependency()
admin_only_permission = make_auth_dependency((UserRoleEnum.ADMIN,))
