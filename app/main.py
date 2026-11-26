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
    FriendSetting,
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


def _ensure_note_public_column() -> None:
    """V10 `notes.is_public` 的幂等自愈加列（对应 sql/v10/sql_v10.sql）。"""
    try:
        with engine.begin() as conn:
            exists = conn.execute(
                text(
                    "SELECT COUNT(*) FROM information_schema.COLUMNS "
                    "WHERE TABLE_SCHEMA = DATABASE() "
                    "AND TABLE_NAME = 'notes' AND COLUMN_NAME = 'is_public'"
                )
            ).scalar_one()
            if not exists:
                conn.execute(
                    text(
                        "ALTER TABLE notes "
                        "ADD COLUMN is_public BOOLEAN NOT NULL DEFAULT FALSE COMMENT '是否公开笔记'"
                    )
                )
    except Exception as exc:  # noqa: BLE001 - 数据库暂未就绪时不阻断应用启动
        print(f"[startup] notes.is_public 自愈加列跳过：{exc}")


def _ensure_friendship_columns() -> None:
    """V6 好友设置列与 V9 申请留言列的幂等自愈加列（对应 sql/v6/sql_v6.sql）。

    checkfirst 只对「整张表不存在」有效；开发库里 friendships 表是 V5 建的旧结构，
    未跑 V6 迁移时 ORM 查询会因缺列 500。此处逐列判断并补齐，可安全重复执行。
    """
    columns = {
        "note": "VARCHAR(100) NULL COMMENT '好友备注'",
        "privacy": "VARCHAR(16) NOT NULL DEFAULT 'all' COMMENT '隐私设置'",
        "relation_type": "VARCHAR(32) NOT NULL DEFAULT 'friend' COMMENT '关系类别'",
        "closeness": "VARCHAR(16) NOT NULL DEFAULT 'friend' COMMENT '关系程度'",
        "is_pinned": "BOOLEAN NOT NULL DEFAULT FALSE COMMENT '是否置顶'",
        "request_message": "VARCHAR(200) NULL COMMENT '好友申请留言'",
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


def _ensure_friend_settings_table() -> None:
    """friend_settings 个人设置表的幂等自愈建表 + 存量数据迁移。

    备注 / 隐私 / 关系类别 / 亲密程度 / 置顶属于「用户个人行为」，从共享的
    friendships 设置列迁移到每用户一行的 friend_settings：建表后按每条笔友关系
    为 requester / addressee 各补一行（已存在则跳过，重复执行无副作用），
    初次迁移沿用 friendships 旧列的值与时间，保证用户看到的设置视觉不变。
    表结构与 sql/v8/sql_v8.sql 对齐（含 created_at / updated_at、uk_fs_pair），
    对早期已建的无时间戳表会自动补列并重命名唯一键。
    """
    try:
        with engine.begin() as conn:
            conn.execute(
                text(
                    "CREATE TABLE IF NOT EXISTS friend_settings ("
                    "id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY "
                    "COMMENT '设置记录 ID（自增主键）', "
                    "friendship_id BIGINT UNSIGNED NOT NULL COMMENT '笔友关系 id', "
                    "user_id BIGINT UNSIGNED NOT NULL COMMENT '设置所属用户 id', "
                    "note VARCHAR(100) NULL COMMENT '该用户对此笔友的备注', "
                    "privacy VARCHAR(16) NOT NULL DEFAULT 'all' COMMENT '隐私设置', "
                    "relation_type VARCHAR(32) NOT NULL DEFAULT 'friend' COMMENT '关系类别', "
                    "closeness VARCHAR(16) NOT NULL DEFAULT 'friend' COMMENT '关系程度', "
                    "is_pinned BOOLEAN NOT NULL DEFAULT FALSE COMMENT '该用户是否置顶此笔友', "
                    "created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间', "
                    "updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP "
                    "ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间', "
                    "UNIQUE KEY uk_fs_pair (friendship_id, user_id), "
                    "KEY idx_fs_user (user_id), "
                    "CONSTRAINT fk_fs_friendship FOREIGN KEY (friendship_id) "
                    "REFERENCES friendships(id) ON DELETE CASCADE, "
                    "CONSTRAINT fk_fs_user FOREIGN KEY (user_id) "
                    "REFERENCES users(id) ON DELETE CASCADE"
                    ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci "
                    "COMMENT='笔友个人设置表（每个用户对每条笔友关系各一份）'"
                )
            )
            # 开发库可能已存在早期无时间戳 / 旧唯一键名的 friend_settings，逐项补齐
            for name, ddl in {
                "created_at": "DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间'",
                "updated_at": (
                    "DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP "
                    "ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'"
                ),
            }.items():
                exists = conn.execute(
                    text(
                        "SELECT COUNT(*) FROM information_schema.COLUMNS "
                        "WHERE TABLE_SCHEMA = DATABASE() "
                        "AND TABLE_NAME = 'friend_settings' AND COLUMN_NAME = :name"
                    ),
                    {"name": name},
                ).scalar_one()
                if not exists:
                    conn.execute(
                        text(f"ALTER TABLE friend_settings ADD COLUMN {name} {ddl}")
                    )
            new_index = conn.execute(
                text(
                    "SELECT COUNT(*) FROM information_schema.STATISTICS "
                    "WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'friend_settings' "
                    "AND INDEX_NAME = 'uk_fs_pair'"
                )
            ).scalar_one()
            old_index = conn.execute(
                text(
                    "SELECT COUNT(*) FROM information_schema.STATISTICS "
                    "WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'friend_settings' "
                    "AND INDEX_NAME = 'uk_friend_settings_pair'"
                )
            ).scalar_one()
            if not new_index and old_index:
                conn.execute(
                    text(
                        "ALTER TABLE friend_settings "
                        "DROP INDEX uk_friend_settings_pair, "
                        "ADD UNIQUE KEY uk_fs_pair (friendship_id, user_id)"
                    )
                )
            for old_fk, new_fk, column, ref_table in (
                ("fk_fs_friendships", "fk_fs_friendship", "friendship_id", "friendships"),
                ("fk_fs_users", "fk_fs_user", "user_id", "users"),
            ):
                counts = {}
                for name in (old_fk, new_fk):
                    counts[name] = conn.execute(
                        text(
                            "SELECT COUNT(*) FROM information_schema.TABLE_CONSTRAINTS "
                            "WHERE TABLE_SCHEMA = DATABASE() "
                            "AND TABLE_NAME = 'friend_settings' "
                            "AND CONSTRAINT_TYPE = 'FOREIGN KEY' AND CONSTRAINT_NAME = :name"
                        ),
                        {"name": name},
                    ).scalar_one()
                if not counts[new_fk] and counts[old_fk]:
                    conn.execute(
                        text(
                            f"ALTER TABLE friend_settings DROP FOREIGN KEY {old_fk}, "
                            f"ADD CONSTRAINT {new_fk} FOREIGN KEY ({column}) "
                            f"REFERENCES {ref_table}(id) ON DELETE CASCADE"
                        )
                    )
            friendships = conn.execute(
                text(
                    "SELECT id, requester_id, addressee_id, note, privacy, "
                    "relation_type, closeness, is_pinned, created_at, updated_at "
                    "FROM friendships"
                )
            ).mappings().all()
            for row in friendships:
                for user_id in (row["requester_id"], row["addressee_id"]):
                    exists = conn.execute(
                        text(
                            "SELECT COUNT(*) FROM friend_settings "
                            "WHERE friendship_id = :fid AND user_id = :uid"
                        ),
                        {"fid": row["id"], "uid": user_id},
                    ).scalar_one()
                    if exists:
                        continue
                    conn.execute(
                        text(
                            "INSERT INTO friend_settings "
                            "(friendship_id, user_id, note, privacy, relation_type, "
                            "closeness, is_pinned, created_at, updated_at) "
                            "VALUES (:fid, :uid, :note, :privacy, :relation_type, "
                            ":closeness, :is_pinned, :created_at, :updated_at)"
                        ),
                        {
                            "fid": row["id"],
                            "uid": user_id,
                            "note": row["note"],
                            "privacy": row["privacy"] or "all",
                            "relation_type": row["relation_type"] or "friend",
                            "closeness": row["closeness"] or "friend",
                            "is_pinned": row["is_pinned"],
                            "created_at": row["created_at"],
                            "updated_at": row["updated_at"],
                        },
                    )
    except Exception as exc:  # noqa: BLE001 - 数据库暂未就绪时不阻断应用启动
        print(f"[startup] friend_settings 自愈建表 / 数据迁移跳过：{exc}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 先保证 V3 活跃度表、V4 users.bio 列、V5 社交新表、V6/V7 好友设置列、friend_settings 个人设置表及其迁移数据存在（幂等），再播种
    _ensure_activity_schema()
    _ensure_bio_column()
    _ensure_social_schema()
    _ensure_note_public_column()
    _ensure_friendship_columns()
    _ensure_friend_settings_table()
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








