from fastapi import APIRouter, Depends,status
from fastapi.security import OAuth2PasswordRequestForm

from server.services.auth import get_auth_service
from server.services.auth.service import AuthService
from server.services.user.models import UserRegistration, UserResponse
from server.services.auth.models import AccessTokenData 

router = APIRouter()

@router.post("/login", response_model=AccessTokenData, status_code=status.HTTP_200_OK)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), auth_service: AuthService = Depends(get_auth_service)):
    return await auth_service.login(form_data)

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserRegistration, auth_service: AuthService = Depends(get_auth_service)):
    return await auth_service.register(user_data)

#TODO: Implement email verification and password reset logic

# @router.post("/verify")
# async def verify():
#     return {"message": "Successfully verified email"}

# @router.post("/reset-password")
# async def reset_password():
#     return {"message": "Successfully reset password"}


#TODO: Implement refresh token and session tracking logic

# @router.post("/refresh")
# async def refresh():
#     return {"message": "Successfully refreshed token"}

# @router.post("/logout")
# async def logout():
#     return {"message": "Successfully logged out"}


