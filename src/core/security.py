"""JWT primitives. Deliberately free of module imports — anything imported from
``src.modules.*`` here would trigger that package's ``__init__`` (which imports
its router, which needs ``CurrentUser`` from here) — a circular import."""

from datetime import UTC, datetime, timedelta

import jwt
from fastapi.security import OAuth2PasswordBearer

from src.core.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def create_access_token(subject: str) -> str:
    """Issue a signed JWT whose ``sub`` claim is the user id."""
    expire = datetime.now(UTC) + timedelta(minutes=settings.access_token_expire_minutes)
    payload = {"sub": subject, "exp": expire}
    return jwt.encode(payload, settings.secret_key, algorithm=settings.jwt_algorithm)


def decode_access_token(token: str) -> str | None:
    """Return the JWT's ``sub`` claim, or ``None`` when invalid or expired."""
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.jwt_algorithm])
    except jwt.PyJWTError:
        return None
    return payload.get("sub")
