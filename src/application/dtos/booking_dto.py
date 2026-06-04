from datetime import date

from pydantic import BaseModel, Field, field_validator


class CreateBookingDTO(BaseModel):
    client_id: str = Field(min_length=1, max_length=10, description="Client identifier", examples=["C001"])
    room_numbers: list[int] = Field(min_length=1, description="List of room numbers to reserve", examples=[[101, 102]])
    check_in: date = Field(description="Check-in date", examples=["2026-06-10"])
    check_out: date = Field(description="Check-out date", examples=["2026-06-12"])

    @field_validator("room_numbers")
    @classmethod
    def validate_room_numbers(cls, value: list[int]) -> list[int]:
        if not value:
            raise ValueError("room_numbers cannot be empty")
        if len(set(value)) != len(value):
            raise ValueError("room_numbers cannot contain duplicates")
        if any(room_number <= 0 for room_number in value):
            raise ValueError("room_numbers must contain only positive integers")
        return value


class UpdateBookingDatesDTO(BaseModel):
    check_in: date = Field(description="Updated check-in date", examples=["2026-06-11"])
    check_out: date = Field(description="Updated check-out date", examples=["2026-06-13"])


class BookingResponseDTO(BaseModel):
    booking_id: int = Field(description="Generated booking identifier", examples=[1])
    client_id: str = Field(description="Client identifier", examples=["C001"])
    room_numbers: list[int] = Field(description="Reserved room numbers", examples=[[101, 102]])
    check_in: date = Field(description="Check-in date", examples=["2026-06-10"])
    check_out: date = Field(description="Check-out date", examples=["2026-06-12"])


class BookingHistoryItemDTO(BaseModel):
    booking_id: int = Field(description="Booking identifier", examples=[1])
    room_numbers: list[int] = Field(description="Reserved room numbers", examples=[[101, 102]])
    room_types: list[str] = Field(description="Reserved room types", examples=[["Double", "Suite"]])
    check_in: date = Field(description="Check-in date", examples=["2026-06-10"])
    check_out: date = Field(description="Check-out date", examples=["2026-06-12"])
    total_days: int = Field(ge=1, description="Total number of nights", examples=[2])
