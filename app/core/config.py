from pydantic import ValidationInfo, field_validator, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(case_sensitive=True)

    PROJECT_NAME: str = "FastAPI Starter Kit"
    PROJECT_DESC: str = "A starter kit for FastAPI with SQLAlchemy"
    API_V1_PREFIX: str = "/api/v1"
    DEBUG: bool = False
    # CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    CORS_ORIGINS: str | list[str] = ["127.0.0.1", "0.0.0.0"]

    REDIS_HOST: str = "redis"
    REDIS_PORT: str = "6379"
    REDIS_PASS: str = ""

    DB_HOST: str = "database"
    DB_PORT: int = 5432
    DB_NAME: str = Field(alias="POSTGRES_DB")
    DB_USERNAME: str = Field(alias="POSTGRES_USER")
    DB_PASSWORD: str = Field(alias="POSTGRES_PASSWORD")
    DB_URL: str = ""

    TIME_ZONE: str = "Asia/Dhaka"
    LOG_LEVEL: str = "DEBUG"
    LOG_FORMAT: str = (
        "time: %(asctime)s | level: %(levelname)s | request_id: %(request_id)s | "
        "user_host: %(user_host)s | user_agent: %(user_agent)s | path: %(path)s | method: %(method)s | "
        "request_data: %(request_data)s | response_data: %(response_data)s | "
        "response_time: %(response_time)s | response_code: %(response_code)s | "
        "message: %(message)s"
    )

    @field_validator("DB_URL", mode="before")
    def prepare_db_url(cls, value, info: ValidationInfo):
        return (
            f"postgresql+asyncpg://{info.data.get('DB_USERNAME')}:{info.data.get('DB_PASSWORD')}"
            f"@{info.data.get('DB_HOST')}:{info.data.get('DB_PORT')}/{info.data.get('DB_NAME')}"
        )

    @field_validator("CORS_ORIGINS")
    def assemble_cors_origins(cls, v: str | list[str]):
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, list):
            return v
        raise ValueError(v)

    @field_validator("LOG_LEVEL")
    def validate_log_level(cls, v: str):
        if v not in [
            "TRACE",
            "DEBUG",
            "INFO",
            "SUCCESS",
            "WARNING",
            "ERROR",
            "CRITICAL",
        ]:
            raise ValueError(
                "Should be one of these value: 'TRACE', 'DEBUG', 'INFO', 'SUCCESS', "
                "'WARNING', 'ERROR', 'CRITICAL'"
            )
        return v


settings = Settings()
