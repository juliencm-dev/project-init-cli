from enum import Enum
from datetime import datetime
from sqlmodel import PrimaryKeyConstraint, SQLModel, Field, Column, Index
import sqlalchemy.dialects.postgresql as pg

from server.utils import nowutc

class ValidationTokenType(str, Enum):
    VERIFICATION = "verification"
    PASSWORD_RESET = "password_reset"

class ValidationToken(SQLModel, table=True):
    __tablename__ = 'validation_tokens'
    __table_args__ = (PrimaryKeyConstraint('user_id', 'token', name='verification_tokens_pk'))
    user_id: str = Field(
        sa_column=Column(
            foreign_key="user.id"
        )
    )
    token: str = Field(
        sa_column=Column(
            pg.VARCHAR(length=255), 
            nullable=False, 
            unique=True
        )
    )
    token_type: ValidationTokenType = Field(
        sa_column=Column(
            pg.ENUM(ValidationTokenType),
            nullable=False
        )
    )
    expires_at: datetime = Field(
        sa_column=Column(
            pg.TIMESTAMP, 
            default=nowutc)
    )


class RefreshToken(SQLModel, table=True):
    __tablename__ = 'refresh_tokens'
    __table_args__ = (PrimaryKeyConstraint('user_id', 'token', 'device', name='refresh_tokens_pk')),
    user_id: str = Field(
        sa_column=Column(
            foreign_key="user.id",
        )
    )
    token: str = Field(
        sa_column=Column(
            pg.VARCHAR(length=255), 
            nullable=False, 
            unique=True,
        )
    )
    device: str = Field(
        sa_column=Column(
            pg.VARCHAR(length=255), 
            nullable=True,
            index=True
        )
    )
    last_used: datetime = Field(
        sa_column=Column(
            pg.TIMESTAMP, 
            default=nowutc)
    )
    expires_at: datetime = Field(
        sa_column=Column(
            pg.TIMESTAMP, 
            default=nowutc)
    )



