from decimal import Decimal
from typing import Optional

from sqlalchemy import Column, Numeric
from sqlmodel import Field, SQLModel


class Room_Type_model(SQLModel, table=True):
    __tablename__ = "Room_Types"

    room_type_id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=50, unique=True)
    description: str = Field(max_length=255)
    capacity: int = Field(gt=0)
    base_price: Decimal = Field(sa_column=Column(Numeric(10, 2), nullable=False))
    active: bool = Field(default=True)
