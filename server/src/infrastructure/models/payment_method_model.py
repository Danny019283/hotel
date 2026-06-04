from typing import Optional
from sqlmodel import SQLModel, Field

class Payment_Method_Model(SQLModel, table=True):
    __tablename__ = "Payment_methods"
    payment_method_id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=50)
    active: bool
