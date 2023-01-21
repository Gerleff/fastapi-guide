from pydantic import BaseModel, Field
from pydantic.generics import GenericModel
from typing import TypeVar, Generic, Iterator
from schemas import CompanyOutputSchema, TripOutputSchema, TripForPassengerOutputSchema

SchemaToStoreVar = TypeVar("SchemaToStoreVar", bound=BaseModel)


class GenericStorageList(GenericModel, Generic[SchemaToStoreVar]):
    __root__: list[SchemaToStoreVar] = Field(default_factory=list)

    # ToDO validate each __root__ elem

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
