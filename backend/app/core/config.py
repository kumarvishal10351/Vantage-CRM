import os
import urllib.parse
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="allow")

    PROJECT_NAME: str = "Sales CRM & Pipeline Management Platform"
    API_V1_STR: str = "/api/v1"
    
    # Base directory
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent.parent
    
    # Database
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: int = int(os.getenv("DB_PORT", 5432))
    DB_NAME: str = os.getenv("DB_NAME", "crm_platform")
    DB_USER: str = os.getenv("DB_USER", "postgres")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "")
    
    # Security
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "crm-super-secret-production-key-change-in-env-2026")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours
    
    # Operational constants
    SNAPSHOT_REFERENCE_DATE: str = "2017-12-31"

    @property
    def sqlalchemy_database_uri(self) -> str:
        user = urllib.parse.quote_plus(self.DB_USER)
        password = urllib.parse.quote_plus(self.DB_PASSWORD)
        return f"postgresql://{user}:{password}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

settings = Settings()
