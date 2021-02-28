from enum import Enum

from pydantic import BaseSettings, HttpUrl


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


settings = Settings()
