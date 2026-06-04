from domain.entities.room import Room
from domain.bussiness_rules.room_rules import RoomRules
from domain.exeptions import DomainError
from application.dtos.room_dto import ChangeRoomStatusDTO, CreateRoomDTO, RoomResponseDTO, UpdateRoomDTO
from infrastructure.repositories.room_repo import Room_repo


class RoomCases:
    def __init__(self, room_repo: Room_repo | None = None):
        self.room_repo = room_repo or Room_repo()

    def register_room(self, room_number: int, room_type: str, price: float, available: bool = True) -> Room:
        room = Room(room_number, room_type, price, available)
        RoomRules.validate_room(room)
        self.room_repo.add(room)
        return room

    def register_room_dto(self, dto: CreateRoomDTO) -> RoomResponseDTO:
        room = self.register_room(dto.room_number, dto.room_type, dto.price, dto.available)
        return RoomResponseDTO(
            room_number=room.room_number,
            room_type=room.room_type,
            price=room.price,
            available=room.available,
        )

    def consult_room(self, room_number: int) -> Room | None:
        return self.room_repo.get_by_id(room_number)

    def consult_room_dto(self, room_number: int) -> RoomResponseDTO | None:
        room = self.consult_room(room_number)
        if room is None:
            return None
        return RoomResponseDTO(
            room_number=room.room_number,
            room_type=room.room_type,
            price=room.price,
            available=room.available,
        )

    def update_room(self, room_number: int, room_type: str, price: float) -> Room:
        existing_room = self.room_repo.get_by_id(room_number)
        if existing_room is None:
            raise DomainError("room not found")

        room = Room(room_number, room_type, price, existing_room.available)
        RoomRules.validate_price(room)
        RoomRules.validate_room_type(room)
        self.room_repo.update(room)
        return room

    def update_room_dto(self, room_number: int, dto: UpdateRoomDTO) -> RoomResponseDTO:
        room = self.update_room(room_number, dto.room_type, dto.price)
        return RoomResponseDTO(
            room_number=room.room_number,
            room_type=room.room_type,
            price=room.price,
            available=room.available,
        )

    def change_room_status(self, room_number: int, available: bool) -> Room:
        existing_room = self.room_repo.get_by_id(room_number)
        if existing_room is None:
            raise DomainError("room not found")

        room = Room(existing_room.room_number, existing_room.room_type, existing_room.price, available)
        self.room_repo.update(room)
        return room

    def change_room_status_dto(self, room_number: int, dto: ChangeRoomStatusDTO) -> RoomResponseDTO:
        room = self.change_room_status(room_number, dto.available)
        return RoomResponseDTO(
            room_number=room.room_number,
            room_type=room.room_type,
            price=room.price,
            available=room.available,
        )

    def consult_available_rooms(self) -> list[Room]:
        rooms = self.room_repo.get_all() or []
        return [room for room in rooms if room.available]

    def consult_available_rooms_dto(self) -> list[RoomResponseDTO]:
        return [
            RoomResponseDTO(
                room_number=room.room_number,
                room_type=room.room_type,
                price=room.price,
                available=room.available,
            )
            for room in self.consult_available_rooms()
        ]

    def list_rooms_dto(self) -> list[RoomResponseDTO]:
        rooms = self.room_repo.get_all() or []
        return [
            RoomResponseDTO(
                room_number=room.room_number,
                room_type=room.room_type,
                price=room.price,
                available=room.available,
            )
            for room in rooms
        ]
