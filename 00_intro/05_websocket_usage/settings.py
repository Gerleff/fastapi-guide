from pydantic import BaseSettings, validator


class Settings(BaseSettings):
    host: str = "localhost"
    port: int = 8000
    address: str | None = None

    @validator("address")
    def check_app_address(cls, value: str | None, values: dict) -> str:
        return value or f"http://{values.get('host')}:{values.get('port')}"


settings = Settings()
