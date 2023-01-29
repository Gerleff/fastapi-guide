from typing import Type, TypeVar

from controller.dependencies.filters import filter_map_typing
from controller.dependencies.pagination import Pagination
from model.db_entities.models import BaseDBModel


ModelVar = TypeVar("ModelVar", bound=BaseDBModel)


class BaseDatabaseHandler:
    async def connect(self, settings): ...

    async def disconnect(self, settings): ...

    async def select(
            self, model: Type[ModelVar], filter_map: filter_map_typing, pagination: Pagination
    ) -> list[ModelVar]: ...

    async def select_by_id(self, model: Type[ModelVar], _id: int) -> ModelVar: ...

    async def insert(self, model: Type[ModelVar], value: dict) -> ModelVar: ...

    async def update_by_id(self, model: Type[ModelVar], _id: int, value: dict) -> ModelVar | None: ...

    async def delete_by_id(self, model: Type[ModelVar], _id: int) -> bool: ...
