from server.db.auth.dao import AuthDAO
from server.db.user.dao import UserDAO


class AuthService:
    def __init__(self, user_dao: UserDAO, auth_dao: AuthDAO):
        self._user_dao = user_dao
        self._auth_dao = auth_dao

    async def register(self, user_data):
        pass

    async def login(self, user_data):
        pass

    async def logout(self):
        pass

    async def verify_email(self, user_data):
        pass

    async def reset_password(self, user_data):
        pass

