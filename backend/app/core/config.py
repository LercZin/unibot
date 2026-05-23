from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parents[3] / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_debug: bool = False

    db_host: str = "localhost"
    db_port: int = 3306
    db_name: str = "unibot"
    db_user: str = "root"
    db_password: str = "1234"

    jwt_secret: str = "change-me"
    jwt_algorithm: str = "HS256"
    jwt_expires_min: int = 120
    jwt_expires_min_lembrar: int = 43_200  # 30 dias

    anthropic_api_key: str = ""
    claude_model: str = "claude-sonnet-4-6"
    claude_max_tokens: int = 1024

    n8n_webhook_url: str = ""

    cors_origins: list[str] = [
        "http://localhost:8080",
        "http://127.0.0.1:8080",
    ]


settings = Settings()
