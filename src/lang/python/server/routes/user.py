from typing import List

from fastapi import APIRouter, Depends, HTTPException, status status
from sqlmodel.ext.asyncio.session import AsyncSession
from db.user.schema import User, UserRequest, UserResponse, UserRole   
from db.user.dao import UserDAO
from db.db import get_session
from http import HTTPStatus

from server.auth.utils import get_current_active_user

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

async def require_admin(user: User = Depends(get_current_active_user)):
    if user.role != UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins are allowed to access this route.")

@router.get("/", response_model=List[UserResponse])
async def get_users(_: User = Depends(require_admin), session: AsyncSession=Depends(get_session)):
    db = UserDAO(session)
    users = await db.get_users()
    return users

@router.get("/{userd_id}", response_model=UserResponse, status_code=HTTPStatus.OK)
async def get_user(userd_id: str, current_user: User = Depends(get_current_active_user),session: AsyncSession=Depends(get_session)):
    #NOTE: Might abstract this into a decorator down the road.
    if current_user.id != userd_id and current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins are allowed to access this route.")

    db = UserDAO(session)
    user = await db.get_user(userd_id)
    return user

@router.put("/{userd_id}", response_model=UserResponse, status_code=HTTPStatus.OK)
async def update_user(userd_id: str, user_data: UserRequest,current_user: User = Depends(get_current_active_user), session: AsyncSession=Depends(get_session)):
    #NOTE: Might abstract this into a decorator down the road.
    if current_user.id != userd_id and current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins are allowed to access this route.")

    db = UserDAO(session)
    updated_user = await db.update_user(userd_id, user_data)
    return updated_user

@router.delete("/{userd_id}", status_code=HTTPStatus.NO_CONTENT)
async def delete_user(userd_id: str, current_user:User = Depends(get_current_active_user), session: AsyncSession=Depends(get_session)):
     #NOTE: Might abstract this into a decorator down the road.
    if current_user.id != userd_id and current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins are allowed to access this route.")

    db = UserDAO(session)
    await db.delete_user(userd_id)
