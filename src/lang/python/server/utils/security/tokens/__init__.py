from typing import Literal
from datetime import datetime, timedelta
from jose import jwt

from server.utils import nowutc
from server.db.auth.schema import  ValidationTokenType
from server.utils.security.tokens.models import ValidationTokenResponse
from server.exceptions.auth import TokenExpiredException, TokenNotFoundException
from server.db.auth.dao import TokenDAO
from server.utils import cuid
from server.config import settings as s

class TokenManager:
    def __init__(self, dao: TokenDAO):
        self.token_dao = dao

    #NOTE: Acces token methods:

    def create_access_token(self, data: dict) -> str:
        """Create a JWT access token. Takes the data and the expiration time as arguments."""
        to_encode = data.copy()

        expires = self._set_token_expiration(s.ACCESS_TOKEN_EXPIRE_MINUTES)

        to_encode.update({"exp": expires})
        encoded_jwt = jwt.encode(to_encode, s.AUTH_SECRET, algorithm=s.ALGORITHM)

        return encoded_jwt

    #NOTE: Validation tokens methods:

    async def create_validation_token(self, user_id: str, token_type: ValidationTokenType) -> ValidationTokenResponse:
        """Create a validation token. Takes the user's id and the token type as arguments."""
        token = self._generate_validation_token(user_id, token_type)
        await self.token_dao.insert_validation_token(token)
        return token

    async def validate_validation_token(self, token_str: str) -> ValidationTokenResponse:
        """Validate a validation token. Takes the token string value as an argument."""
        token = await self.token_dao.get_validation_token(token_str)

        if not token:
            raise TokenNotFoundException()

        if token.expires_at < nowutc():
            raise TokenExpiredException()

        return ValidationTokenResponse(**token.model_dump())

    async def invalidate_validation_token(self, token_str: str) -> None:
        """Delete a validation token. Takes the token string value as an argument."""
        await self.token_dao.delete_validation_token(token_str)


    def _generate_validation_token(self, user_id: str, token_type:ValidationTokenType) -> ValidationTokenResponse:
        """ Generate either a verification or password reset token. Takes the user's id and the token type as arguments."""
        exp = s.VERIFICATION_TOKEN_EXPIRE_MINUTES if token_type == ValidationTokenType.VERIFICATION else s.PASSWORD_RESET_TOKEN_EXPIRE_MINUTES

        return ValidationTokenResponse(user_id=user_id, 
                                       token=cuid(), 
                                       expires_at=self._set_token_expiration(exp),
                                       token_type=token_type)

    #NOTE: General token methods:

    def _set_token_expiration(self, exp: int) -> datetime:
        return nowutc() + timedelta(minutes=exp)


