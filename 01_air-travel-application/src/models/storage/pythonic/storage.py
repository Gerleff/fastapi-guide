import operator
from pathlib import Path

from pydantic import BaseModel, Field, validator
from pydantic.generics import GenericModel
from typing import TypeVar, Generic, Iterator, Protocol, runtime_checkable
from models.database.models import CompanyModel, PassInTripModel, TripModel, UserModel


@runtime_checkable
class ModelProtocol(Protocol):
    id: int

    class Meta:
        table: str


@runtime_checkable
class FilterProtocol(Protocol):
    def filter_python_list(self, python_list: list) -> list:
        ...


@runtime_checkable
class PaginationProtocol(Protocol):
    @property
    def slice(self) -> slice:
        return ...


ModelToStoreVar = TypeVar("ModelToStoreVar", bound=ModelProtocol)


class GenericStorageList(GenericModel, Generic[ModelToStoreVar], arbitrary_types_allowed=True):
    __root__: list[ModelToStoreVar] = Field(default_factory=list)

    @validator("__root__", each_item=True)
    def check_id(cls, value: ModelToStoreVar):
        """To validate each element of list separately"""
        if value.id is None:
            value.id = 0
        return value

    @validator("__root__")
    def check_root(cls, value: list[ModelToStoreVar]):
        """To validate whole list as united value"""
        return sorted(value, key=operator.attrgetter("id"))

    def __iter__(self) -> Iterator[ModelToStoreVar]:
        return self.__root__.__iter__()

    def select(self, _filter: FilterProtocol, pagination: PaginationProtocol):
        """Simple equality filter implementation"""
        return _filter.filter_python_list(self.__root__)[pagination.slice]

    def select_by_id(self, _id: int) -> ModelToStoreVar:
        for elem_index in range(len(self.__root__)):
            if self.__root__[elem_index].id == _id:
                return self.__root__[elem_index]

    def insert(self, value: ModelToStoreVar) -> ModelToStoreVar:
        if self.__root__:
            _last_elem = self.__root__[-1]
            # assert isinstance(value, type(_last_elem)), "Entities in db_conn must be the same type"
            value.id = _last_elem.id + 1
        else:
            value.id = 1
        self.__root__.append(value)
        return value

    def update(self, _id: int, value: ModelToStoreVar) -> ModelToStoreVar | None:
        for elem_index in range(len(self.__root__)):
            if self.__root__[elem_index].id == _id:
                value.id = _id
                self.__root__[elem_index] = value
                return value

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


class StorageHandler:
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
            self, model: ModelProtocol, _filter: FilterProtocol, pagination: PaginationProtocol
    ) -> list[ModelProtocol]:
        pytonic_storage_list: GenericStorageList = getattr(self.storage, model.Meta.table)
        return pytonic_storage_list.select(_filter, pagination)

    async def select_by_id(self, model: ModelProtocol, _id: int) -> ModelProtocol:
        pytonic_storage_list: GenericStorageList = getattr(self.storage, model.Meta.table)
        return pytonic_storage_list.select_by_id(_id)

    async def insert(self, model: ModelProtocol, value: ModelToStoreVar) -> ModelToStoreVar:
        pytonic_storage_list: GenericStorageList = getattr(self.storage, model.Meta.table)
        return pytonic_storage_list.insert(value)

    async def update(self, model: ModelProtocol, _id: int, value: ModelToStoreVar) -> ModelToStoreVar | None:
        pytonic_storage_list: GenericStorageList = getattr(self.storage, model.Meta.table)
        return pytonic_storage_list.update(_id, value)

    async def delete(self, model: ModelProtocol, _id: int) -> bool:
        pytonic_storage_list: GenericStorageList = getattr(self.storage, model.Meta.table)
        return pytonic_storage_list.delete(_id)
