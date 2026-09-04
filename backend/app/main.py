from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text
from backend.app.core.config import settings
from backend.app.core.database import get_db
from backend.app.core.exceptions import (
    AppException, app_exception_handler, unhandled_exception_handler
)
from backend.app.api.v1.router import api_router

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
)

# CORS middleware configured for frontend readiness
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom exception handlers (no stack traces in production JSON)
app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)

# Include API v1 routes
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/", tags=["System"])
def root():
    return {
        "project": settings.PROJECT_NAME,
        "status": "online",
        "version": "1.0.0",
        "documentation": "/docs",
        "api_v1_base": settings.API_V1_STR,
    }

@app.get("/health", tags=["System"])
def health_check(db: Session = Depends(get_db)):
    """Health check validating backend responsiveness and database connectivity."""
    try:
        db.execute(text("SELECT 1;"))
        db_status = "healthy"
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"

    return {
        "status": "healthy" if db_status == "healthy" else "degraded",
        "database": db_status,
        "timestamp_reference": settings.SNAPSHOT_REFERENCE_DATE,
    }
