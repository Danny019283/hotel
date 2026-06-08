from pydantic import BaseModel, Field


class PaymentMethodResponseDTO(BaseModel):
    payment_method_id: int = Field(description="Payment method identifier")
    name: str = Field(description="Payment method display name")
    active: bool = Field(description="Whether the payment method can be used")
