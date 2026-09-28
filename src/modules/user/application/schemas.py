from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    """Shared user fields."""

    email: EmailStr


class UserCreate(UserBase):
    """Registration payload."""

    password: str = Field(min_length=8, max_length=128)


class UserUpdate(BaseModel):
    """Payload for updating a user — every field optional."""

    email: EmailStr | None = None
    password: str | None = Field(default=None, min_length=8, max_length=128)
    is_active: bool | None = None


class UserRead(UserBase):
    """Response schema. Never exposes the password hash."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    is_active: bool
