import os
import urllib.parse
from pathlib import Path
from dotenv import load_dotenv

# Base project directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Load .env file
load_dotenv(BASE_DIR / ".env")

# Data directories
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
CRM_SALES_PROCESSED_DIR = PROCESSED_DATA_DIR / "crm_sales"

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", 5432))
DB_NAME = os.getenv("DB_NAME", "crm_platform")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")

def get_db_url(dbname: str = None) -> str:
    """Return SQLAlchemy database connection URL with properly escaped credentials."""
    if DATABASE_URL and not dbname:
        url = DATABASE_URL.strip()
        if url.startswith("postgres://"):
            url = "postgresql://" + url[len("postgres://"):]
        return url

    target_db = dbname or DB_NAME
    encoded_user = urllib.parse.quote_plus(DB_USER)
    encoded_password = urllib.parse.quote_plus(DB_PASSWORD)
    return f"postgresql://{encoded_user}:{encoded_password}@{DB_HOST}:{DB_PORT}/{target_db}"

def get_db_params(dbname: str = None) -> dict:
    """Return psycopg2 connection parameters."""
    return {
        "host": DB_HOST,
        "port": DB_PORT,
        "dbname": dbname or DB_NAME,
        "user": DB_USER,
        "password": DB_PASSWORD,
    }
