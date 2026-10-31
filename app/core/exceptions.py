"""统一应用异常：业务层抛出 AppError，由 main.py 的全局处理器转为 JSON 响应。"""
from fastapi import status


class AppError(Exception):
    status_code: int = status.HTTP_400_BAD_REQUEST
    detail: str = "请求错误"

    def __init__(self, detail: str | None = None) -> None:
        if detail:
            self.detail = detail
        super().__init__(self.detail)


class ConflictError(AppError):
    status_code = status.HTTP_409_CONFLICT
    detail = "资源冲突"


class NotFoundError(AppError):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "未找到资源"


class UnauthorizedError(AppError):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "未授权"


class ForbiddenError(AppError):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "禁止访问"
