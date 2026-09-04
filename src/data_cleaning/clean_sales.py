"""
Module 1: Sales CRM Data Cleaning and Transformation.
Reads raw sales CSV files, applies documented data quality corrections,
validates integrity, and outputs cleaned CSVs to data/processed/crm_sales/.
"""
import logging
from pathlib import Path
import pandas as pd
import numpy as np
from config.settings import RAW_DATA_DIR, CRM_SALES_PROCESSED_DIR

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

def clean_accounts(raw_dir: Path, output_dir: Path) -> pd.DataFrame:
    """Clean accounts table: fix spelling mistakes and validate data types."""
    logger.info("Cleaning accounts data...")
    df = pd.read_csv(raw_dir / "accounts.csv")
    initial_len = len(df)
    
    # 1. Fix sector typo
    typo_count = (df["sector"] == "technolgy").sum()
    df["sector"] = df["sector"].replace({"technolgy": "technology"})
    logger.info(f"Corrected 'technolgy' -> 'technology' for {typo_count} rows.")
    
    # 2. Fix office_location typo
    loc_typo_count = (df["office_location"] == "Philipines").sum()
    df["office_location"] = df["office_location"].replace({"Philipines": "Philippines"})
    logger.info(f"Corrected 'Philipines' -> 'Philippines' for {loc_typo_count} rows.")
    
    # 3. Data type formatting
    df["account"] = df["account"].astype(str).str.strip()
    df["sector"] = df["sector"].astype(str).str.strip()
    df["year_established"] = df["year_established"].astype(int)
    df["revenue"] = df["revenue"].astype(float)
    df["employees"] = df["employees"].astype(int)
    df["office_location"] = df["office_location"].astype(str).str.strip()
    # subsidiary_of stays object / NaN for standalone
    
    # Validation checks
    assert len(df) == initial_len, f"Row count changed: {len(df)} != {initial_len}"
    assert df["account"].is_unique, "Primary key 'account' is not unique!"
    assert not df["account"].isna().any(), "Primary key 'account' contains NULLs!"
    
    # Self-referencing FK check
    subs = df["subsidiary_of"].dropna()
    invalid_subs = set(subs) - set(df["account"])
    assert len(invalid_subs) == 0, f"Invalid parent accounts found: {invalid_subs}"
    
    # Save processed file
    output_path = output_dir / "accounts.csv"
    df.to_csv(output_path, index=False)
    logger.info(f"Saved cleaned accounts to {output_path} ({len(df)} rows)")
    return df

def clean_products(raw_dir: Path, output_dir: Path) -> pd.DataFrame:
    """Clean and validate product catalog."""
    logger.info("Cleaning products data...")
    df = pd.read_csv(raw_dir / "products.csv")
    
    df["product"] = df["product"].astype(str).str.strip()
    df["series"] = df["series"].astype(str).str.strip()
    df["sales_price"] = df["sales_price"].astype(int)
    
    assert df["product"].is_unique, "Primary key 'product' is not unique!"
    assert not df["product"].isna().any(), "Primary key 'product' contains NULLs!"
    assert (df["sales_price"] > 0).all(), "Sales price must be positive!"
    
    output_path = output_dir / "products.csv"
    df.to_csv(output_path, index=False)
    logger.info(f"Saved cleaned products to {output_path} ({len(df)} rows)")
    return df

def clean_sales_teams(raw_dir: Path, output_dir: Path) -> pd.DataFrame:
    """Clean and validate sales teams data."""
    logger.info("Cleaning sales teams data...")
    df = pd.read_csv(raw_dir / "sales_teams.csv")
    
    df["sales_agent"] = df["sales_agent"].astype(str).str.strip()
    df["manager"] = df["manager"].astype(str).str.strip()
    df["regional_office"] = df["regional_office"].astype(str).str.strip()
    
    assert df["sales_agent"].is_unique, "Primary key 'sales_agent' is not unique!"
    assert not df["sales_agent"].isna().any(), "Primary key 'sales_agent' contains NULLs!"
    
    output_path = output_dir / "sales_teams.csv"
    df.to_csv(output_path, index=False)
    logger.info(f"Saved cleaned sales_teams to {output_path} ({len(df)} rows)")
    return df

def clean_sales_pipeline(raw_dir: Path, output_dir: Path, 
                         accounts_df: pd.DataFrame, 
                         products_df: pd.DataFrame, 
                         teams_df: pd.DataFrame) -> pd.DataFrame:
    """Clean sales pipeline opportunities, standardize product names, validate dates and RI."""
    logger.info("Cleaning sales pipeline data...")
    df = pd.read_csv(raw_dir / "sales_pipeline.csv")
    initial_len = len(df)
    
    # 1. Standardize product name "GTXPro" -> "GTX Pro"
    gtx_pro_count = (df["product"] == "GTXPro").sum()
    df["product"] = df["product"].replace({"GTXPro": "GTX Pro"})
    logger.info(f"Standardized 'GTXPro' -> 'GTX Pro' for {gtx_pro_count} rows.")
    
    # 2. Strip whitespace on string columns
    df["opportunity_id"] = df["opportunity_id"].astype(str).str.strip()
    df["sales_agent"] = df["sales_agent"].astype(str).str.strip()
    df["product"] = df["product"].astype(str).str.strip()
    df["deal_stage"] = df["deal_stage"].astype(str).str.strip()
    
    # Account: keep NaN as NaN, strip non-nulls
    df["account"] = df["account"].apply(lambda x: str(x).strip() if pd.notna(x) else np.nan)
    
    # 3. Date handling
    # Convert to datetime and then format as ISO string YYYY-MM-DD
    df["engage_date"] = pd.to_datetime(df["engage_date"], errors="coerce")
    df["close_date"] = pd.to_datetime(df["close_date"], errors="coerce")
    
    # Validate date logic:
    # - Prospecting: engage_date should be NaT (500 rows)
    prospecting_mask = df["deal_stage"] == "Prospecting"
    assert df.loc[prospecting_mask, "engage_date"].isna().all(), "Prospecting deals must have NULL engage_date"
    
    # - Engaging, Won, Lost: engage_date should be non-null (8300 rows)
    engaged_mask = df["deal_stage"].isin(["Engaging", "Won", "Lost"])
    assert df.loc[engaged_mask, "engage_date"].notna().all(), "Engaged/Won/Lost deals must have valid engage_date"
    
    # - Open deals (Prospecting, Engaging): close_date and close_value should be NaN (2089 rows)
    open_mask = df["deal_stage"].isin(["Prospecting", "Engaging"])
    assert df.loc[open_mask, "close_date"].isna().all(), "Open deals must have NULL close_date"
    assert df.loc[open_mask, "close_value"].isna().all(), "Open deals must have NULL close_value"
    
    # - Closed deals (Won, Lost): close_date should be non-null (6711 rows)
    closed_mask = df["deal_stage"].isin(["Won", "Lost"])
    assert df.loc[closed_mask, "close_date"].notna().all(), "Closed deals must have valid close_date"
    
    # - close_date must not precede engage_date
    invalid_date_order = df.loc[closed_mask, "close_date"] < df.loc[closed_mask, "engage_date"]
    assert not invalid_date_order.any(), "Found close_date before engage_date!"
    
    # - Lost deals: close_value == 0.0
    lost_mask = df["deal_stage"] == "Lost"
    assert (df.loc[lost_mask, "close_value"] == 0.0).all(), "Lost deals must have close_value == 0"
    
    # - Won deals: close_value > 0.0
    won_mask = df["deal_stage"] == "Won"
    assert (df.loc[won_mask, "close_value"] > 0.0).all(), "Won deals must have close_value > 0"
    
    # Convert dates back to string format YYYY-MM-DD for clean CSV representation (null as empty string or NaN)
    df["engage_date"] = df["engage_date"].dt.strftime("%Y-%m-%d")
    df["close_date"] = df["close_date"].dt.strftime("%Y-%m-%d")
    
    # 4. Referential Integrity Checks
    # Primary Key uniqueness
    assert len(df) == initial_len, f"Row count changed: {len(df)} != {initial_len}"
    assert df["opportunity_id"].is_unique, "opportunity_id is not unique!"
    
    # FK: sales_agent -> sales_teams
    invalid_agents = set(df["sales_agent"]) - set(teams_df["sales_agent"])
    assert len(invalid_agents) == 0, f"Orphan sales agents in pipeline: {invalid_agents}"
    
    # FK: product -> products
    invalid_products = set(df["product"]) - set(products_df["product"])
    assert len(invalid_products) == 0, f"Orphan products in pipeline: {invalid_products}"
    
    # FK: account -> accounts (for non-null accounts)
    non_null_accounts = df["account"].dropna()
    invalid_accounts = set(non_null_accounts) - set(accounts_df["account"])
    assert len(invalid_accounts) == 0, f"Orphan accounts in pipeline: {invalid_accounts}"
    
    # Save cleaned file
    output_path = output_dir / "sales_pipeline.csv"
    df.to_csv(output_path, index=False)
    logger.info(f"Saved cleaned sales_pipeline to {output_path} ({len(df)} rows)")
    return df

def run_sales_cleaning():
    """Execute complete sales data cleaning pipeline."""
    CRM_SALES_PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    accounts_df = clean_accounts(RAW_DATA_DIR, CRM_SALES_PROCESSED_DIR)
    products_df = clean_products(RAW_DATA_DIR, CRM_SALES_PROCESSED_DIR)
    teams_df = clean_sales_teams(RAW_DATA_DIR, CRM_SALES_PROCESSED_DIR)
    pipeline_df = clean_sales_pipeline(RAW_DATA_DIR, CRM_SALES_PROCESSED_DIR, 
                                       accounts_df, products_df, teams_df)
    logger.info("Sales CRM cleaning completed successfully.")
    return accounts_df, products_df, teams_df, pipeline_df

if __name__ == "__main__":
    run_sales_cleaning()
