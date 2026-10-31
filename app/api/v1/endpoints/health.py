"""健康检查路由。"""
from fastapi import APIRouter

from app.core.config import get_settings

settings = get_settings()
router = APIRouter(tags=["system"])


@router.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok", "service": settings.app_name, "version": "0.1.0"}
