from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import Depends

from .service import AuthService
from server.db import get_session
from server.db.auth.dao import AuthDAO
from server.db.user.dao import UserDAO

def get_auth_service(session: AsyncSession = Depends(get_session)) -> AuthService:
    return AuthService(UserDAO(session), AuthDAO(session))
