from pydantic import BaseModel, Field


class CreateRoomTypeDTO(BaseModel):
    name: str = Field(min_length=1, max_length=50, description="Room type name", examples=["Suite"])
    description: str = Field(min_length=1, max_length=255, description="Room type description")
    capacity: int = Field(gt=0, description="Maximum room capacity", examples=[2])
    base_price: float = Field(gt=0, description="Base nightly price", examples=[150.0])
    active: bool = Field(default=True, description="Whether the room type is active")


class UpdateRoomTypeDTO(BaseModel):
    name: str = Field(min_length=1, max_length=50, description="Room type name", examples=["Suite"])
    description: str = Field(min_length=1, max_length=255, description="Room type description")
    capacity: int = Field(gt=0, description="Maximum room capacity", examples=[2])
    base_price: float = Field(gt=0, description="Base nightly price", examples=[150.0])


class ChangeRoomTypeStatusDTO(BaseModel):
    active: bool = Field(description="Whether the room type is active")


class RoomTypeResponseDTO(BaseModel):
    room_type_id: int = Field(description="Room type identifier", examples=[1])
    name: str = Field(description="Room type name", examples=["Suite"])
    description: str = Field(description="Room type description")
    capacity: int = Field(description="Maximum room capacity", examples=[2])
    base_price: float = Field(description="Base nightly price", examples=[150.0])
    active: bool = Field(description="Whether the room type is active")
