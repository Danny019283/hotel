from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status

from api.security import AuthenticatedUser, get_current_user
from application.dtos.booking_dto import (
    BookingHistoryItemDTO,
    BookingResponseDTO,
    CreateBookingDTO,
    OccupiedDateRangeDTO,
    UpdateBookingDatesDTO,
)
from application.uses_cases.booking_cases import BookingCases
from domain.exeptions import DomainError


router = APIRouter(prefix="/bookings", tags=["Bookings"])
booking_cases = BookingCases()


@router.post("", response_model=BookingResponseDTO, status_code=status.HTTP_201_CREATED)
def create_booking(dto: CreateBookingDTO, _: AuthenticatedUser = Depends(get_current_user)):
    try:
        return booking_cases.create_booking_dto(dto)
    except DomainError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get("/client/{client_id}/history", response_model=list[BookingHistoryItemDTO])
def history_by_client(client_id: str, _: AuthenticatedUser = Depends(get_current_user)):
    return booking_cases.history_by_client_dto(client_id)


@router.get("/rooms/{room_number}/occupied-ranges", response_model=list[OccupiedDateRangeDTO])
def occupied_ranges_by_room(room_number: int, _: AuthenticatedUser = Depends(get_current_user)):
    try:
        return booking_cases.occupied_ranges_by_room_dto(room_number)
    except DomainError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.get("", response_model=list[BookingResponseDTO])
def list_bookings(_: AuthenticatedUser = Depends(get_current_user)):
    return booking_cases.list_bookings_dto()


@router.get("/{booking_id}", response_model=BookingResponseDTO)
def consult_booking(booking_id: int, _: AuthenticatedUser = Depends(get_current_user)):
    booking = booking_cases.consult_booking_dto(booking_id)
    if booking is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="booking not found")
    return booking


@router.put("/{booking_id}/dates", response_model=BookingResponseDTO)
def modify_booking_dates(
    booking_id: int,
    dto: UpdateBookingDatesDTO,
    _: AuthenticatedUser = Depends(get_current_user),
):
    try:
        return booking_cases.modify_booking_dates_dto(booking_id, dto)
    except DomainError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.delete("/{booking_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_booking(booking_id: int, _: AuthenticatedUser = Depends(get_current_user)):
    try:
        booking_cases.delete_booking(booking_id)
    except DomainError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
