from src.domain.entities.room_type import RoomType
from src.domain.exeptions import RoomPriceError, RoomTypeError


class RoomTypeRules:
    @staticmethod
    def validate_room_type(room_type: RoomType) -> None:
        if room_type.capacity <= 0:
            raise RoomTypeError("capacity must be greater than zero")
        if room_type.base_price <= 0:
            raise RoomPriceError("base_price must be greater than zero")
