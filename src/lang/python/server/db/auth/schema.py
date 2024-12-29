from datetime import datetime
from sqlmodel import Enum, PrimaryKeyConstraint, SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg

from server.utils import nowutc

class ValidationTokenType(str, Enum):
    VERIFICATION = "verification"
    PASSWORD_RESET = "password_reset"

class ValidationToken(SQLModel, table=True):
    __tablename__ = 'verification_tokens'
    __table_args__ = (PrimaryKeyConstraint('user_id', 'token', name='verification_tokens_pk'))
    user_id: str = Field(
        sa_column=Column(
            pg.VARCHAR(length=24), 
            nullable=False, 
            unique=True
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
            Enum(ValidationTokenType),
            nullable=False
        )
    )
    expires_at: datetime = Field(
        sa_column=Column(
            pg.TIMESTAMP, 
            default=nowutc)
    )




