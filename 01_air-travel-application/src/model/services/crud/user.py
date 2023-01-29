from typing import NoReturn

from controller.dependencies.filters import filter_map_typing
from controller.dependencies.pagination import Pagination
from model.db_entities.models import UserModel
from model.services.crud.base import CRUDInterface
from model.services.dto import UserDTO


class UserCRUD(CRUDInterface):
    async def create(self, data: dict) -> UserDTO:
        return UserDTO.from_database(await self.db_conn.insert(UserModel, data))

    async def read(self, filter_map: filter_map_typing, pagination: Pagination) -> list[UserDTO]:
        return [UserDTO.from_database(row) for row in await self.db_conn.select(UserModel, filter_map, pagination)]

    async def read_by_id(self, _id: int) -> UserDTO:
        return UserDTO.from_database(await self.db_conn.select_by_id(UserModel, _id))

    async def update_by_id(self, _id: int, data: dict) -> UserDTO:
        return UserDTO.from_database(await self.db_conn.update_by_id(UserModel, _id, data))

    async def delete_by_id(self, _id: int) -> NoReturn:
        await self.db_conn.delete_by_id(UserModel, _id)
