from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Variables obligatoires
    DATABASE_URL: str = Field(default="sqlite:///./app_data.db")
    GNEWS_API_KEY: str = Field(..., env="GNEWS_API_KEY")
    GNEWS_BASE_URL: str = Field(default="https://gnews.io/api/v4/top-headlines")

    model_config = SettingsConfigDict(
        env_file=".env", 
        extra="ignore", 
        case_sensitive=True
    )

# Instanciation unique
try:
    settings = Settings()
except Exception as e:
    print(f"CRITICAL CONFIG ERROR: {e}")
    raise SystemExit(1)