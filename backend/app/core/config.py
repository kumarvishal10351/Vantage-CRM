import os
import urllib.parse
from pathlib import Path
from typing import List, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

COMPROMISED_DEFAULT_SECRET = "crm-super-secret-production-key-change-in-env-2026"

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="allow")

    PROJECT_NAME: str = "Vantage — Enterprise Revenue Operations Platform"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Base directory
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent.parent
    
    # Database
    DATABASE_URL: Optional[str] = os.getenv("DATABASE_URL")
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: int = int(os.getenv("DB_PORT", 5432))
    DB_NAME: str = os.getenv("DB_NAME", "crm_platform")
    DB_USER: str = os.getenv("DB_USER", "postgres")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "")

    # Connection pooling (optimized for Render free/starter tiers)
    DB_POOL_SIZE: int = int(os.getenv("DB_POOL_SIZE", 5))
    DB_MAX_OVERFLOW: int = int(os.getenv("DB_MAX_OVERFLOW", 10))
    DB_POOL_TIMEOUT: int = int(os.getenv("DB_POOL_TIMEOUT", 30))
    
    # Security
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", COMPROMISED_DEFAULT_SECRET)
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours
    
    # CORS Configuration
    CORS_ORIGINS: str = os.getenv("CORS_ORIGINS", "")
    
    # Operational constants
    SNAPSHOT_REFERENCE_DATE: str = "2017-12-31"

    def model_post_init(self, __context) -> None:
        """Validate security posture upon configuration initialization."""
        if self.ENVIRONMENT.lower() == "production":
            if not self.JWT_SECRET_KEY or self.JWT_SECRET_KEY == COMPROMISED_DEFAULT_SECRET:
                raise ValueError(
                    "Production environment detected! JWT_SECRET_KEY must be explicitly set "
                    "via environment variables to a unique, uncompromised secret."
                )

    @property
    def sqlalchemy_database_uri(self) -> str:
        """
        Return the primary SQLAlchemy connection URI.
        Prefers DATABASE_URL (standard on Render/cloud hosting) if present,
        otherwise constructs URI from individual parameters.
        Normalizes legacy 'postgres://' schema to 'postgresql://'.
        """
        if self.DATABASE_URL:
            url = self.DATABASE_URL.strip()
            if url.startswith("postgres://"):
                url = "postgresql://" + url[len("postgres://"):]
            return url

        user = urllib.parse.quote_plus(self.DB_USER)
        password = urllib.parse.quote_plus(self.DB_PASSWORD)
        return f"postgresql://{user}:{password}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def cors_origins_list(self) -> List[str]:
        """Parse comma-separated CORS origins while preserving local development defaults."""
        defaults = [
            "http://localhost:5173",
            "http://127.0.0.1:5173",
            "http://localhost:3000",
            "http://127.0.0.1:3000",
            "http://localhost:8000",
            "http://127.0.0.1:8000",
        ]
        if self.CORS_ORIGINS:
            custom_origins = [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]
            return list(set(defaults + custom_origins))
        return defaults

settings = Settings()
