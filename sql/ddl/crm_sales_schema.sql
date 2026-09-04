-- ============================================================================
-- Schema: crm_sales
-- Module: Sales CRM Analytics
-- ============================================================================

CREATE SCHEMA IF NOT EXISTS crm_sales;

-- ----------------------------------------------------------------------------
-- Table: accounts
-- ----------------------------------------------------------------------------
DROP TABLE IF EXISTS crm_sales.sales_pipeline CASCADE;
DROP TABLE IF EXISTS crm_sales.accounts CASCADE;

CREATE TABLE crm_sales.accounts (
    account VARCHAR(100) PRIMARY KEY,
    sector VARCHAR(50) NOT NULL,
    year_established INTEGER NOT NULL CHECK (year_established BETWEEN 1800 AND 2100),
    revenue NUMERIC(12, 2) NOT NULL CHECK (revenue >= 0),
    employees INTEGER NOT NULL CHECK (employees >= 0),
    office_location VARCHAR(100) NOT NULL,
    subsidiary_of VARCHAR(100),
    CONSTRAINT fk_accounts_subsidiary FOREIGN KEY (subsidiary_of)
        REFERENCES crm_sales.accounts(account)
        ON UPDATE CASCADE
        ON DELETE SET NULL
);

CREATE INDEX idx_accounts_sector ON crm_sales.accounts(sector);
CREATE INDEX idx_accounts_location ON crm_sales.accounts(office_location);

-- ----------------------------------------------------------------------------
-- Table: products
-- ----------------------------------------------------------------------------
DROP TABLE IF EXISTS crm_sales.products CASCADE;

CREATE TABLE crm_sales.products (
    product VARCHAR(50) PRIMARY KEY,
    series VARCHAR(20) NOT NULL,
    sales_price NUMERIC(10, 2) NOT NULL CHECK (sales_price >= 0)
);

CREATE INDEX idx_products_series ON crm_sales.products(series);

-- ----------------------------------------------------------------------------
-- Table: sales_teams
-- ----------------------------------------------------------------------------
DROP TABLE IF EXISTS crm_sales.sales_teams CASCADE;

CREATE TABLE crm_sales.sales_teams (
    sales_agent VARCHAR(100) PRIMARY KEY,
    manager VARCHAR(100) NOT NULL,
    regional_office VARCHAR(50) NOT NULL
);

CREATE INDEX idx_sales_teams_manager ON crm_sales.sales_teams(manager);
CREATE INDEX idx_sales_teams_region ON crm_sales.sales_teams(regional_office);

-- ----------------------------------------------------------------------------
-- Table: sales_pipeline
-- ----------------------------------------------------------------------------
CREATE TABLE crm_sales.sales_pipeline (
    opportunity_id VARCHAR(50) PRIMARY KEY,
    sales_agent VARCHAR(100) NOT NULL,
    product VARCHAR(50) NOT NULL,
    account VARCHAR(100),  -- Nullable for early-stage opportunities
    deal_stage VARCHAR(20) NOT NULL CHECK (deal_stage IN ('Prospecting', 'Engaging', 'Won', 'Lost')),
    engage_date DATE,       -- Nullable for Prospecting
    close_date DATE,        -- Nullable for open deals
    close_value NUMERIC(12, 2), -- Nullable for open deals, 0 for Lost, >0 for Won
    CONSTRAINT fk_pipeline_agent FOREIGN KEY (sales_agent)
        REFERENCES crm_sales.sales_teams(sales_agent)
        ON UPDATE CASCADE,
    CONSTRAINT fk_pipeline_product FOREIGN KEY (product)
        REFERENCES crm_sales.products(product)
        ON UPDATE CASCADE,
    CONSTRAINT fk_pipeline_account FOREIGN KEY (account)
        REFERENCES crm_sales.accounts(account)
        ON UPDATE CASCADE
        ON DELETE SET NULL,
    -- Business Logic Date & Value Constraints
    CONSTRAINT chk_prospecting_no_engage CHECK (deal_stage != 'Prospecting' OR engage_date IS NULL),
    CONSTRAINT chk_open_no_close_date CHECK (deal_stage NOT IN ('Prospecting', 'Engaging') OR close_date IS NULL),
    CONSTRAINT chk_open_no_close_value CHECK (deal_stage NOT IN ('Prospecting', 'Engaging') OR close_value IS NULL),
    CONSTRAINT chk_lost_zero_value CHECK (deal_stage != 'Lost' OR close_value = 0),
    CONSTRAINT chk_won_positive_value CHECK (deal_stage != 'Won' OR (close_value IS NOT NULL AND close_value > 0)),
    CONSTRAINT chk_date_order CHECK (close_date IS NULL OR engage_date IS NULL OR close_date >= engage_date)
);

CREATE INDEX idx_pipeline_stage ON crm_sales.sales_pipeline(deal_stage);
CREATE INDEX idx_pipeline_agent ON crm_sales.sales_pipeline(sales_agent);
CREATE INDEX idx_pipeline_product ON crm_sales.sales_pipeline(product);
CREATE INDEX idx_pipeline_account ON crm_sales.sales_pipeline(account);
CREATE INDEX idx_pipeline_engage_dt ON crm_sales.sales_pipeline(engage_date);
CREATE INDEX idx_pipeline_close_dt ON crm_sales.sales_pipeline(close_date);
