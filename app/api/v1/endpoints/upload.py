"""头像上传路由（需登录）。文件落到本地 upload_dir/avatars，返回可访问的 URL。"""
from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.config import get_settings
from app.core.exceptions import AppError
from app.db.database import get_db
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import AvatarOut

router = APIRouter(prefix="/upload", tags=["upload"], dependencies=[Depends(get_current_user)])

settings = get_settings()

# 内容类型白名单：图片 MIME -> 落盘扩展名（扩展名由白名单决定，绝不信任原始文件名）
_ALLOWED_IMAGE_TYPES: dict[str, str] = {
    "image/png": ".png",
    "image/jpeg": ".jpg",
    "image/webp": ".webp",
    "image/gif": ".gif",
}


@router.post("/avatar", response_model=AvatarOut)
def upload_avatar(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> AvatarOut:
    """校验图片类型/大小后保存，并把头像地址写回当前用户资料。"""
    content_type = (file.content_type or "").split(";")[0].strip().lower()
    ext = _ALLOWED_IMAGE_TYPES.get(content_type)
    if ext is None:
        raise AppError("头像仅支持 PNG / JPEG / WebP / GIF 格式")

    # 多读 1 字节即可判断是否超限，避免大文件整体载入内存
    content = file.file.read(settings.avatar_max_bytes + 1)
    if len(content) > settings.avatar_max_bytes:
        raise AppError("头像文件大小不能超过 2MB")
    if not content:
        raise AppError("头像文件不能为空")

    avatar_dir = Path(settings.upload_dir) / "avatars"
    avatar_dir.mkdir(parents=True, exist_ok=True)

    filename = f"{uuid4().hex}{ext}"
    (avatar_dir / filename).write_bytes(content)

    url = f"/uploads/avatars/{filename}"
    UserRepository(db).update(user, avatar_url=url)
    return AvatarOut(url=url)
