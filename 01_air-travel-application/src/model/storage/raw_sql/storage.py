import asyncio
import sqlite3
from sqlite3 import Connection, Cursor
from typing import Type

from config.settings import DatabaseSettings
from controller.dependencies.filters import filter_map_typing
from controller.dependencies.pagination import Pagination
from model.storage.base import BaseDatabaseHandler, ModelVar
from model.storage.exceptions import EntityNotFoundError
from model.storage.raw_sql.utils import make_sql_from_filter_map, make_pagination_sql, parse_db_record_into_model


def make_insert_values_statement(table: str, data: dict) -> str:
    insert_fields = ", ".join(data.keys())
    insert_values = ", ".join(f"\"{value}\"" for value in data.values())
    return f"INSERT INTO {table} ({insert_fields}) VALUES ({insert_values}) RETURNING *"


def make_update_values_statement(table: str, data: dict, _id: int) -> str:
    field_value_pairs = ",".join((f"{field} = {value}" for field, value in data.items()))
    return f"UPDATE {table} SET {field_value_pairs} WHERE id = {_id} RETURNING *"


class SQLiteDBHandler(BaseDatabaseHandler):
    def __init__(self, connection: Connection | None = None):
        self.connection = connection

    async def connect(self, settings: DatabaseSettings):
        if not self.connection:
            self.connection = sqlite3.connect(settings.address)

    async def disconnect(self, _):
        self.connection.close()

    async def _fetch(self, sql_statement: str) -> list[tuple]:
        cursor: Cursor = self.connection.cursor()
        cursor.execute(sql_statement)
        await asyncio.sleep(0)
        return cursor.fetchall()

    async def select(
        self, model: Type[ModelVar], filter_map: filter_map_typing, pagination: Pagination
    ) -> list[ModelVar]:
        sql_statement = f"SELECT * FROM {model.Meta.table}"
        if filter_sql_statement := make_sql_from_filter_map(filter_map):
            sql_statement += filter_sql_statement
        sql_statement += make_pagination_sql(pagination)
        return [parse_db_record_into_model(row, model) for row in await self._fetch(sql_statement)]

    async def select_by_id(self, model: Type[ModelVar], _id: int) -> ModelVar:
        sql_statement = f"SELECT * FROM {(table := model.Meta.table)} WHERE id = {_id}"
        if result := await self._fetch(sql_statement):
            return parse_db_record_into_model(result[0], model)
        raise EntityNotFoundError(table, _id)

    async def insert(self, model: Type[ModelVar], value: dict) -> ModelVar:
        result = await self._fetch(make_insert_values_statement(model.Meta.table, value))
        return parse_db_record_into_model(result[0], model)

    async def update_by_id(self, model: Type[ModelVar], _id: int, value: dict) -> ModelVar | None:
        result = await self._fetch(make_update_values_statement(model.Meta.table, value, _id))
        return parse_db_record_into_model(result[0], model)

    async def delete_by_id(self, model: Type[ModelVar], _id: int) -> bool:
        sql_statement = f"DELETE FROM {model.Meta.table} WHERE id = {_id}"
        await self._fetch(sql_statement)
        return True
