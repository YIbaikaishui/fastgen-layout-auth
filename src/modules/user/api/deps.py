"""The current-user dependency lives in the user module: it needs the user
service, and importing that from ``core`` would be a cycle (the user package's
``__init__`` imports the router, which imports this file)."""

from typing import Annotated

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_session
from src.core.security import decode_access_token, oauth2_scheme
from src.modules.user.domain.model import User


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> User:
    """Resolve the authenticated user from the ``Authorization: Bearer`` header."""
    # Imported here (not at module level) for the cycle reason above — by request
    # time every module is fully loaded.
    from src.modules.user.application.user_service import UserNotFound, UserService
    from src.modules.user.infrastructure.user_repository import SqlUserRepository

    subject = decode_access_token(token)
    if subject is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    service = UserService.from_repository(SqlUserRepository(session))
    try:
        return await service.get(int(subject))
    except (UserNotFound, ValueError) as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc


CurrentUser = Annotated[User, Depends(get_current_user)]
