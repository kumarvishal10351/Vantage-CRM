"""
PostgreSQL Database Initialization and Data Loader.
Creates 'crm_platform' database, schemas, tables, and loads cleaned data
from data/processed/ into PostgreSQL with full transaction control and logging.
"""
import logging
from pathlib import Path
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import pandas as pd

from config.settings import (
    DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD,
    CRM_SALES_PROCESSED_DIR, BASE_DIR
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

def create_database_if_not_exists():
    """Connect to default 'postgres' database and create target database if needed."""
    logger.info(f"Checking if database '{DB_NAME}' exists...")
    conn = psycopg2.connect(
        host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASSWORD, dbname="postgres"
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    
    cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (DB_NAME,))
    exists = cur.fetchone()
    if not exists:
        logger.info(f"Creating database '{DB_NAME}'...")
        cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(DB_NAME)))
        logger.info(f"Database '{DB_NAME}' created successfully.")
    else:
        logger.info(f"Database '{DB_NAME}' already exists.")
        
    cur.close()
    conn.close()

def apply_ddl_scripts(conn):
    """Execute DDL scripts to create crm_sales schema, tables, constraints, and indexes."""
    logger.info("Executing DDL scripts...")
    cur = conn.cursor()
    
    ddl_dir = BASE_DIR / "sql" / "ddl"
    sales_ddl_path = ddl_dir / "crm_sales_schema.sql"
    
    with open(sales_ddl_path, "r", encoding="utf-8") as f:
        sales_sql = f.read()
    cur.execute(sales_sql)
    logger.info("Applied crm_sales schema DDL.")
    
    auth_ddl_path = ddl_dir / "crm_auth_schema.sql"
    if auth_ddl_path.exists():
        with open(auth_ddl_path, "r", encoding="utf-8") as f:
            auth_sql = f.read()
        cur.execute(auth_sql)
        logger.info("Applied crm_auth schema DDL.")
    
    conn.commit()
    cur.close()

def load_accounts(conn, csv_path: Path):
    """Load crm_sales.accounts data."""
    logger.info("Loading crm_sales.accounts...")
    df = pd.read_csv(csv_path)
    cur = conn.cursor()
    
    insert_sql = """
        INSERT INTO crm_sales.accounts 
        (account, sector, year_established, revenue, employees, office_location, subsidiary_of)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    records = []
    for _, row in df.iterrows():
        records.append((
            row["account"],
            row["sector"],
            int(row["year_established"]),
            float(row["revenue"]),
            int(row["employees"]),
            row["office_location"],
            None  # temporary
        ))
    
    cur.executemany(insert_sql, records)
    
    # Now update subsidiary_of
    update_sql = """
        UPDATE crm_sales.accounts
        SET subsidiary_of = %s
        WHERE account = %s
    """
    updates = []
    for _, row in df[df["subsidiary_of"].notna()].iterrows():
        updates.append((row["subsidiary_of"], row["account"]))
    cur.executemany(update_sql, updates)
    
    conn.commit()
    cur.close()
    logger.info(f"Loaded {len(df)} records into crm_sales.accounts.")

def load_products(conn, csv_path: Path):
    """Load crm_sales.products data."""
    logger.info("Loading crm_sales.products...")
    df = pd.read_csv(csv_path)
    cur = conn.cursor()
    
    insert_sql = """
        INSERT INTO crm_sales.products (product, series, sales_price)
        VALUES (%s, %s, %s)
    """
    records = [
        (row["product"], row["series"], float(row["sales_price"]))
        for _, row in df.iterrows()
    ]
    cur.executemany(insert_sql, records)
    conn.commit()
    cur.close()
    logger.info(f"Loaded {len(df)} records into crm_sales.products.")

def load_sales_teams(conn, csv_path: Path):
    """Load crm_sales.sales_teams data."""
    logger.info("Loading crm_sales.sales_teams...")
    df = pd.read_csv(csv_path)
    cur = conn.cursor()
    
    insert_sql = """
        INSERT INTO crm_sales.sales_teams (sales_agent, manager, regional_office)
        VALUES (%s, %s, %s)
    """
    records = [
        (row["sales_agent"], row["manager"], row["regional_office"])
        for _, row in df.iterrows()
    ]
    cur.executemany(insert_sql, records)
    conn.commit()
    cur.close()
    logger.info(f"Loaded {len(df)} records into crm_sales.sales_teams.")

def load_sales_pipeline(conn, csv_path: Path):
    """Load crm_sales.sales_pipeline data."""
    logger.info("Loading crm_sales.sales_pipeline...")
    df = pd.read_csv(csv_path)
    cur = conn.cursor()
    
    insert_sql = """
        INSERT INTO crm_sales.sales_pipeline 
        (opportunity_id, sales_agent, product, account, deal_stage, engage_date, close_date, close_value)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    records = []
    for _, row in df.iterrows():
        records.append((
            row["opportunity_id"],
            row["sales_agent"],
            row["product"],
            row["account"] if pd.notna(row["account"]) else None,
            row["deal_stage"],
            row["engage_date"] if pd.notna(row["engage_date"]) else None,
            row["close_date"] if pd.notna(row["close_date"]) else None,
            float(row["close_value"]) if pd.notna(row["close_value"]) else None,
        ))
        
    cur.executemany(insert_sql, records)
    conn.commit()
    cur.close()
    logger.info(f"Loaded {len(df)} records into crm_sales.sales_pipeline.")

def run_database_pipeline():
    """Execute complete database creation, schema creation, and data loading."""
    create_database_if_not_exists()
    
    conn = psycopg2.connect(
        host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASSWORD, dbname=DB_NAME
    )
    
    try:
        apply_ddl_scripts(conn)
        load_accounts(conn, CRM_SALES_PROCESSED_DIR / "accounts.csv")
        load_products(conn, CRM_SALES_PROCESSED_DIR / "products.csv")
        load_sales_teams(conn, CRM_SALES_PROCESSED_DIR / "sales_teams.csv")
        load_sales_pipeline(conn, CRM_SALES_PROCESSED_DIR / "sales_pipeline.csv")
        logger.info("All CRM sales tables loaded successfully into PostgreSQL.")
    finally:
        conn.close()

if __name__ == "__main__":
    run_database_pipeline()

