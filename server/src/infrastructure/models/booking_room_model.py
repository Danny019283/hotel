from typing import Optional
from sqlmodel import SQLModel, Field

class Booking_Room_model(SQLModel, table=True):
    __tablename__ = "Bookings_Rooms"
    booking_room_id: Optional[int] = Field(default=None, primary_key=True)
    booking_id: int = Field(foreign_key="Bookings.booking_id")
    room_number: int = Field(foreign_key="Rooms.room_number")
    price_per_night: float
    subtotal: float
    
