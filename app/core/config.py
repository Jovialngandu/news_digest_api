from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from loguru import logger


class Settings(BaseSettings):
    # Variables obligatoires
    DATABASE_URL: str = Field(default="sqlite:///./app_data.db")
    GNEWS_API_KEY: str = Field(..., env="GNEWS_API_KEY")
    GNEWS_BASE_URL: str = Field(default="https://gnews.io/api/v4/top-headlines")
    SECRET_KEY: str = Field(..., env="SECRET_KEY")
    ALGORITHM: str = Field(default="HS256", env="ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30, env="ACCESS_TOKEN_EXPIRE_MINUTES")

    model_config = SettingsConfigDict(
        env_file=".env", 
        extra="ignore", 
        case_sensitive=True
    )

# Instanciation unique
try:
    settings = Settings()
except Exception as e:
    logger.critical(f" CONFIG ERROR: {e}")
    raise SystemExit(1)