from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from server.auth.dependencies import generate_validation_token
from server.db.auth.schema import ValidationTokenType, ValidationToken

class AuthDAO:
    def __init__(self, session:AsyncSession):
        self.session = session

    #NOTE: Validation tokens DAO methods:
    async def get_validation_token(self, token: str): 
        token_data = await self.session.exec(select(ValidationToken).where(ValidationToken.token == token))
        return token_data.first()

    async def create_validation_token(self, user_id: str, token_type: ValidationTokenType):
        token = generate_validation_token(user_id, token_type)
        self.session.add(token)
        await self.session.commit()
        return token

    async def delete_validation_token(self, token_data: ValidationToken):
        result = await self.session.exec(select(ValidationToken).where(ValidationToken.token == token_data.token))
        token = result.first()
        await self.session.delete(token)
        await self.session.commit()


