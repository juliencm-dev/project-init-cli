from pydantic import BaseModel
from server.utils.security.tokens.models import AccessTokenData, RefreshTokenData

class AuthRequest(BaseModel):
    email: str
    password: str

class AuthResponse(BaseModel):
    access_token: AccessTokenData
    refresh_token: RefreshTokenData 

