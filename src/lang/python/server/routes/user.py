from typing import List

from fastapi import APIRouter, Depends, status
from sqlmodel.ext.asyncio.session import AsyncSession

from server.db import get_session
from server.db.user.schema import User, UserRole   
from server.db.user.dao import UserDAO
from server.services.user.models import UserRequest, UserResponse
from server.services.auth.dependencies import get_current_active_user
from server.exceptions.user import UserRoleNotAllowedException

router = APIRouter()

async def require_admin(user: User = Depends(get_current_active_user)):
    if user.role != UserRole.ADMIN:
        raise UserRoleNotAllowedException()

@router.get("/", response_model=List[UserResponse])
async def get_users(_: User = Depends(require_admin), session: AsyncSession=Depends(get_session)):
    db = UserDAO(session)
    users = await db.get_users()
    return users

@router.get("/me", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_current_user(current_user: User = Depends(get_current_active_user)):
    return current_user

@router.get("/{userd_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_user(userd_id: str, current_user: User = Depends(get_current_active_user),session: AsyncSession=Depends(get_session)):
    #NOTE: Might abstract this into a decorator down the road.
    if current_user.id != userd_id and current_user.role != UserRole.ADMIN:
        raise UserRoleNotAllowedException()

    db = UserDAO(session)
    user = await db.get_user(userd_id)
    return user

@router.put("/{userd_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def update_user(userd_id: str, user_data: UserRequest,current_user: User = Depends(get_current_active_user), session: AsyncSession=Depends(get_session)):
    #NOTE: Might abstract this into a decorator down the road.
    if current_user.id != userd_id and current_user.role != UserRole.ADMIN:
        raise UserRoleNotAllowedException()

    db = UserDAO(session)
    updated_user = await db.update_user(userd_id, user_data)
    return updated_user

@router.delete("/{userd_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(userd_id: str, current_user:User = Depends(get_current_active_user), session: AsyncSession=Depends(get_session)):
     #NOTE: Might abstract this into a decorator down the road.
    if current_user.id != userd_id and current_user.role != UserRole.ADMIN:
        raise UserRoleNotAllowedException()

    db = UserDAO(session)
    await db.delete_user(userd_id)
