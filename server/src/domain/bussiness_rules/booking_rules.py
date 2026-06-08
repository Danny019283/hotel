from decimal import Decimal
from datetime import date

from src.domain.entities.booking import Booking
from src.domain.exeptions import BookingDatesError, BookingOverlapError, BookingPastDateError, BookingStayError


class BookingRules:
    @staticmethod
    def calculate_nights(check_in: date, check_out: date) -> int:
        nights = (check_out - check_in).days
        if nights <= 0:
            raise BookingStayError("booking must last at least one night")
        return nights

    @staticmethod
    def validate_check_in_before_check_out(check_in: date, check_out: date) -> None:
        if check_in > check_out:
            raise BookingDatesError("check_in cannot be greater than check_out")

    @staticmethod
    def validate_minimum_stay(check_in: date, check_out: date) -> None:
        BookingRules.calculate_nights(check_in, check_out)

    @staticmethod
    def validate_not_in_past(check_in: date) -> None:
        if check_in < date.today():
            raise BookingPastDateError("check_in cannot be in the past")

    @staticmethod
    def validate_no_overlap(has_overlap: bool, room_number: int) -> None:
        if has_overlap:
            raise BookingOverlapError(f"room {room_number} is already booked for the selected dates")

    @staticmethod
    def calculate_room_subtotal(room, check_in: date, check_out: date) -> float:
        nights = BookingRules.calculate_nights(check_in, check_out)
        return room.base_price * Decimal(nights)

    @staticmethod
    def calculate_booking_total(booking: Booking) -> float:
        nights = BookingRules.calculate_nights(booking.check_in, booking.check_out)
        total = sum((room.base_price for room in booking.rooms), Decimal("0.00"))
        return total * Decimal(nights)

    @staticmethod
    def validate_booking(booking: Booking) -> None:
        BookingRules.validate_check_in_before_check_out(booking.check_in, booking.check_out)
        BookingRules.validate_minimum_stay(booking.check_in, booking.check_out)
        BookingRules.validate_not_in_past(booking.check_in)
