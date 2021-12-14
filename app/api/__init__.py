import logging

from fastapi import APIRouter, FastAPI

from app.core.config import settings

from . import auth, v1

log = logging.getLogger('uvicorn')
router = APIRouter(prefix=settings.API_PREFIX)
router.include_router(auth.router)
router.include_router(v1.router)


def register_api(app: FastAPI) -> None:
    app.include_router(router)
    log.info('API registred.')
