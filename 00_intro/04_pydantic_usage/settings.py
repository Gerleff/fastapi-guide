from pydantic import BaseSettings, validator


class Settings(BaseSettings):
    class Config(BaseSettings.Config):
        env_prefix = "APP_"

    HOST: str = "localhost"
    PORT: int = 8000
    ADDRESS: str | None = None

    @validator("ADDRESS")
    def check_app_address(cls, value: str | None, values: dict) -> str:
        return value or f"http://{values.get('HOST')}:{values.get('PORT')}"


settings = Settings()
