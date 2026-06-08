from typing import Optional

from sqlalchemy import Column, LargeBinary
from sqlmodel import Field, SQLModel


class User_model(SQLModel, table=True):
    __tablename__ = "Users"
    user_id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(max_length=50, unique=True, index=True)
    password_hash: bytes = Field(sa_column=Column(LargeBinary))
    role: str = Field(max_length=30)
