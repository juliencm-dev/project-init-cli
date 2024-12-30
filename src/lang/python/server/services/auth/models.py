from datetime import datetime
from pydantic import BaseModel

class AuthRequest(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: str
    exp: datetime
