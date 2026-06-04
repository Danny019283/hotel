from pydantic import BaseModel, Field


class CreateRoomDTO(BaseModel):
    room_number: int = Field(gt=0, description="Room number", examples=[101])
    room_type: str = Field(min_length=1, max_length=50, description="Room type", examples=["Double"])
    price: float = Field(gt=0, description="Room base price per night", examples=[120.0])
    available: bool = Field(default=True, description="Whether the room is available for reservation")


class UpdateRoomDTO(BaseModel):
    room_type: str = Field(min_length=1, max_length=50, description="Room type", examples=["Double"])
    price: float = Field(gt=0, description="Room base price per night", examples=[120.0])


class ChangeRoomStatusDTO(BaseModel):
    available: bool = Field(description="Whether the room is available for reservation")


class RoomResponseDTO(BaseModel):
    room_number: int = Field(description="Room number", examples=[101])
    room_type: str = Field(description="Room type", examples=["Double"])
    price: float = Field(description="Room base price per night", examples=[120.0])
    available: bool = Field(description="Whether the room is available for reservation")
