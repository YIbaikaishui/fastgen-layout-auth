"""Auth HTTP router: login + a protected identity endpoint."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_session
from src.modules.auth.application.auth_service import AuthService
from src.modules.auth.application.schemas import LoginRequest, Token
from src.modules.user.api.deps import CurrentUser
from src.modules.user.application.schemas import UserRead
from src.modules.user.application.user_service import BadCredentials

SessionDep = Annotated[AsyncSession, Depends(get_session)]

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=Token)
async def login(data: LoginRequest, session: SessionDep) -> Token:
    """Exchange email + password for a JWT access token."""
    try:
        return await AuthService(session).login(data.email, data.password)
    except BadCredentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.get("/me", response_model=UserRead)
async def read_me(current_user: CurrentUser) -> UserRead:
    """Protected example: requires ``Authorization: Bearer <token>``."""
    return current_user
