from datetime import datetime
from pydantic import BaseModel
from sqlmodel import SQLModel, Field, Column
from sqlalchemy import event
import sqlalchemy.dialects.postgresql as pg
from cuid2 import Cuid as CUID2

def cuid():
    return CUID2().generate()

class UserResponse(BaseModel):
    id: str
    first_name: str
    last_name: str
    email: str
    created_at: datetime
    updated_at: datetime

class UserRequest(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str

class User(SQLModel, table=True):
    __tablename__ = 'users'
    id: str = Field(
        default_factory=cuid,
        sa_column=Column(pg.VARCHAR(length=24), primary_key=True, unique=True)
    )
    first_name: str 
    last_name: str 
    email: str = Field(nullable=False,unique=True, max_length=128)
    password: str 
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))


@event.listens_for(User, "before_update")
def update_timestamp(mapper, connection, target):
    target.updated_at = datetime.now()

