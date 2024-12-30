from datetime import datetime
from pydantic import BaseModel
from sqlmodel import Enum, SQLModel, Field, Column
from sqlalchemy import event
import sqlalchemy.dialects.postgresql as pg

from server.utils import nowutc, cuid

#NOTE: If you wish to add RBAC to your app, you can uncomment the different role fields.

class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"



class User(SQLModel, table=True):
    __tablename__ = 'users'
    id: str = Field(
        default_factory=cuid,
        sa_column=Column(
            pg.VARCHAR(length=24), 
            primary_key=True, 
            unique=True
        )
    )
    first_name: str 
    last_name: str 
    email: str = Field(
        sa_column=Column(
            pg.VARCHAR(length=128), 
            nullable=False, 
            unique=True
        )
    )
    password: str 
    verified: datetime = Field(
        sa_column=Column(
            pg.TIMESTAMP, 
            default=None, 
            nullable=True
        )
    )
    role: UserRole = Field(
        sa_column=Column(
            pg.VARCHAR(length=16), 
            default=UserRole.USER)
    )
    created_at: datetime = Field(
        sa_column=Column(
            pg.TIMESTAMP, 
            default=nowutc)
    )
    updated_at: datetime = Field(
        sa_column=Column(
            pg.TIMESTAMP, 
            default=nowutc)
    )

@event.listens_for(User, "after_update")
def update_timestamp(mapper, connection, target):
    target.updated_at = nowutc()

