import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text

from backend.app.core.config import settings
from backend.app.core.database import get_db
from backend.app.core.exceptions import (
    AppException, app_exception_handler, unhandled_exception_handler
)
from backend.app.api.v1.router import api_router

# Configure root application logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO),
    format="%(asctime)s [%(levelname)s] [%(name)s] %(message)s",
)
logger = logging.getLogger("backend.app.main")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan managing startup validation and shutdown."""
    logger.info(f"Starting {settings.PROJECT_NAME} in '{settings.ENVIRONMENT}' mode...")
    # Safe, non-blocking schema and data check
    try:
        from src.database.init_db import initialize_database
        initialize_database()
        logger.info("Database schema and data readiness confirmed.")
    except Exception as exc:
        logger.warning(
            f"Database initialization deferred or failed during startup: {exc}. "
            "Application will continue serving non-database endpoints."
        )
    yield
    logger.info("Shutting down application...")

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=(
        "Production-style, portfolio-grade B2B Sales CRM & Pipeline Management Platform REST API. "
        "Provides comprehensive endpoints for managing accounts, opportunities, sales pipeline, "
        "sales organization (agents, managers, regional offices), products, deterministic opportunity "
        "prioritization, opportunity aging, and operational work queues."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan,
)

# Production-safe CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_origin_regex=r"https:\/\/.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom exception handlers
app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)

# Include API v1 routes
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/", tags=["System"])
def root():
    return {
        "project": settings.PROJECT_NAME,
        "status": "online",
        "environment": settings.ENVIRONMENT,
        "version": "1.0.0",
        "documentation": "/docs",
        "api_v1_base": settings.API_V1_STR,
    }

@app.get("/health", tags=["System"])
def health_check(db: Session = Depends(get_db)):
    """
    Health check validating backend responsiveness and database connectivity.
    Does not expose internal hostnames, IPs, or credentials.
    """
    try:
        db.execute(text("SELECT 1;"))
        db_status = "healthy"
        overall_status = "healthy"
    except Exception as exc:
        logger.error(f"Database connectivity check failed: {exc}")
        db_status = "unhealthy"
        overall_status = "degraded"

    return {
        "status": overall_status,
        "database": db_status,
        "environment": settings.ENVIRONMENT,
        "timestamp_reference": settings.SNAPSHOT_REFERENCE_DATE,
    }
