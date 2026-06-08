from typing import Literal

from pydantic import BaseModel, Field


RoomType = Literal["Suite", "Doble", "Individual"]


class CreateRoomDTO(BaseModel):
    room_number: int = Field(gt=0, description="Room number", examples=[101])
    room_type: RoomType = Field(description="Room type", examples=["Doble"])
    price: float = Field(gt=0, description="Room base price per night", examples=[120.0])
    available: bool = Field(default=True, description="Whether the room is available for reservation")


class UpdateRoomDTO(BaseModel):
    room_type: RoomType = Field(description="Room type", examples=["Doble"])
    price: float = Field(gt=0, description="Room base price per night", examples=[120.0])


class ChangeRoomStatusDTO(BaseModel):
    available: bool = Field(description="Whether the room is available for reservation")


class RoomResponseDTO(BaseModel):
    room_number: int = Field(description="Room number", examples=[101])
    room_type: str = Field(description="Room type", examples=["Doble"])
    price: float = Field(description="Room base price per night", examples=[120.0])
    available: bool = Field(description="Whether the room is available for reservation")
