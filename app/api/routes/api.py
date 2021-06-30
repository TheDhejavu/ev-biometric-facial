from fastapi import APIRouter, Request, Depends
from app.api.routes import (
    auth_routes,
)

router = APIRouter()
router.include_router(auth_routes.router, tags=["auth"], prefix="/auth")
