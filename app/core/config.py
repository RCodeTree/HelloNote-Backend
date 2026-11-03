"""应用配置（基于 pydantic-settings 从环境变量 / .env 读取）。"""
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    app_name: str = "Hello!Note API"
    app_env: str = "development"
    # 开发环境启动时若 users 表为空，自动播种演示账号
    seed_demo_user: bool = True

    database_url: str = (
        "mysql+pymysql://root:123456@127.0.0.1:3306/hello_note?charset=utf8mb4"
    )

    jwt_secret: str = "dev-only-change-me-in-production"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 1440

    cors_origins: str = "http://127.0.0.1:5173,http://localhost:5173"

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
