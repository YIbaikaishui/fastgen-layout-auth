"""User repository port interface."""

from typing import Protocol

from src.modules.user.domain.model import User


class UserRepository(Protocol):
    """Persistence contract for ``User`` entities."""

    async def add(self, entity: User) -> User: ...

    async def get(self, entity_id: int) -> User | None: ...

    async def get_by_email(self, email: str) -> User | None: ...

    async def list(self) -> list[User]: ...

    async def delete(self, entity: User) -> None: ...
