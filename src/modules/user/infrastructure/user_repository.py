"""SQLAlchemy adapter for the User repository port."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.user.domain.model import User


class SqlUserRepository:
    """Implements :class:`src.modules.user.domain.repository.UserRepository`."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add(self, entity: User) -> User:
        self._session.add(entity)
        await self._session.commit()
        await self._session.refresh(entity)
        return entity

    async def get(self, entity_id: int) -> User | None:
        return await self._session.get(User, entity_id)

    async def get_by_email(self, email: str) -> User | None:
        result = await self._session.scalars(select(User).where(User.email == email))
        return result.first()

    async def list(self) -> list[User]:
        result = await self._session.scalars(select(User))
        return list(result)

    async def delete(self, entity: User) -> None:
        await self._session.delete(entity)
        await self._session.commit()
