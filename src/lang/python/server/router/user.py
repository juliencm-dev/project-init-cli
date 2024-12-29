from typing import List

from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from db.user.schema import UserRequest, UserResponse   
from db.user.dao import UserDAO
from db.db import get_session
from http import HTTPStatus

from argon2 import PasswordHasher

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

@router.get("/", response_model=List[UserResponse])
async def get_users(session: AsyncSession=Depends(get_session)):
    db = UserDAO(session)
    users = await db.get_users()
    return users

@router.post("/", response_model=UserResponse, status_code=HTTPStatus.CREATED)
async def create_user(user_data: UserRequest, session: AsyncSession=Depends(get_session)):
    db = UserDAO(session)
    ph = PasswordHasher()

    #NOTE: I chose to use Argon2 for hashing passwords as it's one of the best solution. But you can change this to whatever you prefer, like bcrypt.
    user_data.password = ph.hash(user_data.password)

    new_user = await db.create_user(user_data)
    return new_user

@router.get("/{userd_id}", response_model=UserResponse, status_code=HTTPStatus.OK)
async def get_user(userd_id: str, session: AsyncSession=Depends(get_session)):
    db = UserDAO(session)
    user = await db.get_user(userd_id)
    return user

@router.put("/{userd_id}", response_model=UserResponse, status_code=HTTPStatus.OK)
async def update_user(userd_id: str, user_data: UserRequest, session: AsyncSession=Depends(get_session)):
    db = UserDAO(session)
    updated_user = await db.update_user(userd_id, user_data)
    return updated_user

@router.delete("/{userd_id}", status_code=HTTPStatus.NO_CONTENT)
async def delete_user(userd_id: str, session: AsyncSession=Depends(get_session)):
    db = UserDAO(session)
    await db.delete_user(userd_id)
