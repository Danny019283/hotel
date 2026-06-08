from pydantic import BaseModel, Field


class CreateRoomDTO(BaseModel):
    room_number: int = Field(gt=0, description="Room number", examples=[101])
    room_type_id: int = Field(gt=0, description="Room type identifier", examples=[1])


class UpdateRoomDTO(BaseModel):
    room_type_id: int = Field(gt=0, description="Room type identifier", examples=[1])


class RoomResponseDTO(BaseModel):
    room_number: int = Field(description="Room number", examples=[101])
    room_type_id: int = Field(description="Room type identifier", examples=[1])
    room_type_name: str = Field(description="Room type", examples=["Doble"])
    room_type_description: str = Field(description="Room type description")
    capacity: int = Field(description="Room type capacity", examples=[2])
    base_price: float = Field(description="Room base price per night", examples=[120.0])
    room_type_active: bool = Field(description="Whether the room type is active")
    can_delete: bool = Field(description="Whether the room can be deleted")
