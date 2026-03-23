from pydantic_settings import BaseSettings
from functools import lru_cache
import os


class Settings(BaseSettings):
    app_name: str = "Chess Tutor API"
    app_version: str = "0.1.0"
    debug: bool = os.getenv("DEBUG", "true").lower() == "true"
    frontend_url: str = os.getenv("FRONTEND_URL", "http://localhost:3000")
    api_prefix: str = "/api"

    @property
    def allowed_origins(self) -> list[str]:
        origins = [
            "http://localhost:3000",
            "http://127.0.0.1:3000",
        ]
        if self.frontend_url and self.frontend_url not in origins:
            origins.append(self.frontend_url)
        return origins

    class Config:
        env_file = ".env"
        extra = "ignore"


@lru_cache
def get_settings() -> Settings:
    return Settings()

