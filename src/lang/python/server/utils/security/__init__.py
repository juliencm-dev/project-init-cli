from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from .password import PasswordManager
from .tokens import TokenManager
from server.db.auth.dao import TokenDAO
from server.db import get_session

def get_password_manager() -> PasswordManager:
    return PasswordManager()

def get_token_manager(session: AsyncSession = Depends(get_session)) -> TokenManager:
    return TokenManager(TokenDAO(session))

