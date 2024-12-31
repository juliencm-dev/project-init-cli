from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import Depends

from .service import AuthService
from server.db import get_session
from server.db.user.dao import UserDAO
from server.utils.security.password import PasswordManager
from server.utils.security.tokens import TokenManager
from server.utils.security import get_password_manager, get_token_manager

def get_auth_service(session: AsyncSession = Depends(get_session), 
                     pwd_manager: PasswordManager = Depends(get_password_manager), 
                     token_manager: TokenManager = Depends(get_token_manager)) -> AuthService:
   
    return AuthService(UserDAO(session), pwd_manager=pwd_manager, token_manager=token_manager)
