from typing import Sequence 
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from server.db.user.schema import User
from server.exceptions.user import UserNotFoundException
from server.services.user.models import UserRegistration, UserUpdate

class UserDAO:
    def __init__(self, session:AsyncSession):
        self.session = session

    async def get_user_by_id(self, id: str) -> User:
        result = await self.session.exec(select(User).where(User.id == id))
        user = result.first()

        if not user:
            raise UserNotFoundException()
        
        return user

    async def get_users(self) -> Sequence[User]:
        users =  await self.session.exec(select(User).order_by(User.last_name))
        return users.all()
    
    async def get_user_by_email(self, email: str) -> User:
        result = await self.session.exec(select(User).where(User.email == email))
        user = result.first()

        if not user:
            raise UserNotFoundException() 

        return user

    async def insert_user(self, user_data: UserRegistration) -> User:
        user = User(**user_data.model_dump())
        self.session.add(user)
        await self.session.commit()
        return user

    async def update_user(self, id: str, user_data: UserUpdate) -> User:
        user = await self.get_user_by_id(id)

        for key, value in user_data.model_dump().items():
            setattr(user, key, value)

        self.session.add(user)
        await self.session.commit()
        return user

    async def delete_user(self, id: str) -> None:
        user = await self.get_user_by_id(id)

        await self.session.delete(user)
        await self.session.commit()
