"""根入口：复用 app.main 中的应用实例（便于 `uvicorn main:app` 启动）。"""
from app.main import app

__all__ = ["app"]
