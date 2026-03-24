import base64
import hashlib
import hmac
import secrets
from datetime import datetime, timedelta, timezone

from jose import jwt

from app.core.config import get_settings

settings = get_settings()
PBKDF2_ROUNDS = 390000


def _pbkdf2_hash(password: str, salt: bytes) -> str:
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, PBKDF2_ROUNDS)
    return base64.b64encode(digest).decode("ascii")


def hash_password(password: str) -> str:
    if len(password) < 6:
        raise ValueError("Password must be at least 6 characters")
    salt = secrets.token_bytes(16)
    return f"pbkdf2_sha256${PBKDF2_ROUNDS}${base64.b64encode(salt).decode('ascii')}${_pbkdf2_hash(password, salt)}"


def verify_password(plain_password: str, stored_hash: str) -> bool:
    try:
        algorithm, rounds, salt_b64, expected = stored_hash.split("$", 3)
        if algorithm != "pbkdf2_sha256":
            return False
        salt = base64.b64decode(salt_b64)
        calculated = base64.b64encode(
            hashlib.pbkdf2_hmac("sha256", plain_password.encode("utf-8"), salt, int(rounds))
        ).decode("ascii")
        return hmac.compare_digest(calculated, expected)
    except Exception:
        return False


def create_access_token(subject: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    payload = {"sub": subject, "exp": expire}
    return jwt.encode(payload, settings.secret_key, algorithm="HS256")
