-- ============================================================================
-- Schema: crm_sales
-- Module: Application Authentication & Authorization
-- Note: App users are infrastructure accounts separate from CRM sales entities.
-- ============================================================================

CREATE TABLE IF NOT EXISTS crm_sales.app_users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('Admin', 'Sales Manager', 'Sales Agent')),
    is_active BOOLEAN DEFAULT TRUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_app_users_email ON crm_sales.app_users(email);
CREATE INDEX IF NOT EXISTS idx_app_users_role ON crm_sales.app_users(role);

-- Seed initial demonstration application users
INSERT INTO crm_sales.app_users (email, hashed_password, full_name, role)
VALUES
    ('admin@crm.local', '$2b$12$C.FAhA8gjKX8HFyOD1FD/.0Y0o1Xx9Z6/ea4O97mHNTHLYdQrCAfm', 'System Administrator', 'Admin'),
    ('manager@crm.local', '$2b$12$GPevExrGxE77/L7xId1t.ukpNh1IHF926SY0ZOYlWj9wM1hp3z.BG', 'Sales Operations Manager', 'Sales Manager'),
    ('agent@crm.local', '$2b$12$iwMQpFiJLYdmjKCZzAwAs.qIMdG5Q2JNoLq.i53ieeNZ.dONGUIFC', 'Sales Representative', 'Sales Agent')
ON CONFLICT (email) DO NOTHING;
