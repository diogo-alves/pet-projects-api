from functools import lru_cache
from typing import List

from pydantic import BaseSettings, validator
from pydantic.networks import AnyHttpUrl


class Settings(BaseSettings):
    ACCESS_TOKEN_EXPIRATION_MINUTES: int = 30
    API_PREFIX: str = '/api'
    API_V1_PREFIX: str = '/v1'
    APP_NAME: str = 'Pet Projects API'
    DATABASE_URL: str
    DEFAULT_SUPERUSER_EMAIL: str
    SECRET_KEY: str
    JWT_SIGNING_ALGORITHM: str = 'HS256'
    CORS_ALLOWED_ORIGINS: List[AnyHttpUrl] = []

    @validator('DATABASE_URL')
    def normalize_database_dialetic(cls, db_url):
        # "postgres://" dialect has been deprecated in SQLAlchemy 1.4,
        # but is still used by Heroku
        # https://github.com/sqlalchemy/sqlalchemy/issues/6083
        if db_url.startswith('postgres://'):
            db_url = db_url.replace('postgres://', 'postgresql://')
        return db_url

    class Config:
        env_file = '.env'
        case_sensitive = True


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
