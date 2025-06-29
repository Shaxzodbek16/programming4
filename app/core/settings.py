from functools import cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # API
    API_V1_STR: str
    BASE_URL: str

    # PROJECT METADATA
    PROJECT_NAME: str
    PROJECT_DESCRIPTION: str
    PROJECT_VERSION: str

    # POSTGRES CREDENTIALS
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_DATABASE: str

    TEST_POSTGRES_USER: str
    TEST_POSTGRES_PASSWORD: str
    TEST_POSTGRES_HOST: str
    TEST_POSTGRES_PORT: str
    TEST_POSTGRES_DATABASE: str

    # REDIS CREDENTIALS
    REDIS_HOST: str
    REDIS_PORT: str
    REDIS_DB: str

    # JWT CREDENTIALS
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_MINUTES: int

    # EMAIL CREDENTIALS
    EMAIL_PASSWORD: str
    EMAIL: str
    SMTP_PORT: int
    SMTP_SERVER: str

    model_config = SettingsConfigDict(env_file=".env")

    @property
    def get_postgres_url(self) -> str:
        return f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DATABASE}"

    @property
    def get_redis_url(self) -> str:
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"

    @property
    def get_test_database_url(self) -> str:
        return f"{self.TEST_POSTGRES_USER}:{self.TEST_POSTGRES_PASSWORD}@{self.TEST_POSTGRES_HOST}:{self.TEST_POSTGRES_PORT}/{self.TEST_POSTGRES_DATABASE}"


@cache
def get_settings() -> Settings:
    return Settings()  # noqa
