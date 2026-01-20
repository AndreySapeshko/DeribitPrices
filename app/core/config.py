from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str
    DERIBIT_BASE_URL: str

    class Config:
        env_file = ".env"
        extra = "ignore"

    @property
    def database_url(self):
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:"
            f"{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:"
            f"{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )


settings = Settings()
