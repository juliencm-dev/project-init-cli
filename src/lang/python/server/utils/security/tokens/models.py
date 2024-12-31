from datetime import datetime
from pydantic import BaseModel

class AccessTokenResponse(BaseModel):
    token: str
    token_type: str

class RefreshTokenResponse(BaseModel):
    token: str
    expires_at: datetime

class ValidationTokenResponse(BaseModel):
    user_id: str
    token: str
    expires_at: datetime
    token_type: str



