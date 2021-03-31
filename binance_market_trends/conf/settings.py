from enum import Enum

from pydantic import BaseSettings, HttpUrl
from sqlalchemy.engine.url import URL


class LogLevel(str, Enum):
    DEBUG = 'DEBUG'
    INFO = 'INFO'
    WARNING = 'WARNING'
    ERROR = 'ERROR'
    CRITICAL = 'CRITICAL'


class Env(str, Enum):
    LOCAL = 'LOCAL'
    STAGING = 'STAGING'
    PRODUCTION = 'PRODUCTION'


class Settings(BaseSettings):
    DEBUG: bool = False
    ENV: Env = Env.LOCAL.value
    LOG_LEVEL: LogLevel = LogLevel.INFO.value
    ALLOWED_ORIGINS: str = 'http://localhost'
    API_PORT: int = 80
    SENTRY_DSN: HttpUrl = None
    POSTGRES_USER: str = 'postgres'
    POSTGRES_PASSWORD: str = ''
    POSTGRES_DB: str = 'postgres'
    POSTGRES_HOSTNAME: str = 'localhost'
    POSTGRES_PORT: int = 5432

    @property
    def sqlalchemy_database_uri(self) -> str:
        return str(URL(
            drivername='postgresql',
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_HOSTNAME,
            port=self.POSTGRES_PORT,
            database=self.POSTGRES_DB,
        ))


settings = Settings()
