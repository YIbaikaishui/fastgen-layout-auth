"""Auth application service: exchange credentials for a token."""

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.security import create_access_token
from src.modules.auth.application.schemas import Token
from src.modules.user.application.user_service import UserService
from src.modules.user.infrastructure.user_repository import SqlUserRepository


class AuthService:
    """Login use case. Free of HTTP concerns."""

    def __init__(self, session: AsyncSession) -> None:
        self._users = UserService.from_repository(SqlUserRepository(session))

    async def login(self, email: str, password: str) -> Token:
        """Authenticate credentials and issue a JWT. ``BadCredentials`` propagates
        to the router, which maps it to 401."""
        user = await self._users.authenticate(email, password)
        return Token(access_token=create_access_token(str(user.id)))
