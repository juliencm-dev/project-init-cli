from pydantic import BaseModel

from server.db.user.schema import UserRole

class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: str

class UserRegistration(UserBase):
    password: str
    role: UserRole | None = None

class UserUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    password: str | None = None
    role: UserRole | None = None
    verified: bool | None = None

class UserResponse(UserBase):
    role: str
    verified: bool
