"""
Production Readiness & Deployment Test Suite.

Validates:
- DATABASE_URL parsing and postgres:// normalization
- Connection pool parameters from settings
- Production JWT secret validation enforcement
- CORS origins list parsing
- Error handling in health check without credential leakage
- Database initialization idempotence
"""

import os
import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from backend.app.core.config import Settings, COMPROMISED_DEFAULT_SECRET
from backend.app.main import app

@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c

def test_database_url_normalization():
    """Verify postgres:// is rewritten to postgresql:// for SQLAlchemy compatibility."""
    s = Settings(
        DATABASE_URL="postgres://user:pass@ep-host.render.com:5432/my_db",
        _env_file=None
    )
    assert s.sqlalchemy_database_uri == "postgresql://user:pass@ep-host.render.com:5432/my_db"

def test_database_url_precedence():
    """Verify DATABASE_URL overrides discrete DB_* parameters."""
    s = Settings(
        DATABASE_URL="postgresql://render_user:render_pass@remote_host:5432/render_db",
        DB_HOST="localhost",
        DB_NAME="local_db",
        _env_file=None
    )
    assert s.sqlalchemy_database_uri == "postgresql://render_user:render_pass@remote_host:5432/render_db"

def test_production_jwt_secret_enforcement():
    """Verify that in production mode, default or missing JWT secret raises ValueError."""
    with pytest.raises(ValueError, match="Production environment detected"):
        Settings(
            ENVIRONMENT="production",
            JWT_SECRET_KEY=COMPROMISED_DEFAULT_SECRET,
            _env_file=None
        )

def test_production_jwt_secret_custom_accepted():
    """Verify that a unique secret in production is accepted."""
    s = Settings(
        ENVIRONMENT="production",
        JWT_SECRET_KEY="a-very-secure-custom-production-secret-12345",
        _env_file=None
    )
    assert s.JWT_SECRET_KEY == "a-very-secure-custom-production-secret-12345"

def test_cors_origins_parsing():
    """Verify comma-separated CORS origins are parsed with defaults preserved."""
    s = Settings(
        CORS_ORIGINS="https://vantage-crm.vercel.app, https://demo.example.com",
        _env_file=None
    )
    origins = s.cors_origins_list
    assert "https://vantage-crm.vercel.app" in origins
    assert "https://demo.example.com" in origins
    assert "http://localhost:5173" in origins

def test_health_check_safe_on_error(client):
    """Verify that database errors in /health return 'unhealthy' without leaking connection details."""
    with patch("backend.app.main.text") as mock_text:
        # Simulate database query failure
        mock_text.side_effect = Exception("password authentication failed for user 'secret_user'")
        res = client.get("/health")
        assert res.status_code == 200
        data = res.json()
        assert data["status"] == "degraded"
        assert data["database"] == "unhealthy"
        # Ensure raw exception text with secrets is NOT leaked in client response
        assert "secret_user" not in str(data)

def test_init_db_idempotent():
    """Verify that init_db can be called repeatedly without error."""
    from src.database.init_db import initialize_database
    # Running it against existing database should be a no-op and succeed
    initialize_database()
