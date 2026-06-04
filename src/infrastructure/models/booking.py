from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import date

class Booking_model(SQLModel, table=True):
    __tablename__ = "Bookings"
    booking_id: Optional[int] = Field(default=None, primary_key=True)
    check_in: date
    check_out: date
    client_id: str = Field(foreign_key="Clients.client_id", max_length=10)
