from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer 
from sqlmodel.ext.asyncio.session import AsyncSession
from jose import jwt, JWTError
from datetime import datetime

from server.exceptions.auth import EmailNotVerifiedException, InvalidCredentialsException
from server.db import get_session
from server.db.user.schema import User 
from server.db.user.dao import UserDAO
from server.services.auth.models import TokenData
from server.utils import nowutc
from server.config import settings as s
from server import API_PREFIX 

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{API_PREFIX}/auth/login")

#NOTE: This function is used to get the current user from the JWT token. It takes the token as an argument and returns the user's data.

async def _get_current_user(token: str=Depends(oauth2_scheme), session: AsyncSession=Depends(get_session)):

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

async def get_current_active_user(user: User = Depends(_get_current_user)):
    if user.verified:
        return user
    else:
        raise EmailNotVerifiedException() 



