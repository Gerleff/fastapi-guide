from typing import Protocol, NoReturn, Literal


class DatabaseProtocol(Protocol):
    async def connect(self, settings) -> NoReturn:
        ...

    async def disconnect(self, settings) -> NoReturn:
        ...

    async def select(self, model, _filter, pagination) -> list[...]:
        ...

    def select_by_id(self, model, _id) -> ...:
        ...

    async def insert(self, model, value) -> ...:
        ...

    async def update(self, model, _id: int, value) -> ...:
        ...

    async def delete(self, model, _id: int) -> bool:
        ...


class DBSettingsProtocol(Protocol):
    database_type: Literal["pythonic_storage", "sqlite"] = "pythonic_storage"
