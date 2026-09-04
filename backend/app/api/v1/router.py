from fastapi import APIRouter
from backend.app.api.v1.auth import router as auth_router
from backend.app.api.v1.accounts import router as accounts_router
from backend.app.api.v1.opportunities import router as opportunities_router
from backend.app.api.v1.pipeline import router as pipeline_router
from backend.app.api.v1.agents import router as agents_router
from backend.app.api.v1.managers import router as managers_router
from backend.app.api.v1.products import router as products_router
from backend.app.api.v1.prioritization import router as prioritization_router
from backend.app.api.v1.aging import router as aging_router
from backend.app.api.v1.work_queues import router as work_queues_router

api_router = APIRouter()

api_router.include_router(auth_router)
api_router.include_router(accounts_router)
api_router.include_router(opportunities_router)
api_router.include_router(pipeline_router)
api_router.include_router(agents_router)
api_router.include_router(managers_router)
api_router.include_router(products_router)
api_router.include_router(prioritization_router)
api_router.include_router(aging_router)
api_router.include_router(work_queues_router)
