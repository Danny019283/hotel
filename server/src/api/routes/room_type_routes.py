from fastapi import APIRouter, Depends, HTTPException, status

from api.security import AuthenticatedUser, get_current_user, require_admin
from application.dtos.room_type_dto import (
    ChangeRoomTypeStatusDTO,
    CreateRoomTypeDTO,
    RoomTypeResponseDTO,
    UpdateRoomTypeDTO,
)
from application.uses_cases.room_type_cases import RoomTypeCases
from domain.exeptions import DomainError


router = APIRouter(prefix="/room-types", tags=["Room types"])
room_type_cases = RoomTypeCases()


@router.post("", response_model=RoomTypeResponseDTO, status_code=status.HTTP_201_CREATED)
def create_room_type(dto: CreateRoomTypeDTO, _: AuthenticatedUser = Depends(require_admin)):
    try:
        return room_type_cases.create_room_type_dto(dto)
    except DomainError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get("", response_model=list[RoomTypeResponseDTO])
def list_room_types(_: AuthenticatedUser = Depends(get_current_user)):
    return room_type_cases.list_room_types_dto()


@router.get("/{room_type_id}", response_model=RoomTypeResponseDTO)
def consult_room_type(room_type_id: int, _: AuthenticatedUser = Depends(get_current_user)):
    room_type = room_type_cases.consult_room_type_dto(room_type_id)
    if room_type is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="room type not found")
    return room_type


@router.put("/{room_type_id}", response_model=RoomTypeResponseDTO)
def update_room_type(
    room_type_id: int,
    dto: UpdateRoomTypeDTO,
    _: AuthenticatedUser = Depends(require_admin),
):
    try:
        return room_type_cases.update_room_type_dto(room_type_id, dto)
    except DomainError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.patch("/{room_type_id}/status", response_model=RoomTypeResponseDTO)
def change_room_type_status(
    room_type_id: int,
    dto: ChangeRoomTypeStatusDTO,
    _: AuthenticatedUser = Depends(require_admin),
):
    try:
        return room_type_cases.change_room_type_status_dto(room_type_id, dto)
    except DomainError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.delete("/{room_type_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_room_type(room_type_id: int, _: AuthenticatedUser = Depends(require_admin)):
    try:
        room_type_cases.delete_room_type(room_type_id)
    except DomainError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
