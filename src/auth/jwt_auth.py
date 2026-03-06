import os
from datetime import datetime, timedelta
from jose import jwt, JWTError
from src.utils.logging_config import get_logger

logger = get_logger(__name__)

_SECRET = os.environ.get('JWT_SECRET', 'change-me-in-production')
_ALGO = 'HS256'


def create_access_token(subject: str, expires_minutes: int = 60) -> str:
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    to_encode = {"sub": subject, "exp": expire}
    return jwt.encode(to_encode, _SECRET, algorithm=_ALGO)


def verify_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, _SECRET, algorithms=[_ALGO])
        return payload
    except JWTError as e:
        logger.exception('JWT verification failed')
        raise
