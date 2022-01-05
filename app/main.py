import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import register_api
from app.core.config import settings
from app.exceptions import register_exception_handlers

log = logging.getLogger('uvicorn')
app = FastAPI(
    title=settings.APP_NAME,
    description='A **FastAPI** project to aggregate personal projects',
    version='1.0.0',
    terms_of_service='terms.html',
    contact={'name': 'Diogo Alves', 'email': 'diogo.alves.ti@gmail.com'},
    license_info={
        'name': 'MIT License',
        'url': 'https://mit-license.org/',
    },
    openapi_tags=[
        {
            'name': 'Authentication',
            'description': 'Authentication process',
            'externalDocs': {
                'description': 'Example of using external docs',
                'url': 'https://swagger.io/specification/#external-documentation-object',  # noqa
            },
        },
        {
            'name': 'Users',
            'description': 'Manage users',
        },
        {
            'name': 'Projects',
            'description': 'Manage projects',
        },
    ],
)
if settings.CORS_ALLOWED_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            str(origin) for origin in settings.CORS_ALLOWED_ORIGINS
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.on_event('startup')
async def startup():
    log.info("Starting up...")
    register_api(app)
    register_exception_handlers(app)
