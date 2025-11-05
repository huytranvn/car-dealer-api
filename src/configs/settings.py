from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str = Field("postgresql://localhost/snorlax")
    SECRET_KEY: str = Field("your-secret-key-change-this-in-production", description="Secret key for JWT token signing")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )


settings = Settings()