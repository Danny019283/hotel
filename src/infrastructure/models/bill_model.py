from typing import Optional
from sqlmodel import SQLModel, Field

class Bill_model(SQLModel, table=True):
    __tablename__ = "Bills"
    bill_id: Optional[int] = Field(default=None, primary_key=True)
    booking_id: int = Field(foreign_key="Bookings.booking_id", unique=True)
    payment_method_id: int = Field(foreign_key="Payment_methods.payment_method_id")
    total: float
