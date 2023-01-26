from pathlib import Path
from typing import Type, Protocol, Literal, NoReturn

from starlette.requests import Request

from .pythonic.storage import StorageHandler


class DBSettingsProtocol(Protocol):
    database_type: Literal["pythonic_storage", "sqlite"] = "pythonic_storage"
    match database_type:
        case "pythonic_storage":
            file_path: str | Path = "storage.json"
            rollback: bool = True
        case _:
            raise NotImplementedError


class DatabaseConnectorProtocol(Protocol):
    async def connect(self, settings) -> NoReturn:
        ...

    async def disconnect(self, settings) -> NoReturn:
        ...


async def connect_on_startup(app, db_settings: DBSettingsProtocol):
    db_connection_cls: Type[DatabaseConnectorProtocol]
    match db_settings.database_type:
        case "pythonic_storage":
            db_connection_cls = StorageHandler
        case _:
            raise NotImplementedError
    app.state.db_connection = db_connection_cls()
    await app.state.db_connection.connect(db_settings)


async def disconnect_on_shutdown(app, db_settings: DBSettingsProtocol):
    db_connection: DatabaseConnectorProtocol = app.state.db_connection
    await db_connection.disconnect(db_settings)


def get_db_connection(request: Request):
    return request.app.state.db_connection
