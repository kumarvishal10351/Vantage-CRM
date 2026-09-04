"""
Phase 2 CRM Automated Validation Test Suite.
Validates raw immutability, processed file existence, PostgreSQL crm_sales schema,
table structures, constraints, row counts, referential integrity,
and data quality transformations.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import psycopg2
import pandas as pd

from config.settings import (
    DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD,
    RAW_DATA_DIR, CRM_SALES_PROCESSED_DIR
)

def run_phase2_validation():
    print("=" * 80)
    print("PHASE 2 CRM COMPREHENSIVE VALIDATION")
    print("=" * 80)
    
    results = []
    
    def check(name: str, condition: bool, details: str = ""):
        status = "PASS" if condition else "FAIL"
        results.append((name, status, details))
        detail_str = f" ({details})" if details else ""
        print(f"  [{status}] {name}{detail_str}")
        return condition

    # ------------------------------------------------------------------------
    # 1. Raw Files Immutability & Existence
    # ------------------------------------------------------------------------
    print("\n--- 1. Raw Files Audit ---")
    raw_files = [
        "sales_pipeline.csv", "accounts.csv", "products.csv",
        "sales_teams.csv", "data_dictionary.csv"
    ]
    for rf in raw_files:
        p = RAW_DATA_DIR / rf
        check(f"Raw file exists: {rf}", p.exists() and p.stat().st_size > 0)
        
    # Check that raw accounts still has the typo (proving raw is untouched)
    raw_acc = pd.read_csv(RAW_DATA_DIR / "accounts.csv")
    check("Raw accounts.csv is untouched (retains 'technolgy')", (raw_acc["sector"] == "technolgy").sum() == 12)
    check("Raw accounts.csv is untouched (retains 'Philipines')", (raw_acc["office_location"] == "Philipines").sum() == 1)
    
    raw_sp = pd.read_csv(RAW_DATA_DIR / "sales_pipeline.csv")
    check("Raw sales_pipeline.csv is untouched (retains 'GTXPro')", (raw_sp["product"] == "GTXPro").sum() == 1480)

    # ------------------------------------------------------------------------
    # 2. Processed Files Existence & Structure
    # ------------------------------------------------------------------------
    print("\n--- 2. Processed Files Audit ---")
    proc_files = {
        CRM_SALES_PROCESSED_DIR / "accounts.csv": 85,
        CRM_SALES_PROCESSED_DIR / "products.csv": 7,
        CRM_SALES_PROCESSED_DIR / "sales_teams.csv": 35,
        CRM_SALES_PROCESSED_DIR / "sales_pipeline.csv": 8800,
        CRM_SALES_PROCESSED_DIR / "prioritized_open_opportunities.csv": 2089,
    }
    for path, expected_rows in proc_files.items():
        exists = path.exists()
        if exists:
            df = pd.read_csv(path)
            row_match = len(df) == expected_rows
            check(f"Processed file {path.name} exists with {expected_rows} rows", exists and row_match, f"got {len(df)} rows")
        else:
            check(f"Processed file {path.name} exists", False)

    # ------------------------------------------------------------------------
    # 3. PostgreSQL Database & Schema Audit
    # ------------------------------------------------------------------------
    print("\n--- 3. PostgreSQL Database & Schema Audit ---")
    conn = psycopg2.connect(
        host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASSWORD, dbname=DB_NAME
    )
    cur = conn.cursor()
    
    # Schemas
    cur.execute("SELECT schema_name FROM information_schema.schemata WHERE schema_name = 'crm_sales'")
    schemas = [r[0] for r in cur.fetchall()]
    check("Schema 'crm_sales' exists", "crm_sales" in schemas)
    
    # Tables
    expected_tables = {
        ("crm_sales", "accounts"): 85,
        ("crm_sales", "products"): 7,
        ("crm_sales", "sales_teams"): 35,
        ("crm_sales", "sales_pipeline"): 8800,
    }
    for (schema, table), expected_count in expected_tables.items():
        cur.execute(f"SELECT COUNT(*) FROM {schema}.{table}")
        actual_count = cur.fetchone()[0]
        check(f"Table {schema}.{table} count == {expected_count}", actual_count == expected_count, f"actual={actual_count}")

    # ------------------------------------------------------------------------
    # 4. Primary Key & Unique Constraints
    # ------------------------------------------------------------------------
    print("\n--- 4. Primary Key Integrity ---")
    pk_checks = [
        ("crm_sales.accounts", "account"),
        ("crm_sales.products", "product"),
        ("crm_sales.sales_teams", "sales_agent"),
        ("crm_sales.sales_pipeline", "opportunity_id"),
    ]
    for table, col in pk_checks:
        cur.execute(f"SELECT COUNT({col}) - COUNT(DISTINCT {col}) FROM {table}")
        dup_count = cur.fetchone()[0]
        cur.execute(f"SELECT COUNT(*) FROM {table} WHERE {col} IS NULL")
        null_count = cur.fetchone()[0]
        check(f"PK {table}.{col} has 0 duplicates and 0 nulls", dup_count == 0 and null_count == 0)

    # ------------------------------------------------------------------------
    # 5. Referential Integrity in PostgreSQL
    # ------------------------------------------------------------------------
    print("\n--- 5. Referential Integrity Audit ---")
    
    # Pipeline -> Teams
    cur.execute("""
        SELECT COUNT(*) FROM crm_sales.sales_pipeline sp
        LEFT JOIN crm_sales.sales_teams st ON sp.sales_agent = st.sales_agent
        WHERE st.sales_agent IS NULL
    """)
    orphan_agents = cur.fetchone()[0]
    check("Zero orphan sales agents in sales_pipeline", orphan_agents == 0)
    
    # Pipeline -> Products
    cur.execute("""
        SELECT COUNT(*) FROM crm_sales.sales_pipeline sp
        LEFT JOIN crm_sales.products pr ON sp.product = pr.product
        WHERE pr.product IS NULL
    """)
    orphan_products = cur.fetchone()[0]
    check("Zero orphan products in sales_pipeline", orphan_products == 0)
    
    # Pipeline -> Accounts (non-null)
    cur.execute("""
        SELECT COUNT(*) FROM crm_sales.sales_pipeline sp
        LEFT JOIN crm_sales.accounts acc ON sp.account = acc.account
        WHERE sp.account IS NOT NULL AND acc.account IS NULL
    """)
    orphan_accounts = cur.fetchone()[0]
    check("Zero orphan accounts in sales_pipeline (non-null)", orphan_accounts == 0)
    
    # Accounts self-reference (non-null)
    cur.execute("""
        SELECT COUNT(*) FROM crm_sales.accounts a
        LEFT JOIN crm_sales.accounts p ON a.subsidiary_of = p.account
        WHERE a.subsidiary_of IS NOT NULL AND p.account IS NULL
    """)
    orphan_parents = cur.fetchone()[0]
    check("Zero orphan parent accounts in accounts.subsidiary_of", orphan_parents == 0)

    # ------------------------------------------------------------------------
    # 6. Nullability & Business Logic Checks
    # ------------------------------------------------------------------------
    print("\n--- 6. Nullability & Business Logic Checks ---")
    
    # Missing account in sales_pipeline
    cur.execute("SELECT COUNT(*) FROM crm_sales.sales_pipeline WHERE account IS NULL")
    null_accounts = cur.fetchone()[0]
    check("Expected 1,425 NULL accounts in sales_pipeline", null_accounts == 1425)
    
    # Missing engage_date in sales_pipeline
    cur.execute("SELECT COUNT(*) FROM crm_sales.sales_pipeline WHERE engage_date IS NULL")
    null_engage = cur.fetchone()[0]
    check("Expected 500 NULL engage_date in sales_pipeline (Prospecting)", null_engage == 500)
    
    # Missing close_date in sales_pipeline
    cur.execute("SELECT COUNT(*) FROM crm_sales.sales_pipeline WHERE close_date IS NULL")
    null_close_dt = cur.fetchone()[0]
    check("Expected 2,089 NULL close_date in sales_pipeline (open deals)", null_close_dt == 2089)
    
    # Missing close_value in sales_pipeline
    cur.execute("SELECT COUNT(*) FROM crm_sales.sales_pipeline WHERE close_value IS NULL")
    null_close_val = cur.fetchone()[0]
    check("Expected 2,089 NULL close_value in sales_pipeline (open deals)", null_close_val == 2089)
    
    # Date ordering for closed deals
    cur.execute("SELECT COUNT(*) FROM crm_sales.sales_pipeline WHERE close_date < engage_date")
    invalid_dates = cur.fetchone()[0]
    check("Zero records with close_date < engage_date", invalid_dates == 0)
    
    # Lost deals value == 0
    cur.execute("SELECT COUNT(*) FROM crm_sales.sales_pipeline WHERE deal_stage = 'Lost' AND close_value != 0")
    bad_lost = cur.fetchone()[0]
    check("All 2,473 Lost deals have close_value == 0.0", bad_lost == 0)
    
    # Won deals value > 0
    cur.execute("SELECT COUNT(*) FROM crm_sales.sales_pipeline WHERE deal_stage = 'Won' AND (close_value IS NULL OR close_value <= 0)")
    bad_won = cur.fetchone()[0]
    check("All 4,238 Won deals have close_value > 0.0", bad_won == 0)

    # ------------------------------------------------------------------------
    # 7. Data Quality Transformations Verified in DB
    # ------------------------------------------------------------------------
    print("\n--- 7. Data Quality Transformations Verification ---")
    
    # Sector typo fix
    cur.execute("SELECT COUNT(*) FROM crm_sales.accounts WHERE sector = 'technolgy'")
    bad_sector = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM crm_sales.accounts WHERE sector = 'technology'")
    good_sector = cur.fetchone()[0]
    check("Sector 'technolgy' typo corrected to 'technology'", bad_sector == 0 and good_sector == 12)
    
    # Office location typo fix
    cur.execute("SELECT COUNT(*) FROM crm_sales.accounts WHERE office_location = 'Philipines'")
    bad_loc = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM crm_sales.accounts WHERE office_location = 'Philippines'")
    good_loc = cur.fetchone()[0]
    check("Location 'Philipines' typo corrected to 'Philippines'", bad_loc == 0 and good_loc == 1)
    
    # Product name standardization
    cur.execute("SELECT COUNT(*) FROM crm_sales.sales_pipeline WHERE product = 'GTXPro'")
    bad_prod = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM crm_sales.sales_pipeline WHERE product = 'GTX Pro'")
    good_prod = cur.fetchone()[0]
    check("Product 'GTXPro' standardized to 'GTX Pro'", bad_prod == 0 and good_prod == 1480)

    cur.close()
    conn.close()
    
    # ------------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------------
    print("\n" + "=" * 80)
    passed = sum(1 for _, s, _ in results if s == "PASS")
    failed = sum(1 for _, s, _ in results if s == "FAIL")
    print(f"TOTAL: {passed} PASSED, {failed} FAILED out of {len(results)} validation checks.")
    print("=" * 80)
    
    return failed == 0

def test_phase2_validation():
    assert run_phase2_validation() is True

if __name__ == "__main__":
    success = run_phase2_validation()
    sys.exit(0 if success else 1)
