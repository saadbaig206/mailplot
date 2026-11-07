from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "mailpilot-development-secret-key-change-in-production-min32bytes"
    ALLOWED_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]

    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./mailpilot_dev.db"
    SYNC_DATABASE_URL: str = "sqlite:///./mailpilot_dev.db"

    # Token Encryption Key (Base64-encoded 32-byte key for Fernet / AES-GCM)
    ENCRYPTION_KEY: str = "dGhpcy1pcy1hLTMyLWJ5dGUtZW5jcnlwdGlvbi1rZXkxMjM="

    # Application Authentication (Managed OIDC)
    OIDC_ISSUER: str = "https://auth.mailpilot.local/"
    OIDC_AUDIENCE: str = "mailpilot-api"
    OIDC_JWKS_URI: str = "https://auth.mailpilot.local/.well-known/jwks.json"
    ENABLE_DEV_MOCK_AUTH: bool = True

    # Google OAuth
    GOOGLE_CLIENT_ID: str = "mock-google-client-id"
    GOOGLE_CLIENT_SECRET: str = "mock-google-client-secret"
    GOOGLE_REDIRECT_URI: str = "http://localhost:8000/api/v1/oauth/google/callback"

    # Microsoft OAuth
    MICROSOFT_CLIENT_ID: str = "mock-microsoft-client-id"
    MICROSOFT_CLIENT_SECRET: str = "mock-microsoft-client-secret"
    MICROSOFT_TENANT_ID: str = "common"
    MICROSOFT_REDIRECT_URI: str = "http://localhost:8000/api/v1/oauth/microsoft/callback"


@lru_cache
def get_settings() -> Settings:
    return Settings()
