"""User HTTP router."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_session
from src.modules.user.api.deps import CurrentUser
from src.modules.user.application.schemas import UserCreate, UserRead, UserUpdate
from src.modules.user.application.user_service import EmailTaken, UserNotFound, UserService
from src.modules.user.domain.model import User
from src.modules.user.infrastructure.user_repository import SqlUserRepository

SessionDep = Annotated[AsyncSession, Depends(get_session)]

router = APIRouter(prefix="/users", tags=["users"])


def _service(session: AsyncSession) -> UserService:
    return UserService.from_repository(SqlUserRepository(session))


@router.post("", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register(data: UserCreate, session: SessionDep) -> User:
    """Register a new user (login lives in the auth module)."""
    try:
        return await _service(session).register(data)
    except EmailTaken:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")


@router.get("", response_model=list[UserRead])
async def list_users(session: SessionDep) -> list[User]:
    return await _service(session).list()


@router.get("/me", response_model=UserRead)
async def read_me(current_user: CurrentUser) -> User:
    """The authenticated user (protected example: requires a Bearer token)."""
    return current_user


@router.get("/{user_id}", response_model=UserRead)
async def get_user(user_id: int, session: SessionDep) -> User:
    try:
        return await _service(session).get(user_id)
    except UserNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


@router.patch("/{user_id}", response_model=UserRead)
async def update_user(user_id: int, data: UserUpdate, session: SessionDep) -> User:
    try:
        return await _service(session).update(user_id, data)
    except UserNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, session: SessionDep) -> None:
    try:
        await _service(session).delete(user_id)
    except UserNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
