from decimal import Decimal

from application.dtos.room_type_dto import (
    ChangeRoomTypeStatusDTO,
    CreateRoomTypeDTO,
    RoomTypeResponseDTO,
    UpdateRoomTypeDTO,
)
from domain.bussiness_rules.room_type_rules import RoomTypeRules
from domain.entities.room_type import RoomType
from domain.exeptions import DomainError
from infrastructure.repositories.room_repo import Room_repo
from infrastructure.repositories.room_type_repo import RoomType_repo


class RoomTypeCases:
    def __init__(self, room_type_repo: RoomType_repo | None = None, room_repo: Room_repo | None = None):
        self.room_type_repo = room_type_repo or RoomType_repo()
        self.room_repo = room_repo or Room_repo()

    def _to_dto(self, room_type: RoomType) -> RoomTypeResponseDTO:
        rooms = self.room_repo.get_all() or []
        return RoomTypeResponseDTO(
            room_type_id=room_type.room_type_id,
            name=room_type.name,
            description=room_type.description,
            capacity=room_type.capacity,
            base_price=float(room_type.base_price),
            active=room_type.active,
            can_delete=not any(room.room_type_id == room_type.room_type_id for room in rooms),
        )

    def create_room_type(self, name: str, description: str, capacity: int, base_price: float, active: bool) -> RoomType:
        if self.room_type_repo.get_by_name(name.strip()) is not None:
            raise DomainError("room type already exists")
        room_type = RoomType(None, name, description, capacity, Decimal(str(base_price)), active)
        RoomTypeRules.validate_room_type(room_type)
        self.room_type_repo.add(room_type)
        return room_type

    def create_room_type_dto(self, dto: CreateRoomTypeDTO) -> RoomTypeResponseDTO:
        room_type = self.create_room_type(dto.name, dto.description, dto.capacity, dto.base_price, dto.active)
        return self._to_dto(room_type)

    def consult_room_type(self, room_type_id: int) -> RoomType | None:
        return self.room_type_repo.get_by_id(room_type_id)

    def consult_room_type_dto(self, room_type_id: int) -> RoomTypeResponseDTO | None:
        room_type = self.consult_room_type(room_type_id)
        return self._to_dto(room_type) if room_type is not None else None

    def list_room_types_dto(self) -> list[RoomTypeResponseDTO]:
        return [self._to_dto(room_type) for room_type in (self.room_type_repo.get_all() or [])]

    def update_room_type(self, room_type_id: int, name: str, description: str, capacity: int, base_price: float) -> RoomType:
        existing_room_type = self.room_type_repo.get_by_id(room_type_id)
        if existing_room_type is None:
            raise DomainError("room type not found")
        duplicated = self.room_type_repo.get_by_name(name.strip())
        if duplicated is not None and duplicated.room_type_id != room_type_id:
            raise DomainError("room type already exists")
        room_type = RoomType(room_type_id, name, description, capacity, Decimal(str(base_price)), existing_room_type.active)
        RoomTypeRules.validate_room_type(room_type)
        self.room_type_repo.update(room_type)
        return room_type

    def update_room_type_dto(self, room_type_id: int, dto: UpdateRoomTypeDTO) -> RoomTypeResponseDTO:
        room_type = self.update_room_type(room_type_id, dto.name, dto.description, dto.capacity, dto.base_price)
        return self._to_dto(room_type)

    def change_room_type_status(self, room_type_id: int, active: bool) -> RoomType:
        existing_room_type = self.room_type_repo.get_by_id(room_type_id)
        if existing_room_type is None:
            raise DomainError("room type not found")
        room_type = RoomType(
            room_type_id,
            existing_room_type.name,
            existing_room_type.description,
            existing_room_type.capacity,
            existing_room_type.base_price,
            active,
        )
        self.room_type_repo.update(room_type)
        return room_type

    def change_room_type_status_dto(self, room_type_id: int, dto: ChangeRoomTypeStatusDTO) -> RoomTypeResponseDTO:
        room_type = self.change_room_type_status(room_type_id, dto.active)
        return self._to_dto(room_type)

    def delete_room_type(self, room_type_id: int) -> None:
        if self.room_type_repo.get_by_id(room_type_id) is None:
            raise DomainError("room type not found")
        rooms = self.room_repo.get_all() or []
        if any(room.room_type_id == room_type_id for room in rooms):
            raise DomainError("cannot delete a room type assigned to rooms")
        self.room_type_repo.delete(room_type_id)
