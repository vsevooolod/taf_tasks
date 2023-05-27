from pathlib import Path
from functools import lru_cache

from pydantic import SecretStr, StrictStr, AnyUrl, PositiveInt, validator
from dotenv import find_dotenv
from pydantic.env_settings import BaseSettings

from app.pkg.models import Logger


class _Settings(BaseSettings):
    class Config:
        env_file_encoding = "utf-8"
        arbitrary_types_allowed = True


class Settings(_Settings):
    X_API_TOKEN: SecretStr
    TZ: str

    POSTGRES_HOST: StrictStr
    POSTGRES_PORT: PositiveInt
    POSTGRES_USER: StrictStr
    POSTGRES_PASSWORD: SecretStr
    POSTGRES_DB: StrictStr

    LOGGER_LEVEL: Logger
    LOGGER_DIR_PATH_INTERNAL: Path

    @validator("LOGGER_DIR_PATH_INTERNAL")
    def create_logger_directory(cls, v: Path) -> Path:
        if not v.exists():
            v.mkdir(parents=True, exist_ok=True)
        return v


@lru_cache()
def get_settings(env_file: str = ".env") -> Settings:
    return Settings(_env_file=find_dotenv(env_file))
