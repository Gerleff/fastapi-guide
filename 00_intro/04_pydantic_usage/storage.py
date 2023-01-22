import operator

from pydantic import BaseModel, Field, validator, root_validator
from pydantic.generics import GenericModel
from typing import TypeVar, Generic, Iterator
from schemas import CompanyOutputSchema, TripOutputSchema, TripForPassengerOutputSchema

SchemaToStoreVar = TypeVar("SchemaToStoreVar", bound=BaseModel)


class GenericStorageList(GenericModel, Generic[SchemaToStoreVar]):
    __root__: list[SchemaToStoreVar] = Field(default_factory=list)

    @validator("__root__", each_item=True)
    def check_id(cls, value: SchemaToStoreVar):
        """To validate each element of list separately"""
        if value.id is None:
            value.id = 0
        return value

    @validator("__root__")
    def check_root(cls, value: list[SchemaToStoreVar]):
        """To validate whole list as united value"""
        return sorted(value, key=operator.attrgetter("id"))

    def __iter__(self) -> Iterator[SchemaToStoreVar]:
        return self.__root__.__iter__()

    def filter(self):
        return self.__root__

    def get_by_id(self, _id: int) -> SchemaToStoreVar | None:
        for elem in self:
            if elem.id == _id:
                return elem

    def insert(self, value: SchemaToStoreVar) -> SchemaToStoreVar:
        if self.__root__:
            assert isinstance(value, type(_last_elem := self.__root__[-1])), "Entities in storage must be the same type"
            value.id = _last_elem.id + 1
        else:
            value.id = 1
        self.__root__.append(value)
        return value

    def update_by_id(self, _id: int, value: SchemaToStoreVar) -> SchemaToStoreVar | None:
        for elem_index in range(len(self.__root__)):
            if self.__root__[elem_index].id == _id:
                value.id = _id
                self.__root__[elem_index] = value
                return value

    def delete_by_id(self, _id: int) -> bool:
        for elem_index in range(len(self.__root__)):
            if self.__root__[elem_index].id == _id:
                del self.__root__[elem_index]
                return True
        return False


class Storage(BaseModel):
    companies: GenericStorageList[CompanyOutputSchema]
    trips: GenericStorageList[TripOutputSchema]
    pass_in_trip: GenericStorageList[TripForPassengerOutputSchema]

    # Just to show usage of flag "pre"
    @root_validator(pre=True)
    def show_root_validator_with_pre_true(cls, values):
        print(values)
        return values

    @root_validator()
    def show_root_validator_with_pre_false(cls, values):
        print(values)
        return values
