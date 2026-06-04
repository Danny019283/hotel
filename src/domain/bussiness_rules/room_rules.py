from src.domain.entities.room import Room
from src.domain.exeptions import RoomAvailabilityError, RoomPriceError, RoomTypeError


class RoomRules:
    @staticmethod
    def validate_available(room: Room) -> None:
        if not room.available:
            raise RoomAvailabilityError("room is not available")

    @staticmethod
    def validate_price(room: Room) -> None:
        if room.price <= 0:
            raise RoomPriceError("room price must be greater than zero")

    @staticmethod
    def validate_room_type(room: Room) -> None:
        if not room.room_type.strip():
            raise RoomTypeError("room_type cannot be empty")

    @staticmethod
    def validate_room(room: Room) -> None:
        RoomRules.validate_available(room)
        RoomRules.validate_price(room)
        RoomRules.validate_room_type(room)
