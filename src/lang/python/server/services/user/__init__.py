from fastapi import Depends

from .service import UserService
from server.db import get_session
from server.db.user.dao import UserDAO

def get_user_service(session = Depends(get_session)) -> UserService:
    return UserService(UserDAO(session))
