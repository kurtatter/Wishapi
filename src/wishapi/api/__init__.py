from fastapi import APIRouter

from .wishes import router as wishes_router
from .auth import router as authenticate_router
from .reports import router as reports_router

router = APIRouter()
router.include_router(authenticate_router)
router.include_router(wishes_router)
router.include_router(reports_router)
