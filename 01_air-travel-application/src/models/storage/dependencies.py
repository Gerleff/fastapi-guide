from typing import Type

from starlette.requests import Request

from .protocol import DBSettingsProtocol, DatabaseProtocol
from .pythonic.storage import StorageHandler


async def connect_on_startup(app, db_settings: DBSettingsProtocol):
    db_connection_cls: Type[DatabaseProtocol]
    match db_settings.database_type:
        case "pythonic_storage":
            db_connection_cls = StorageHandler
        case _:
            raise NotImplementedError
    app.state.db_connection = db_connection_cls()
    await app.state.db_connection.connect(db_settings)


async def disconnect_on_shutdown(app, db_settings: DBSettingsProtocol):
    db_connection: DatabaseProtocol = app.state.db_connection
    await db_connection.disconnect(db_settings)


def get_db_connection(request: Request):
    return request.app.state.db_connection
