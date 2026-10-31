"""安全工具：密码哈希（PBKDF2-HMAC-SHA256，无第三方原生依赖）与 JWT 签发/校验。"""
import hashlib
import hmac
import secrets
from datetime import datetime, timedelta, timezone
from typing import Any

from jose import jwt

from app.core.config import get_settings

settings = get_settings()

PBKDF2_ALGORITHM = "sha256"
PBKDF2_ITERATIONS = 100_000
_PBKDF2_PREFIX = f"pbkdf2_{PBKDF2_ALGORITHM}"


def hash_password(password: str) -> str:
    """生成形如 pbkdf2_sha256$<iterations>$<salt_hex>$<hash_hex> 的存储串。"""
    salt = secrets.token_bytes(16)
    dk = hashlib.pbkdf2_hmac(PBKDF2_ALGORITHM, password.encode("utf-8"), salt, PBKDF2_ITERATIONS)
    return f"{_PBKDF2_PREFIX}${PBKDF2_ITERATIONS}${salt.hex()}${dk.hex()}"


def verify_password(password: str, stored: str) -> bool:
    """常量时间比较，校验明文密码与存储串是否匹配。"""
    try:
        prefix, iter_s, salt_hex, hash_hex = stored.split("$")
        if prefix != _PBKDF2_PREFIX:
            return False
        iterations = int(iter_s)
        salt = bytes.fromhex(salt_hex)
        dk = hashlib.pbkdf2_hmac(PBKDF2_ALGORITHM, password.encode("utf-8"), salt, iterations)
        return hmac.compare_digest(dk.hex(), hash_hex)
    except (ValueError, AttributeError):
        return False


def create_access_token(subject: str | int, expires_minutes: int | None = None) -> str:
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=expires_minutes or settings.access_token_expire_minutes
    )
    payload = {
        "sub": str(subject),
        "iat": datetime.now(timezone.utc),
        "exp": expire,
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def decode_access_token(token: str) -> dict[str, Any] | None:
    try:
        return jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
    except jwt.JWTError:
        return None
