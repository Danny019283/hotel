from typing import Optional

from sqlmodel import Field, SQLModel

class Room_model(SQLModel, table=True):
    __tablename__ = "Rooms"
    room_number: Optional[int] = Field(default=None, primary_key=True)
    room_type_id: int = Field(foreign_key="Room_Types.room_type_id")
    available: bool = Field(default=True)
