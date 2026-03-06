import os
import datetime
from jose import jwt, JWTError
from src.utils.logging_config import get_logger

logger = get_logger("jwt_auth")

SECRET = os.getenv("JWT_SECRET", "change-me-please")
ALGO = os.getenv("JWT_ALGO", "HS256")
EXP_MIN = int(os.getenv("JWT_EXP_MIN", "60"))


def create_token(subject: str, roles: list = None) -> str:
    now = datetime.datetime.utcnow()
    payload = {
        "sub": subject,
        "roles": roles or [],
        "iat": now,
        "exp": now + datetime.timedelta(minutes=EXP_MIN),
    }
    token = jwt.encode(payload, SECRET, algorithm=ALGO)
    return token


def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, SECRET, algorithms=[ALGO])
    except JWTError as e:
        logger.exception("Invalid JWT: %s", e)
        raise
