from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from server.db.user.schema import User, UserRequest

class UserDAO:
    def __init__(self, session:AsyncSession):
        self.session = session

    async def get_user(self, id: str):
        user = await self.session.exec(select(User).where(User.id == id))
        return user.first()

    async def get_users(self):
        users =  await self.session.exec(select(User).order_by(User.last_name))
        return users.all()
    
    async def get_user_by_email(self, email: str):
        user = await self.session.exec(select(User).where(User.email == email))
        return user.first()

    async def create_user(self, user_data: UserRequest):
        user = User(**user_data.model_dump())
        self.session.add(user)
        await self.session.commit()
        return user

    async def update_user(self, id: str, user_data: UserRequest):
        result = await self.session.exec(select(User).where(User.id == id))
        user = result.first()

        #NOTE: I'm using model_dump() to get the data from the request and transform it to a dictionary to update the database.
        #NOTE: We can then use setattr() to update the attributes of the user object.

        for key, value in user_data.model_dump().items():
            setattr(user, key, value)

        self.session.add(user)
        await self.session.commit()
        return user

    async def delete_user(self, id: str):
        result = await self.session.exec(select(User).where(User.id == id))
        user = result.first()
        await self.session.delete(user)
        await self.session.commit()
