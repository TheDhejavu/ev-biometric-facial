# Application Configuration Class
import logging
import sys
from typing import List
import os

from loguru import logger
from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings, Secret

from app.common.logger import InterceptHandler

API_PREFIX = "/api"

JWT_TOKEN_PREFIX = "Token"  # noqa: S105
VERSION = "1.0.0"

if os.environ.get('ENV_NAME') == "test":
    config = Config(".env.test")
else:
    config = Config(".env")

LOGO: str = config("LOGO", cast=str,
                   default="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png")
DEBUG: bool = config("DEBUG", cast=bool, default=False)
DESCRIPTION: str = config("DESCRIPTION", default="Patricia Fix API")
DATABASE_URL: str = config("DB_CONNECTION", cast=str, default="")
DATABASE_HOST: str = config("DB_HOST", cast=str, default="127.0.0.1")
DATABASE_PORT: int = config("DB_PORT", cast=int, default=3306)
DATABASE_USER: str = config("DB_USER", cast=str, default="root")
DATABASE_PASSWORD: str = config("DB_PASSWORD", cast=str, default="")
DATABASE_NAME: str = config("DB_NAME", cast=str, default="")

REDIS_URL = config('REDIS_URL')
REDIS_HOST = config('REDIS_HOST')
REDIS_PORT = config('REDIS_PORT')
REDIS_DB = config('REDIS_DB')

MAX_CONNECTIONS_COUNT: int = config(
    "MAX_CONNECTIONS_COUNT", cast=int, default=10)
MIN_CONNECTIONS_COUNT: int = config(
    "MIN_CONNECTIONS_COUNT", cast=int, default=10)

PROJECT_NAME: str = config("PROJECT_NAME", default="Facial Recognition Service")
ALLOWED_HOSTS: List[str] = config(
    "ALLOWED_HOSTS",
    cast=CommaSeparatedStrings,
    default="",
)

# logging configuration

LOGGING_LEVEL = logging.DEBUG if DEBUG else logging.INFO
LOGGERS = ("uvicorn.asgi", "uvicorn.access")

logging.getLogger().handlers = [InterceptHandler()]
for logger_name in LOGGERS:
    logging_logger = logging.getLogger(logger_name)
    logging_logger.handlers = [InterceptHandler(level=LOGGING_LEVEL)]

logger.configure(handlers=[{"sink": sys.stderr, "level": LOGGING_LEVEL}])
