from dataclasses import dataclass
from enum import Enum
from pathlib import Path

from pydantic import BaseSettings, validator


class AppSettings(BaseSettings):
    class Config(BaseSettings.Config):
        env_file = ".env"
        env_prefix = "APP_"

    HOST: str = "localhost"
    PORT: int = 8000
    ADDRESS: str | None = None

    @validator("ADDRESS")
    def check_app_address(cls, value: str | None, values: dict) -> str:
        return value or f"http://{values.get('HOST')}:{values.get('PORT')}"


class DBTypeEnum(str, Enum):
    pythonic_storage = "pythonic_storage"
    sqlite = "sqlite"


class DatabaseSettings(BaseSettings):
    class Config(BaseSettings.Config):
        env_file = ".env"
        env_prefix = "DB_"

    database_type: DBTypeEnum = "sqlite"
    file_path: str | Path = "model/storage/pythonic/storage.json"
    rollback: bool = True

    address: str = "model/storage/raw_sql/storage.db"


@dataclass
class Settings:
    app: AppSettings = AppSettings()
    database: DatabaseSettings = DatabaseSettings()


def get_settings(_settings: Settings = Settings()):
    return _settings
