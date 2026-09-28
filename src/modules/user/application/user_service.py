"""User application service (use cases)."""

from src.modules.user.application.passwords import hash_password, verify_password
from src.modules.user.application.schemas import UserCreate, UserUpdate
from src.modules.user.domain.model import User
from src.modules.user.domain.repository import UserRepository


class UserError(Exception):
    """Base exception for the user domain. Raise subclasses from the service."""


class UserNotFound(UserError):
    """Raised when the requested user does not exist."""


class EmailTaken(UserError):
    """Raised when registering with an email that already exists."""


class BadCredentials(UserError):
    """Raised when login credentials do not match."""


class UserService:
    """Application service for user use cases. Free of HTTP concerns."""

    def __init__(self, repository: UserRepository) -> None:
        self._entities = repository

    @classmethod
    def from_repository(cls, repository: UserRepository) -> "UserService":
        return cls(repository)

    async def register(self, data: UserCreate) -> User:
        if await self._entities.get_by_email(data.email) is not None:
            raise EmailTaken()
        user = User(email=data.email, hashed_password=hash_password(data.password))
        return await self._entities.add(user)

    async def authenticate(self, email: str, password: str) -> User:
        """Verify credentials, raising ``BadCredentials`` on any mismatch."""
        user = await self._entities.get_by_email(email)
        if user is None or not verify_password(password, user.hashed_password):
            raise BadCredentials()
        return user

    async def create(self, data: UserCreate) -> User:
        return await self.register(data)

    async def list(self) -> list[User]:
        return await self._entities.list()

    async def get(self, item_id: int) -> User:
        entity = await self._entities.get(item_id)
        if entity is None:
            raise UserNotFound()
        return entity

    async def update(self, item_id: int, data: UserUpdate) -> User:
        entity = await self.get(item_id)
        for field, value in data.model_dump(exclude_unset=True).items():
            if field == "password":
                entity.hashed_password = hash_password(value)
            else:
                setattr(entity, field, value)
        return await self._entities.add(entity)

    async def delete(self, item_id: int) -> None:
        entity = await self.get(item_id)
        await self._entities.delete(entity)
