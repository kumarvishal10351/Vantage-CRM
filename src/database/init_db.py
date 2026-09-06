"""
Idempotent Database Initialization & Migration Utility.

Safely initializes schemas, tables, indexes, and seed datasets without
destructive DROP TABLE or CASCADE statements. Guaranteed zero data loss
on existing databases.
"""

import sys
import logging
from pathlib import Path

# Ensure repository root is in sys.path for direct CLI execution
REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import pandas as pd

from backend.app.core.config import settings

logger = logging.getLogger("src.database.init_db")

BASE_DIR = settings.BASE_DIR
PROCESSED_DIR = BASE_DIR / "data" / "processed" / "crm_sales"


def get_connection():
    """Establish psycopg2 connection using either DATABASE_URL or individual parameters."""
    if settings.DATABASE_URL:
        url = settings.DATABASE_URL.strip()
        # psycopg2 accepts postgresql:// or postgres://
        return psycopg2.connect(url)
    
    return psycopg2.connect(
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        user=settings.DB_USER,
        password=settings.DB_PASSWORD,
        dbname=settings.DB_NAME,
    )


DDL_SCHEMA = """
CREATE SCHEMA IF NOT EXISTS crm_sales;

CREATE TABLE IF NOT EXISTS crm_sales.accounts (
    account VARCHAR(100) PRIMARY KEY,
    sector VARCHAR(50) NOT NULL,
    year_established INTEGER NOT NULL,
    revenue NUMERIC(12, 2) NOT NULL,
    employees INTEGER NOT NULL,
    office_location VARCHAR(100) NOT NULL,
    subsidiary_of VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS crm_sales.products (
    product VARCHAR(50) PRIMARY KEY,
    series VARCHAR(20) NOT NULL,
    sales_price NUMERIC(10, 2) NOT NULL
);

CREATE TABLE IF NOT EXISTS crm_sales.sales_teams (
    sales_agent VARCHAR(100) PRIMARY KEY,
    manager VARCHAR(100) NOT NULL,
    regional_office VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS crm_sales.sales_pipeline (
    opportunity_id VARCHAR(50) PRIMARY KEY,
    sales_agent VARCHAR(100) NOT NULL,
    product VARCHAR(50) NOT NULL,
    account VARCHAR(100),
    deal_stage VARCHAR(20) NOT NULL,
    engage_date DATE,
    close_date DATE,
    close_value NUMERIC(12, 2)
);

CREATE TABLE IF NOT EXISTS crm_sales.app_users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    role VARCHAR(20) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_accounts_sector ON crm_sales.accounts(sector);
CREATE INDEX IF NOT EXISTS idx_accounts_location ON crm_sales.accounts(office_location);
CREATE INDEX IF NOT EXISTS idx_products_series ON crm_sales.products(series);
CREATE INDEX IF NOT EXISTS idx_sales_teams_manager ON crm_sales.sales_teams(manager);
CREATE INDEX IF NOT EXISTS idx_sales_teams_region ON crm_sales.sales_teams(regional_office);
CREATE INDEX IF NOT EXISTS idx_pipeline_stage ON crm_sales.sales_pipeline(deal_stage);
CREATE INDEX IF NOT EXISTS idx_pipeline_agent ON crm_sales.sales_pipeline(sales_agent);
CREATE INDEX IF NOT EXISTS idx_pipeline_product ON crm_sales.sales_pipeline(product);
CREATE INDEX IF NOT EXISTS idx_pipeline_account ON crm_sales.sales_pipeline(account);
CREATE INDEX IF NOT EXISTS idx_pipeline_engage_dt ON crm_sales.sales_pipeline(engage_date);
CREATE INDEX IF NOT EXISTS idx_pipeline_close_dt ON crm_sales.sales_pipeline(close_date);
CREATE INDEX IF NOT EXISTS idx_app_users_email ON crm_sales.app_users(email);
CREATE INDEX IF NOT EXISTS idx_app_users_role ON crm_sales.app_users(role);
"""

SEED_USERS_SQL = """
INSERT INTO crm_sales.app_users (email, hashed_password, full_name, role)
VALUES
    ('admin@crm.local', '$2b$12$C.FAhA8gjKX8HFyOD1FD/.0Y0o1Xx9Z6/ea4O97mHNTHLYdQrCAfm', 'System Administrator', 'Admin'),
    ('manager@crm.local', '$2b$12$GPevExrGxE77/L7xId1t.ukpNh1IHF926SY0ZOYlWj9wM1hp3z.BG', 'Sales Operations Manager', 'Sales Manager'),
    ('agent@crm.local', '$2b$12$iwMQpFiJLYdmjKCZzAwAs.qIMdG5Q2JNoLq.i53ieeNZ.dONGUIFC', 'Sales Representative', 'Sales Agent')
ON CONFLICT (email) DO NOTHING;
"""


def seed_data_if_empty(conn):
    """Populates CRM tables from processed CSV datasets only if tables are unpopulated."""
    cur = conn.cursor()
    
    # Check accounts
    cur.execute("SELECT COUNT(*) FROM crm_sales.accounts;")
    acc_count = cur.fetchone()[0]
    
    if acc_count == 0 and PROCESSED_DIR.exists():
        logger.info("Initializing database with seed CRM datasets...")
        
        # 1. Accounts
        accounts_csv = PROCESSED_DIR / "accounts.csv"
        if accounts_csv.exists():
            df_acc = pd.read_csv(accounts_csv)
            insert_acc = """
                INSERT INTO crm_sales.accounts 
                (account, sector, year_established, revenue, employees, office_location, subsidiary_of)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (account) DO NOTHING;
            """
            records = []
            for _, r in df_acc.iterrows():
                sub = r["subsidiary_of"] if pd.notna(r["subsidiary_of"]) else None
                records.append((
                    r["account"], r["sector"], int(r["year_established"]),
                    float(r["revenue"]), int(r["employees"]), r["office_location"], sub
                ))
            cur.executemany(insert_acc, records)
            logger.info(f"Seeded {len(records)} accounts.")

        # 2. Products
        products_csv = PROCESSED_DIR / "products.csv"
        if products_csv.exists():
            df_prod = pd.read_csv(products_csv)
            insert_prod = """
                INSERT INTO crm_sales.products (product, series, sales_price)
                VALUES (%s, %s, %s)
                ON CONFLICT (product) DO NOTHING;
            """
            records = [
                (r["product"], r["series"], float(r["sales_price"]))
                for _, r in df_prod.iterrows()
            ]
            cur.executemany(insert_prod, records)
            logger.info(f"Seeded {len(records)} products.")

        # 3. Sales Teams
        teams_csv = PROCESSED_DIR / "sales_teams.csv"
        if teams_csv.exists():
            df_teams = pd.read_csv(teams_csv)
            insert_team = """
                INSERT INTO crm_sales.sales_teams (sales_agent, manager, regional_office)
                VALUES (%s, %s, %s)
                ON CONFLICT (sales_agent) DO NOTHING;
            """
            records = [
                (r["sales_agent"], r["manager"], r["regional_office"])
                for _, r in df_teams.iterrows()
            ]
            cur.executemany(insert_team, records)
            logger.info(f"Seeded {len(records)} sales personnel.")

        # 4. Sales Pipeline
        pipeline_csv = PROCESSED_DIR / "sales_pipeline.csv"
        if pipeline_csv.exists():
            df_pipe = pd.read_csv(pipeline_csv)
            insert_pipe = """
                INSERT INTO crm_sales.sales_pipeline 
                (opportunity_id, sales_agent, product, account, deal_stage, engage_date, close_date, close_value)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (opportunity_id) DO NOTHING;
            """
            records = []
            for _, r in df_pipe.iterrows():
                acc = r["account"] if pd.notna(r["account"]) else None
                eng = r["engage_date"] if pd.notna(r["engage_date"]) else None
                cls = r["close_date"] if pd.notna(r["close_date"]) else None
                val = float(r["close_value"]) if pd.notna(r["close_value"]) else None
                records.append((
                    r["opportunity_id"], r["sales_agent"], r["product"],
                    acc, r["deal_stage"], eng, cls, val
                ))
            cur.executemany(insert_pipe, records)
            logger.info(f"Seeded {len(records)} sales opportunities.")

        conn.commit()
    else:
        logger.info(f"Database already populated ({acc_count} accounts found). Skipping data seed.")

    # Check app users
    cur.execute(SEED_USERS_SQL)
    conn.commit()
    cur.close()


def initialize_database():
    """Main entry point for idempotent schema and seed initialization."""
    logger.info("Verifying PostgreSQL database schema readiness...")
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(DDL_SCHEMA)
        conn.commit()
        cur.close()
        logger.info("DDL schema validation complete.")
        
        seed_data_if_empty(conn)
        logger.info("Database initialization completed successfully.")
    finally:
        conn.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
    initialize_database()
