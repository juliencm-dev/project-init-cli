from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from server.db.auth.schema import  ValidationToken
from server.utils.security.tokens.models import ValidationTokenResponse
from server.exceptions.auth import TokenNotCreatedException, TokenNotFoundException

class TokenDAO:
    def __init__(self, session:AsyncSession):
        self.session = session

    #NOTE: Validation tokens DAO methods:
    async def get_validation_token(self, token: str): 
        token_data = await self.session.exec(select(ValidationToken).where(ValidationToken.token == token))
        return token_data.first()

    async def insert_validation_token(self, token_data: ValidationTokenResponse):
        try:
            self.session.add(ValidationToken(**token_data.model_dump()))
            await self.session.commit()
        except Exception:
            await self.session.rollback()
            raise TokenNotCreatedException()

        return token_data

    async def delete_validation_token(self, token_str: str):
        result = await self.session.exec(select(ValidationToken).where(ValidationToken.token == token_str))
        token = result.first()

        if not token:
            raise TokenNotFoundException()

        await self.session.delete(token)
        await self.session.commit()


