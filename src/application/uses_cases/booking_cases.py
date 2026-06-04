from datetime import date

from application.dtos.booking_dto import BookingHistoryItemDTO, BookingResponseDTO, CreateBookingDTO, UpdateBookingDatesDTO
from domain.bussiness_rules.booking_rules import BookingRules
from domain.entities.booking import Booking
from domain.exeptions import DomainError
from infrastructure.repositories.booking_repo import Booking_repo
from infrastructure.repositories.client_repo import Client_repo
from infrastructure.repositories.room_repo import Room_repo


class BookingCases:
    def __init__(
        self,
        booking_repo: Booking_repo | None = None,
        client_repo: Client_repo | None = None,
        room_repo: Room_repo | None = None,
    ):
        self.booking_repo = booking_repo or Booking_repo()
        self.client_repo = client_repo or Client_repo()
        self.room_repo = room_repo or Room_repo()

    def _validate_room_overlaps(
        self,
        room_numbers: list[int],
        check_in: date,
        check_out: date,
        exclude_booking_id: int | None = None,
    ) -> None:
        for room_number in room_numbers:
            has_overlap = self.booking_repo.exists_overlap(
                room_number,
                check_in,
                check_out,
                exclude_booking_id=exclude_booking_id,
            )
            BookingRules.validate_no_overlap(has_overlap, room_number)

    def create_booking(
        self,
        client_id: str,
        room_numbers: list[int],
        check_in: date,
        check_out: date,
    ) -> Booking:
        client = self.client_repo.get_by_id(client_id)
        if client is None:
            raise DomainError("client not found")

        rooms = []
        for room_number in room_numbers:
            room = self.room_repo.get_by_id(room_number)
            if room is None:
                raise DomainError(f"room {room_number} not found")
            rooms.append(room)

        booking = Booking(None, client, rooms, check_in, check_out)
        BookingRules.validate_booking(booking)
        self._validate_room_overlaps(room_numbers, check_in, check_out)
        self.booking_repo.add(booking)
        return booking

    def create_booking_dto(self, dto: CreateBookingDTO) -> BookingResponseDTO:
        booking = self.create_booking(dto.client_id, dto.room_numbers, dto.check_in, dto.check_out)
        return BookingResponseDTO(
            booking_id=booking.booking_id,
            client_id=booking.client.client_id,
            room_numbers=[room.room_number for room in booking.rooms],
            check_in=booking.check_in,
            check_out=booking.check_out,
        )

    def consult_booking(self, booking_id: int) -> Booking | None:
        return self.booking_repo.get_by_id(booking_id)

    def consult_booking_dto(self, booking_id: int) -> BookingResponseDTO | None:
        booking = self.consult_booking(booking_id)
        if booking is None:
            return None
        return BookingResponseDTO(
            booking_id=booking.booking_id,
            client_id=booking.client.client_id,
            room_numbers=[room.room_number for room in booking.rooms],
            check_in=booking.check_in,
            check_out=booking.check_out,
        )

    def modify_booking_dates(self, booking_id: int, check_in: date, check_out: date) -> Booking:
        existing_booking = self.booking_repo.get_by_id(booking_id)
        if existing_booking is None:
            raise DomainError("booking not found")

        booking = Booking(
            existing_booking.booking_id,
            existing_booking.client,
            existing_booking.rooms,
            check_in,
            check_out,
        )
        BookingRules.validate_booking(booking)
        self._validate_room_overlaps(
            [room.room_number for room in existing_booking.rooms],
            check_in,
            check_out,
            exclude_booking_id=existing_booking.booking_id,
        )
        self.booking_repo.update(booking)
        return booking

    def modify_booking_dates_dto(self, booking_id: int, dto: UpdateBookingDatesDTO) -> BookingResponseDTO:
        booking = self.modify_booking_dates(booking_id, dto.check_in, dto.check_out)
        return BookingResponseDTO(
            booking_id=booking.booking_id,
            client_id=booking.client.client_id,
            room_numbers=[room.room_number for room in booking.rooms],
            check_in=booking.check_in,
            check_out=booking.check_out,
        )

    def history_by_client(self, client_id: str) -> list[Booking]:
        bookings = self.booking_repo.get_all() or []
        return [booking for booking in bookings if booking.client.client_id == client_id]

    def history_by_client_dto(self, client_id: str) -> list[BookingHistoryItemDTO]:
        return [
            BookingHistoryItemDTO(
                booking_id=booking.booking_id,
                room_numbers=[room.room_number for room in booking.rooms],
                room_types=[room.room_type for room in booking.rooms],
                check_in=booking.check_in,
                check_out=booking.check_out,
                total_days=(booking.check_out - booking.check_in).days,
            )
            for booking in self.history_by_client(client_id)
        ]

    def list_bookings_dto(self) -> list[BookingResponseDTO]:
        return [
            BookingResponseDTO(
                booking_id=booking.booking_id,
                client_id=booking.client.client_id,
                room_numbers=[room.room_number for room in booking.rooms],
                check_in=booking.check_in,
                check_out=booking.check_out,
            )
            for booking in (self.booking_repo.get_all() or [])
        ]
