"""Password hashing — a user-domain concern, used by the user service.

Uses ``bcrypt`` directly (not passlib, which is in maintenance mode and breaks
with bcrypt >= 4.1). bcrypt only considers the first 72 bytes of a password;
the schema caps length, and we truncate defensively."""

import bcrypt

_MAX_PASSWORD_BYTES = 72


def hash_password(password: str) -> str:
    """Hash a plaintext password for storage."""
    secret = password.encode("utf-8")[:_MAX_PASSWORD_BYTES]
    return bcrypt.hashpw(secret, bcrypt.gensalt()).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Check a plaintext password against its hash."""
    secret = plain_password.encode("utf-8")[:_MAX_PASSWORD_BYTES]
    return bcrypt.checkpw(secret, hashed_password.encode("utf-8"))
