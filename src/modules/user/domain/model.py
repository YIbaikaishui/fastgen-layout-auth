from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from src.core.database import Base


class User(Base):
    """User entity. Passwords are stored only as hashes."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(320), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(1024))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
