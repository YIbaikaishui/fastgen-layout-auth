from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings, loaded from environment / .env."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "sqlite+aiosqlite:///./app.db"

    # Auth — override SECRET_KEY in .env (never commit a real one)
    secret_key: str = "dev-only-insecure-secret-change-me-32b+"  # >= 32 bytes for HS256
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24


settings = Settings()
