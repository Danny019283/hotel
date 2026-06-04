from typing import Optional
from sqlmodel import SQLModel, Field

class Room_model(SQLModel, table=True):
    __tablename__ = "Rooms"
    room_number: Optional[int] = Field(default=None, primary_key=True)
    room_type: str = Field(max_length=50)
    price: float
    available: bool
