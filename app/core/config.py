from pydantic import BaseSettings


class Settings(BaseSettings):
    ACCESS_TOKEN_EXPIRATION_MINUTES: int
    API_PREFIX: str = '/api'
    API_V1_PREFIX: str = '/v1'
    APP_NAME: str = 'Pet Projects API'
    DATABASE_URL: str
    DEFAULT_SUPERUSER_EMAIL: str
    SECRET_KEY: str

    class Config:
        env_file = '.env'
        case_sensitive = True


settings = Settings()
