from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

from server.exceptions.auth import InvalidCredentialsException
from server.exceptions.user import UserNotCreatedException
from server.services.user.models import UserRequest, UserResponse
from server.services.auth.models import AuthRequest, Token   
from server.services.auth.dependencies import authenticate_user, register_user, create_access_token
from server.config import settings as s

router = APIRouter()

@router.post("/login", status_code=status.HTTP_200_OK)
async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> Token:
    user = await authenticate_user(AuthRequest(email=form_data.username, password=form_data.password))

    if not user:
        raise InvalidCredentialsException()

    access_token_expires = timedelta(minutes=s.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.id, "role": user.role}, expires_delta=access_token_expires
    )

    return Token(access_token=access_token, token_type="bearer")

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user_data: UserRequest) -> UserResponse:
    user = await register_user(user_data)

    if not user:
       raise UserNotCreatedException()
    
    #TODO: Implement email verification and password reset logic
    
    return UserResponse(**user.model_dump())




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


