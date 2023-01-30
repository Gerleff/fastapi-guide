from pathlib import Path
from typing import Type, Protocol, NoReturn, Literal

from fastapi import FastAPI
from starlette.requests import Request

from config.settings import DBTypeEnum, DatabaseSettings
from model.storage.pythonic.storage import StorageHandler
from model.storage.raw_sql.storage import SQLiteDBHandler


class DatabaseConnectorProtocol(Protocol):
    async def connect(self, settings) -> NoReturn:
        ...

    async def disconnect(self, settings) -> NoReturn:
        ...


async def connect_on_startup(app: FastAPI, db_settings: DatabaseSettings):
    db_connection_cls: Type[DatabaseConnectorProtocol]
    match db_settings.database_type:
        case DBTypeEnum.pythonic_storage:
            db_connection_cls = StorageHandler
        case DBTypeEnum.sqlite:
            db_connection_cls = SQLiteDBHandler
        case _:
            raise NotImplementedError
    app.state.db_connection = db_connection_cls()
    await app.state.db_connection.connect(db_settings)


async def disconnect_on_shutdown(app, db_settings: DatabaseSettings):
    db_connection: DatabaseConnectorProtocol = app.state.db_connection
    await db_connection.disconnect(db_settings)


def get_db_connection(request: Request) -> DatabaseConnectorProtocol:
    return request.app.state.db_connection
