from decimal import Decimal
from typing import Optional

from sqlalchemy import Column, Numeric
from sqlmodel import Field, SQLModel

class Booking_Room_model(SQLModel, table=True):
    __tablename__ = "Bookings_Rooms"
    booking_room_id: Optional[int] = Field(default=None, primary_key=True)
    booking_id: int = Field(foreign_key="Bookings.booking_id")
    room_number: int = Field(foreign_key="Rooms.room_number")
    price_per_night: Decimal = Field(sa_column=Column(Numeric(10, 2), nullable=False))
    subtotal: Decimal = Field(sa_column=Column(Numeric(10, 2), nullable=False))
    
