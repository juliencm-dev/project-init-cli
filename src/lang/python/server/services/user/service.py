from typing import Sequence
from fastapi import Depends

from server.db.user.dao import UserDAO
from server.db.user.schema import User, UserRole
from server.services.user.models import  UserRegistration, UserUpdate
from server.exceptions.user import UserRoleNotAllowedException, UserWithEmailAlreadyExistsException
from server.services.auth.dependencies import get_current_active_user
from server.utils.security import get_password_manager
from server.utils.security.password import PasswordManager

class UserService:
    def __init__(self, user_dao: UserDAO, current_user: User = Depends(get_current_active_user), pwd_manager: PasswordManager = Depends(get_password_manager)):
        self._user_dao = user_dao
        self._pwd_manager = pwd_manager
        self._current_user = current_user
    
    def get_current_user(self) -> User:
        return self._current_user

    async def get_user(self, user_id: str) -> User:
        self._check_user_permission(user_id)
        user = await self._user_dao.get_user_by_id(user_id)
        return user

    async def get_users(self) -> Sequence[User]:
        self._require_admin()
        users = await self._user_dao.get_users()
        return users

    async def create_user(self, user_data: UserRegistration) -> User:
        user = await self._user_dao.get_user_by_email(user_data.email)

        if user:
            raise UserWithEmailAlreadyExistsException()

        user_data.password = self._pwd_manager.hash_password(user_data.password)
        new_user = await self._user_dao.insert_user(user_data)
        return new_user

    async def update_user(self, user_id: str, user_data: UserUpdate) -> User:
        self._check_user_permission(user_id)
        updated_user = await self._user_dao.update_user(user_id, user_data)
        return updated_user

    async def delete_user(self, user_id: str) -> None:
        self._check_user_permission(user_id)
        await self._user_dao.delete_user(user_id)

    #NOTE: Permissions check functions:

    def _require_admin(self):
        if self._current_user.role != UserRole.ADMIN:
            raise UserRoleNotAllowedException()

    def _check_user_permission(self, target_user_id: str) -> None:
        if self._current_user.id != target_user_id and self._current_user.role != UserRole.ADMIN:
            raise UserRoleNotAllowedException()

