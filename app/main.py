# # API application creation and configuration.

from fastapi import FastAPI, Request, Depends
from fastapi.openapi.utils import get_openapi
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware

from app.api.routes.api import router as api_router
from app.common.config import LOGO, ALLOWED_HOSTS, API_PREFIX, DESCRIPTION, DEBUG, PROJECT_NAME, VERSION


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=PROJECT_NAME,
        version=VERSION,
        description=DESCRIPTION,
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": LOGO
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


def get_application() -> FastAPI:
    application = FastAPI(title=PROJECT_NAME, debug=DEBUG, version=VERSION)

    application.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_HOSTS or ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.include_router(api_router, prefix=API_PREFIX)
    application.openapi = custom_openapi

    return application


app = get_application()


@app.get('/')
async def root():
    return {
        'message': 'Welcome to Facial Recognition Machine Learning Service.'
    }
