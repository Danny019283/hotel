from domain.entities.room import Room
from domain.bussiness_rules.room_rules import RoomRules
from domain.exeptions import DomainError
from application.dtos.room_dto import CreateRoomDTO, RoomResponseDTO, UpdateRoomDTO
from infrastructure.repositories.booking_repo import Booking_repo
from infrastructure.repositories.room_repo import Room_repo
from infrastructure.repositories.room_type_repo import RoomType_repo


class RoomCases:
    def __init__(
        self,
        room_repo: Room_repo | None = None,
        room_type_repo: RoomType_repo | None = None,
        booking_repo: Booking_repo | None = None,
    ):
        self.room_repo = room_repo or Room_repo()
        self.room_type_repo = room_type_repo or RoomType_repo()
        self.booking_repo = booking_repo or Booking_repo()

    def _build_room(self, room_number: int, room_type_id: int) -> Room:
        room_type = self.room_type_repo.get_by_id(room_type_id)
        if room_type is None:
            raise DomainError("room type not found")
        return Room(
            room_number=room_number,
            room_type_id=room_type.room_type_id,
            room_type_name=room_type.name,
            room_type_description=room_type.description,
            capacity=room_type.capacity,
            base_price=room_type.base_price,
            room_type_active=room_type.active,
        )

    def _to_dto(self, room: Room) -> RoomResponseDTO:
        return RoomResponseDTO(
            room_number=room.room_number,
            room_type_id=room.room_type_id,
            room_type_name=room.room_type_name,
            room_type_description=room.room_type_description,
            capacity=room.capacity,
            base_price=float(room.base_price),
            room_type_active=room.room_type_active,
            can_delete=not self.booking_repo.room_has_bookings(room.room_number),
        )

    def register_room(self, room_number: int, room_type_id: int) -> Room:
        room = self._build_room(room_number, room_type_id)
        RoomRules.validate_room(room)
        self.room_repo.add(room)
        return room

    def register_room_dto(self, dto: CreateRoomDTO) -> RoomResponseDTO:
        room = self.register_room(dto.room_number, dto.room_type_id)
        return self._to_dto(room)

    def consult_room(self, room_number: int) -> Room | None:
        return self.room_repo.get_by_id(room_number)

    def consult_room_dto(self, room_number: int) -> RoomResponseDTO | None:
        room = self.consult_room(room_number)
        return self._to_dto(room) if room is not None else None

    def update_room(self, room_number: int, room_type_id: int) -> Room:
        existing_room = self.room_repo.get_by_id(room_number)
        if existing_room is None:
            raise DomainError("room not found")

        room = self._build_room(room_number, room_type_id)
        RoomRules.validate_price(room)
        RoomRules.validate_room_type(room)
        self.room_repo.update(room)
        return room

    def update_room_dto(self, room_number: int, dto: UpdateRoomDTO) -> RoomResponseDTO:
        room = self.update_room(room_number, dto.room_type_id)
        return self._to_dto(room)

    def list_rooms_dto(self) -> list[RoomResponseDTO]:
        rooms = self.room_repo.get_all() or []
        return [self._to_dto(room) for room in rooms]

    def delete_room(self, room_number: int) -> None:
        if self.room_repo.get_by_id(room_number) is None:
            raise DomainError("room not found")
        if self.booking_repo.room_has_bookings(room_number):
            raise DomainError("cannot delete a room that has bookings")
        self.room_repo.delete(room_number)
