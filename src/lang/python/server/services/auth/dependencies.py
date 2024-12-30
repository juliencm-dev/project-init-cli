from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer 
from sqlmodel.ext.asyncio.session import AsyncSession
from argon2 import PasswordHasher
from jose import jwt, JWTError
from datetime import datetime, timedelta

from server.exceptions.auth import EmailNotVerifiedException, InvalidCredentialsException
from server.db import get_session
from server.db.user.schema import User 
from server.db.auth.schema import ValidationToken, ValidationTokenType
from server.db.user.dao import UserDAO
from server.services.auth.models import TokenData, AuthRequest
from server.services.user.models import UserRequest
from server.utils import nowutc, cuid
from server.config import settings as s

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

#NOTE: This function is used to authenticate the user. It takes the user's email and password and checks if the user exists in the database.
#NOTE: We use a AuthRequest pydantic model to validate the data.

async def authenticate_user(user_data: AuthRequest, session: AsyncSession=Depends(get_session)):
    db = UserDAO(session)
    ph = PasswordHasher()

    user = await db.get_user_by_email(user_data.email)

    if not user:
        return None
    if not ph.verify(user.password, user_data.password):
        return None 

    return user

#NOTE: This function is used to register a new user. It takes the user's data and creates a new user in the database.
#NOTE: We use a UserRequest pydantic model to validate the data.

async def register_user(user_data: UserRequest , session: AsyncSession=Depends(get_session)):
    db = UserDAO(session)
    ph = PasswordHasher()

    user = await db.get_user_by_email(user_data.email)

    if user:
        return None

    user_data.password = ph.hash(user_data.password)
    new_user = await db.create_user(user_data)

    return new_user

#NOTE: This function is used to create a JWT token for the user. It takes the user's id and the expiration time as arguments.

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()

    if expires_delta:
        expire = nowutc() + expires_delta
    else:
        expire = nowutc() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, s.AUTH_SECRET, algorithm=s.ALGORITHM)

    return encoded_jwt

#NOTE: This function is used to get the current user from the JWT token. It takes the token as an argument and returns the user's data.

async def get_current_user(token: str=Depends(oauth2_scheme), session: AsyncSession=Depends(get_session)):

    try:
        payload = jwt.decode(token, s.AUTH_SECRET, algorithms=[s.ALGORITHM])
        user_id: str | None = payload.get("sub")
        exp: datetime | None = payload.get("exp")

        if exp is None:
            raise InvalidCredentialsException() 

        if  exp < nowutc():
            raise InvalidCredentialsException()

        if user_id is None:
            raise InvalidCredentialsException()

        token_data = TokenData(id=user_id, exp=exp)

    except JWTError:
        raise InvalidCredentialsException()

    db = UserDAO(session)
    user = await db.get_user(token_data.id)
    
    if user is None:
        raise InvalidCredentialsException()

    return user

#NOTE: Simple function that check is the user is verified.

async def get_current_active_user(user: User = Depends(get_current_user)):
    if user.verified:
        return user
    else:
        raise EmailNotVerifiedException() 

def set_token_expiration(exp: int):
    return datetime.now() + timedelta(minutes=exp)

def generate_validation_token(user_id: str, token_type: ValidationTokenType):
    exp = s.VERIFICATION_TOKEN_EXPIRE_MINUTES if token_type == ValidationTokenType.VERIFICATION else s.PASSWORD_RESET_TOKEN_EXPIRE_MINUTES
    return ValidationToken(user_id=user_id, token=cuid(), expires_at=set_token_expiration(exp), token_type=token_type)

