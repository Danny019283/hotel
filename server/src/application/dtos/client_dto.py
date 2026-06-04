from pydantic import BaseModel, Field, field_validator


class CreateClientDTO(BaseModel):
    client_id: str = Field(min_length=1, max_length=10, description="Unique client identifier", examples=["C001"])
    name: str = Field(min_length=1, max_length=50, description="Client first name", examples=["Juan"])
    last_name: str = Field(min_length=1, max_length=50, description="Client last name", examples=["Perez"])
    phone: int = Field(description="Client phone number with exactly 8 digits", examples=[88887777])
    email: str = Field(min_length=5, max_length=100, pattern=r"^[^\s@]+@[^\s@]+\.[^\s@]+$", description="Client email address", examples=["juan@example.com"])

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value: int) -> int:
        if value < 10000000 or value > 99999999:
            raise ValueError("phone must have exactly 8 digits")
        return value


class UpdateClientDTO(BaseModel):
    name: str = Field(min_length=1, max_length=50, description="Client first name", examples=["Juan"])
    last_name: str = Field(min_length=1, max_length=50, description="Client last name", examples=["Perez"])
    phone: int = Field(description="Client phone number with exactly 8 digits", examples=[88887777])
    email: str = Field(min_length=5, max_length=100, pattern=r"^[^\s@]+@[^\s@]+\.[^\s@]+$", description="Client email address", examples=["juan@example.com"])

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value: int) -> int:
        if value < 10000000 or value > 99999999:
            raise ValueError("phone must have exactly 8 digits")
        return value


class ClientResponseDTO(BaseModel):
    client_id: str = Field(description="Unique client identifier", examples=["C001"])
    name: str = Field(description="Client first name", examples=["Juan"])
    last_name: str = Field(description="Client last name", examples=["Perez"])
    phone: int = Field(description="Client phone number", examples=[88887777])
    email: str = Field(description="Client email address", examples=["juan@example.com"])
