from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm

from server.db.user.dao import UserDAO
from server.db.auth.schema import ValidationTokenType
from server.exceptions.auth import InvalidCredentialsException, InvalidVerificationTokenException, TokenExpiredException, TokenNotFoundException
from server.exceptions.user import UserNotCreatedException
from server.services.auth.models import AuthRequest 
from server.services.user.models import UserRegistration  
from server.services.user import get_user_service, UserService
from server.db.user.schema import User
from server.utils.security.password import PasswordManager
from server.utils.security.tokens import TokenManager
from server.utils.security.tokens.models import AccessTokenResponse, RefreshTokenResponse

class AuthService:
    def __init__(self, user_dao: UserDAO, pwd_manager: PasswordManager, token_manager: TokenManager):
        self._user_dao = user_dao
        self._pwd_manager = pwd_manager
        self._token_manager = token_manager

    #NOTE: Public class methods:

    async def register(self, user_data: UserRegistration, user_service: UserService = Depends(get_user_service)) -> User:
        user = await user_service.create_user(user_data)

        if not user:
           raise UserNotCreatedException()

        #TODO: Implement email verification:
        # user the email service to generate the verifcation token and send the email.
        # email_service = get_email_service()
        # await email_service.send_verification_email(user.email)

        return user

    async def login(self, form_data: OAuth2PasswordRequestForm = Depends()) -> AccessTokenResponse:
        user = await self._authenticate_user(AuthRequest(email=form_data.username, password=form_data.password))
    
        if not user:
            raise InvalidCredentialsException()

        access_token = self._token_manager.create_access_token(
            data={"sub": user.id, "role": user.role} 
        )

        return AccessTokenResponse(token=access_token, token_type="bearer")

    async def logout(self):
        pass

    async def verify_email(self, verification_token: str):
        try:
            token = await self._token_manager.validate_validation_token(verification_token)
        except TokenNotFoundException:
            raise InvalidVerificationTokenException()
   


    async def reset_password(self, password_reset_token: str):
        pass


    #NOTE: Protected class methods:

    async def _authenticate_user(self, user_data: AuthRequest):
        """Authenticate a user. Uses a Pydantic model to validate the data."""
        user = await self._user_dao.get_user_by_email(user_data.email)

        if not user:
            return None
        if not self._pwd_manager.verify_password(user.password, user_data.password):
            return None 

        return user

