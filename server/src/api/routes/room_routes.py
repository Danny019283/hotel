from fastapi import APIRouter, Depends, HTTPException, status

from api.security import AuthenticatedUser, get_current_user, require_admin
from application.dtos.room_dto import CreateRoomDTO, RoomResponseDTO, UpdateRoomDTO
from application.uses_cases.room_cases import RoomCases
from domain.exeptions import DomainError


router = APIRouter(prefix="/rooms", tags=["Rooms"])
room_cases = RoomCases()


@router.post("", response_model=RoomResponseDTO, status_code=status.HTTP_201_CREATED)
def register_room(dto: CreateRoomDTO, _: AuthenticatedUser = Depends(require_admin)):
    try:
        return room_cases.register_room_dto(dto)
    except DomainError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get("/{room_number}", response_model=RoomResponseDTO)
def consult_room(room_number: int, _: AuthenticatedUser = Depends(get_current_user)):
    room = room_cases.consult_room_dto(room_number)
    if room is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="room not found")
    return room


@router.put("/{room_number}", response_model=RoomResponseDTO)
def update_room(room_number: int, dto: UpdateRoomDTO, _: AuthenticatedUser = Depends(require_admin)):
    try:
        return room_cases.update_room_dto(room_number, dto)
    except DomainError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get("", response_model=list[RoomResponseDTO])
def list_rooms(_: AuthenticatedUser = Depends(get_current_user)):
    return room_cases.list_rooms_dto()


@router.delete("/{room_number}", status_code=status.HTTP_204_NO_CONTENT)
def delete_room(room_number: int, _: AuthenticatedUser = Depends(require_admin)):
    try:
        room_cases.delete_room(room_number)
    except DomainError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
