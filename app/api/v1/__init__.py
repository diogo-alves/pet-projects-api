from fastapi import APIRouter

from app.core.config import settings

from . import projects, users

router = APIRouter(prefix=settings.API_V1_PREFIX)
router.include_router(users.router)
router.include_router(projects.router)
