from pydantic import BaseModel
from datetime import datetime

from server.db.user.schema import UserRole

class UserResponse(BaseModel):
    id: str
    first_name: str
    last_name: str
    email: str
    role: UserRole
    verified: datetime | None
    created_at: datetime
    updated_at: datetime

class UserRequest(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str
