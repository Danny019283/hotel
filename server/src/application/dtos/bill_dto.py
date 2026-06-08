from pydantic import BaseModel, Field


class CreateBillDTO(BaseModel):
    booking_id: int = Field(gt=0, description="Booking identifier to bill", examples=[1])
    payment_method_id: int = Field(gt=0, description="Payment method identifier", examples=[2])


class UpdateBillPaymentMethodDTO(BaseModel):
    payment_method_id: int = Field(gt=0, description="Updated payment method identifier", examples=[2])


class BillResponseDTO(BaseModel):
    bill_id: int = Field(description="Generated bill identifier", examples=[1])
    booking_id: int = Field(description="Related booking identifier", examples=[1])
    payment_method_id: int = Field(description="Payment method identifier", examples=[2])
    total: float = Field(ge=0, description="Total bill amount", examples=[240.0])


class BillSummaryDTO(BaseModel):
    bill_id: int = Field(description="Bill identifier", examples=[1])
    booking_id: int = Field(description="Booking identifier", examples=[1])
    client_id: str = Field(description="Client identifier", examples=["C001"])
    room_numbers: list[int] = Field(description="Billed room numbers", examples=[[101, 102]])
    room_types: list[str] = Field(description="Billed room types", examples=[["Doble", "Suite"]])
    payment_method_id: int = Field(description="Payment method identifier", examples=[2])
    total: float = Field(ge=0, description="Total bill amount", examples=[240.0])
