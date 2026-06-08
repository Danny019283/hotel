from decimal import Decimal
from typing import Optional

from sqlalchemy import Column, Numeric
from sqlmodel import Field, SQLModel

class Bill_model(SQLModel, table=True):
    __tablename__ = "Bills"
    bill_id: Optional[int] = Field(default=None, primary_key=True)
    booking_id: int = Field(foreign_key="Bookings.booking_id", unique=True)
    payment_method_id: int = Field(foreign_key="Payment_methods.payment_method_id")
    total: Decimal = Field(sa_column=Column(Numeric(10, 2), nullable=False))
