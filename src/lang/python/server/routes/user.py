from typing import List

from fastapi import APIRouter, Depends, status

from server.services.user import get_user_service
from server.services.user.models import UserResponse, UserUpdate 
from server.services.user.service import UserService

router = APIRouter()

@router.get("/", response_model=List[UserResponse])
async def get_users(user_service: UserService = Depends(get_user_service)):
    return await user_service.get_users()
    
@router.get("/me", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_current_user(user_service: UserService = Depends(get_user_service)):
    return user_service.get_current_user()

@router.get("/{userd_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_user(userd_id: str, user_service: UserService = Depends(get_user_service)):
    return await user_service.get_user(userd_id)

@router.put("/{userd_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def update_user(userd_id: str, user_data: UserUpdate, user_service: UserService = Depends(get_user_service)):
    return await user_service.update_user(userd_id, user_data)

@router.delete("/{userd_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(userd_id: str, user_service: UserService = Depends(get_user_service)):
    await user_service.delete_user(userd_id)
    
