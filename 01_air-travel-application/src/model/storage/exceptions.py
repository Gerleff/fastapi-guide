from typing import Protocol, TypeVar, Type


class ModelProtocol(Protocol):
    id: int | None

    class Meta:
        table: str


ModelArgT = TypeVar("ModelArgT", bound=Type[ModelProtocol])


class EntityNotFoundError(Exception):
    message = None
    message_format = "Entity with id {} is not found in table {}"

    def __init_(self, model: ModelArgT, _id: int):
        self.message = self.message_format.format(_id, model.Meta.table)
