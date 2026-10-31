"""应用入口：装配路由、CORS、全局异常处理与开发环境演示数据播种。"""
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.v1.router import api_router
from app.core.config import get_settings
from app.core.exceptions import AppError
from app.core.security import hash_password
from app.db.database import SessionLocal
from app.models import Note, Tag, User, note_tags  # noqa: F401  确保 ORM 映射与关联表注册
from app.repositories.note_repository import NoteRepository
from app.repositories.user_repository import UserRepository

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
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
        if note_repo.count_by_user(user.id) > 0:
            return  # 已播种过，跳过

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


@app.exception_handler(AppError)
async def handle_app_error(request: Request, exc: AppError) -> JSONResponse:
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})
