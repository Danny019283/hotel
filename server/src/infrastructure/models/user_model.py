from sqlalchemy import LargeBinary, Column
from sqlmodel import Field, SQLModel


class User_model(SQLModel, table=True):
    __tablename__ = "Users"
    username: str = Field(primary_key=True, max_length=50)
    password_hash: bytes = Field(sa_column=Column(LargeBinary))
    role: str = Field(max_length=30)
