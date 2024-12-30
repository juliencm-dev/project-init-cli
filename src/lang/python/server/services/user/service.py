from typing import List

from server.db.user.dao import UserDAO
from server.services.user.models import UserRequest, UserResponse

class UserService:
    def __init__(self, user_dao: UserDAO):
        self._dao = user_dao
    
    async def get_users(self) -> List[UserResponse]:
        pass
    
    async def get_user(self, user_id: str) -> UserResponse:
        pass
    
    async def create_user(self, user_data: UserRequest) -> UserResponse:
        pass
    
    async def update_user(self, user_id: str, user_data: UserRequest) -> UserResponse:
        pass
    
    async def delete_user(self, user_id: str) -> None:
        pass
