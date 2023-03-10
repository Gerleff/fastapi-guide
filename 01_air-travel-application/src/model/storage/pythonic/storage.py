import operator
from pathlib import Path
from typing import Generic, Iterator, Protocol, Type

from pydantic import BaseModel, Field, validator
from pydantic.generics import GenericModel

from controller.dependencies.filters import filter_map_typing
from controller.dependencies.pagination import Pagination
from model.db_entities.models import CompanyModel, PassInTripModel, TripModel, UserModel, BaseDBModel
from model.storage.base import BaseDatabaseHandler, ModelVar
from model.storage.exceptions import EntityNotFoundError
from model.storage.pythonic.utils import filter_python_list, make_pagination_slice


class GenericStorageList(GenericModel, Generic[ModelVar], arbitrary_types_allowed=True):
    __root__: list[ModelVar] = Field(default_factory=list)

    @validator("__root__", each_item=True)
    def check_id(cls, value: ModelVar):
        """To validate each element of list separately"""
        if value.id is None:
            value.id = 0
        return value

    @validator("__root__")
    def check_root(cls, value: list[ModelVar]):
        """To validate whole list as united value"""
        return sorted(value, key=operator.attrgetter("id"))

    @property
    def next_id(self):
        if self.__root__:
            return self.__root__[-1].id + 1
        return 1

    def __iter__(self) -> Iterator[ModelVar]:
        return self.__root__.__iter__()

    def select(self, filter_map: filter_map_typing, pagination: Pagination):
        """Simple equality filter implementation"""
        return filter_python_list(filter_map, self.__root__)[make_pagination_slice(pagination)]

    def select_by_id(self, _id: int) -> ModelVar:
        for elem_index in range(len(self.__root__)):
            if self.__root__[elem_index].id == _id:
                return self.__root__[elem_index]

    def insert(self, value: ModelVar) -> ModelVar:
        self.__root__.append(value)
        return value

    def update(self, _id: int, value: dict) -> ModelVar | None:
        for elem_index in range(len(self.__root__)):
            if self.__root__[elem_index].id == _id:
                model_to_change = self.__root__[elem_index]
                for field, new_value in value.items():
                    setattr(model_to_change, field, new_value)
                return model_to_change

    def delete(self, _id: int) -> bool:
        for elem_index in range(len(self.__root__)):
            if self.__root__[elem_index].id == _id:
                del self.__root__[elem_index]
                return True
        return False


class Storage(BaseModel):
    companies: GenericStorageList[CompanyModel]
    trips: GenericStorageList[TripModel]
    pass_in_trip: GenericStorageList[PassInTripModel]
    users: GenericStorageList[UserModel]


class SettingsProtocol(Protocol):
    file_path: str | Path = "storage.json"
    rollback: bool = True


class StorageHandler(BaseDatabaseHandler):
    def __init__(self, storage: Storage | None = None):
        self.storage = storage

    async def connect(self, settings: SettingsProtocol):
        if not self.storage:
            self.storage = Storage.parse_file(settings.file_path)

    async def disconnect(self, settings: SettingsProtocol):
        if not settings.rollback:
            with open(settings.file_path, "w") as file:
                file.write(self.storage.json(indent=4, ensure_ascii=False))

    async def select(
        self, model: Type[BaseDBModel], filter_map: filter_map_typing, pagination: Pagination
    ) -> list[BaseDBModel]:
        pytonic_storage_list: GenericStorageList = getattr(self.storage, model.Meta.table)
        return pytonic_storage_list.select(filter_map, pagination)

    async def select_by_id(self, model: Type[BaseDBModel], _id: int) -> BaseDBModel:
        pytonic_storage_list: GenericStorageList = getattr(self.storage, table := model.Meta.table)
        if result := pytonic_storage_list.select_by_id(_id):
            return result
        raise EntityNotFoundError(table, _id)

    async def insert(self, model: Type[BaseDBModel], value: dict) -> ModelVar:
        pytonic_storage_list: GenericStorageList = getattr(self.storage, model.Meta.table)
        return pytonic_storage_list.insert(model(id=pytonic_storage_list.next_id, **value))

    async def update_by_id(self, model: Type[BaseDBModel], _id: int, value: dict) -> ModelVar | None:
        pytonic_storage_list: GenericStorageList = getattr(self.storage, table := model.Meta.table)
        if result := pytonic_storage_list.update(_id, value):
            return result
        raise EntityNotFoundError(table, _id)

    async def delete_by_id(self, model: Type[BaseDBModel], _id: int) -> bool:
        pytonic_storage_list: GenericStorageList = getattr(self.storage, table := model.Meta.table)
        if result := pytonic_storage_list.delete(_id):
            return result
        raise EntityNotFoundError(table, _id)
