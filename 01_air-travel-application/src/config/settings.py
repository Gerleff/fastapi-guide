from pathlib import Path

from pydantic import BaseSettings, validator


class Settings(BaseSettings):  # ToDO separate
    class Config(BaseSettings.Config):
        env_file = ".env"
        env_prefix = "APP_"

    HOST: str = "localhost"
    PORT: int = 8000
    ADDRESS: str | None = None

    @validator("ADDRESS")
    def check_app_address(cls, value: str | None, values: dict) -> str:
        return value or f"http://{values.get('HOST')}:{values.get('PORT')}"

    database_type: str = "pythonic_storage"
    file_path: str | Path = "model/storage/pythonic/storage.json"
    rollback: bool = True


def get_settings(_settings: Settings = Settings()):
    return _settings
