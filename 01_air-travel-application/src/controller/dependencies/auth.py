from fastapi import Security, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic.dataclasses import dataclass
from starlette import status

from models.enum import UserRoleEnum


@dataclass
class AuthData:
    id: int
    role: UserRoleEnum


_description = "Primitive auth schema. Credential format: role:id"
_auth_error = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authenticated")


def get_auth_data(security: HTTPAuthorizationCredentials = Security(HTTPBearer(description=_description))) -> AuthData:
    role, _id = security.credentials.split(":")
    return AuthData(id=_id, role=role)


async def check_user_existence(auth_data: AuthData = Depends(get_auth_data)) -> AuthData:
    # ToDO check in db_conn users existence
    if "exists":
        return auth_data
    raise _auth_error


def auth_only_permission(auth_data: AuthData = Depends(check_user_existence)) -> AuthData:
    return auth_data


def admin_only_permission(auth_data: AuthData = Depends(check_user_existence)) -> AuthData:
    if auth_data.role != UserRoleEnum.ADMIN:
        raise _auth_error
    return auth_data
