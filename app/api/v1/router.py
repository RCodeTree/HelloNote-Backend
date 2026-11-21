"""API v1 路由聚合。"""
from fastapi import APIRouter

from app.api.v1.endpoints import (
    activity,
    auth,
    chats,
    comments,
    dashboard,
    friends,
    health,
    notifications,
    notes,
    tags,
    upload,
)

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(health.router)
api_router.include_router(auth.router)
api_router.include_router(notes.router)
api_router.include_router(tags.router)
api_router.include_router(dashboard.router)
api_router.include_router(activity.router)
api_router.include_router(upload.router)
api_router.include_router(comments.router)
api_router.include_router(friends.router)
api_router.include_router(chats.router)
api_router.include_router(notifications.router)
