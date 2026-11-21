"""应用入口：装配路由、CORS、全局异常处理与开发环境演示数据播种。"""
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import text

from app.api.v1.router import api_router
from app.core.config import get_settings
from app.core.exceptions import AppError
from app.core.security import hash_password
from app.db.database import SessionLocal, engine
from app.models import (  # noqa: F401  确保 ORM 映射与关联表注册
    Conversation,
    Friendship,
    Message,
    Notification,
    Note,
    NoteComment,
    NoteLike,
    Tag,
    User,
    UserActivity,
    note_tags,
)
from app.repositories.note_repository import NoteRepository
from app.repositories.notification_repo import NotificationRepository
from app.repositories.user_repository import UserRepository

settings = get_settings()


def _ensure_activity_schema() -> None:
    """V3 新表 `user_activity` 的幂等自愈建表（checkfirst）。

    数据库结构变更的正式入口是 `sql/v3/sql_v3.sql`（含历史回填）；此处仅做**防御性兜底**：
    即使尚未执行迁移脚本，笔记增/改/删里的活跃度埋点也不会因「缺表」而拖累主业务。
    只创建「新增的那张表」，绝不改动任何既有表或数据，可安全重复执行。
    """
    try:
        UserActivity.__table__.create(bind=engine, checkfirst=True)
    except Exception as exc:  # noqa: BLE001 - 数据库暂未就绪时不阻断应用启动
        print(f"[startup] user_activity 自愈建表跳过：{exc}")


def _ensure_social_schema() -> None:
    """V5 社交功能新表的幂等自愈建表（checkfirst）。

    正式入口是 `sql/v5/sql_v5.sql`；此处仅做**防御性兜底**：即使尚未跑迁移，
    评论 / 点赞 / 笔友 / 聊天接口也不会因「缺表」拖累主业务。
    只创建新增表（按外键依赖顺序），不改动既有表或数据，可安全重复执行；
    单张表失败被隔离并跳过，不阻断其余表创建与应用启动。
    """
    for model in (NoteComment, NoteLike, Friendship, Conversation, Message, Notification):
        try:
            model.__table__.create(bind=engine, checkfirst=True)
        except Exception as exc:  # noqa: BLE001 - 数据库暂未就绪时不阻断应用启动
            print(f"[startup] {model.__tablename__} 自愈建表跳过：{exc}")


def _ensure_bio_column() -> None:
    """V4 `users.bio` 的幂等自愈加列（对应 sql/v4/sql_v4.sql）。

    正式的结构变更入口是迁移脚本；此处是防御性兜底：若开发库尚未执行 V4，
    启动即补上该列，避免 ORM 查询 users 时因「Unknown column 'users.bio'」
    导致登录 / 获取用户 / PATCH /auth/me 全线 500。只新增这一列，可安全重复执行。
    """
    try:
        with engine.begin() as conn:
            exists = conn.execute(
                text(
                    "SELECT COUNT(*) FROM information_schema.COLUMNS "
                    "WHERE TABLE_SCHEMA = DATABASE() "
                    "AND TABLE_NAME = 'users' AND COLUMN_NAME = 'bio'"
                )
            ).scalar_one()
            if not exists:
                conn.execute(
                    text(
                        "ALTER TABLE users "
                        "ADD COLUMN bio VARCHAR(500) NULL COMMENT '个人简介'"
                    )
                )
    except Exception as exc:  # noqa: BLE001 - 数据库暂未就绪时不阻断应用启动
        print(f"[startup] users.bio 自愈加列跳过：{exc}")


def _ensure_friendship_columns() -> None:
    """V6 `friendships` 好友设置列的幂等自愈加列（对应 sql/v6/sql_v6.sql）。

    checkfirst 只对「整张表不存在」有效；开发库里 friendships 表是 V5 建的旧结构，
    未跑 V6 迁移时 ORM 查询会因缺列 500。此处逐列判断并补齐，可安全重复执行。
    """
    columns = {
        "note": "VARCHAR(100) NULL COMMENT '好友备注'",
        "privacy": "VARCHAR(16) NOT NULL DEFAULT 'all' COMMENT '隐私设置'",
        "relation_type": "VARCHAR(32) NOT NULL DEFAULT 'friend' COMMENT '关系类别'",
        "closeness": "VARCHAR(16) NOT NULL DEFAULT 'friend' COMMENT '关系程度'",
    }
    try:
        with engine.begin() as conn:
            for name, ddl in columns.items():
                exists = conn.execute(
                    text(
                        "SELECT COUNT(*) FROM information_schema.COLUMNS "
                        "WHERE TABLE_SCHEMA = DATABASE() "
                        "AND TABLE_NAME = 'friendships' AND COLUMN_NAME = :name"
                    ),
                    {"name": name},
                ).scalar_one()
                if not exists:
                    conn.execute(text(f"ALTER TABLE friendships ADD COLUMN {name} {ddl}"))
    except Exception as exc:  # noqa: BLE001 - 数据库暂未就绪时不阻断应用启动
        print(f"[startup] friendships 设置列自愈加列跳过：{exc}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 先保证 V3 活跃度表、V4 users.bio 列、V5 社交新表、V6 好友设置列存在（幂等），再播种
    _ensure_activity_schema()
    _ensure_bio_column()
    _ensure_social_schema()
    _ensure_friendship_columns()
    # 开发环境：users 表为空时播种演示账号，便于直接登录体验
    if settings.seed_demo_user and settings.app_env != "production":
        _seed_demo_user()
    yield


def _seed_demo_user() -> None:
    """开发环境演示数据：演示账号 + 标签 + 笔记（幂等，可重复启动）。"""
    db = SessionLocal()
    try:
        repo = UserRepository(db)
        user = repo.get_by_username("demo")
        if user is None:
            user = repo.create(
                username="demo",
                display_name="演示用户",
                email="demo@hellonote.app",
                password_hash=hash_password("demo1234"),
            )

        note_repo = NoteRepository(db)
        if note_repo.count_by_user(user.id) == 0:
            tag_defs = [
                ("灵感", "#9A8052"),
                ("工作", "#77735D"),
                ("读书", "#754747"),
                ("旅行", "#5B7C7C"),
                ("待办", "#9A8052"),
            ]
            tags = [Tag(user_id=user.id, name=name, color=color) for name, color in tag_defs]
            db.add_all(tags)
            db.flush()

            notes_defs = [
                ("关于专注的随想", "专注不是一次性的决定，而是一种被反复找回的状态。\n\n当环境足够安静，思绪才有落点。", True, [0, 1]),
                ("本周阅读清单", "《安静》— 关于注意力；《卡片笔记写作法》— 关于知识沉淀。", True, [2]),
                ("京都旅行碎片", "清晨的伏见稻荷，红与绿之间，时间慢了下来。", False, [3]),
                ("产品评审纪要", "讨论了面板的信息密度，决定先保持克制，后续再做个性化。", False, [1]),
                ("待办：整理读书笔记", "把零散的标注汇总成一篇可检索的索引。", False, [4, 2]),
                ("一句喜欢的诗", "我们终将相遇，在没有喧嚣的地方。", False, [0]),
            ]
            for title, content, pinned, tag_idx in notes_defs:
                note = Note(user_id=user.id, title=title, content=content, is_pinned=pinned)
                db.add(note)
                db.flush()
                for i in tag_idx:
                    db.execute(
                        note_tags.insert().values(note_id=note.id, tag_id=tags[i].id)
                    )
            db.commit()

        # 系统通知种子：幂等，独立于笔记播种，每次启动都执行（避免旧库漏插）
        try:
            NotificationRepository(db).seed_system_notification(
                user.id, "欢迎使用 Hello!Note，开始记录你的想法"
            )
        except Exception as exc:  # noqa: BLE001 - 通知种子失败不阻断启动
            print(f"[startup] 系统通知种子跳过：{exc}")
    finally:
        db.close()


app = FastAPI(title=settings.app_name, version="0.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

# 静态资源：头像上传目录对外暴露为 /uploads（api_router 前缀为 /api/v1，不会冲突）。
# 先建目录再挂载，避免 StaticFiles 在目录不存在时启动报错。
upload_root = Path(settings.upload_dir)
upload_root.mkdir(parents=True, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=upload_root), name="uploads")


@app.exception_handler(AppError)
async def handle_app_error(request: Request, exc: AppError) -> JSONResponse:
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})



