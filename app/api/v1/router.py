"""API v1 路由聚合。"""
from fastapi import APIRouter

from app.api.v1.endpoints import auth, dashboard, health, notes, tags

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(health.router)
api_router.include_router(auth.router)
api_router.include_router(notes.router)
api_router.include_router(tags.router)
api_router.include_router(dashboard.router)
