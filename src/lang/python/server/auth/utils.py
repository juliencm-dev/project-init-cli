from sqlmodel.ext.asyncio.session import AsyncSession
from server.config import settings
from server.db.db import get_session
from server.db.user.schema import User, UserRequest
from server.utils import nowutc
from db.user.dao import UserDAO
from auth.schema import TokenData, AuthRequest

from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer 
from argon2 import PasswordHasher

oauth2_schema = OAuth2PasswordBearer(tokenUrl="/auth/login")

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
    encoded_jwt = jwt.encode(to_encode, settings.AUTH_SECRET, algorithm=settings.ALGORITHM)

    return encoded_jwt

#NOTE: This function is used to get the current user from the JWT token. It takes the token as an argument and returns the user's data.

async def get_current_user(token: str=Depends(oauth2_schema), session: AsyncSession=Depends(get_session)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.AUTH_SECRET, algorithms=[settings.ALGORITHM])
        user_id: str | None = payload.get("sub")
        exp: datetime | None = payload.get("exp")

        if exp is None:
            raise credentials_exception

        if  exp < nowutc():
            raise credentials_exception

        if user_id is None:
            raise credentials_exception

        token_data = TokenData(id=user_id, exp=exp)

    except JWTError:
        raise credentials_exception

    db = UserDAO(session)
    user = await db.get_user(token_data.id)
    
    if user is None:
        raise credentials_exception

    return user

async def get_current_active_user(user: User = Depends(get_current_user)):
    if user.verified:
        return user
    else:
        raise HTTPException(status_code=400, detail="Please verify your email address to activate your account.")

