from domain.entities.booking import Booking
from domain.entities.payment_method import Payment_Method


class Bill:
    def __init__(self, bill_id: int | None, booking: Booking, payment_method: Payment_Method, total: float):
        self.bill_id = bill_id
        self.booking = booking
        self.payment_method = payment_method
        self.total = total

    @property
    def bill_id(self) -> int | None:
        return self.__bill_id

    @bill_id.setter
    def bill_id(self, value: int | None):
        if value is None:
            self.__bill_id = value
            return
        if not isinstance(value, int):
            raise TypeError("bill_id must be an int")
        if value <= 0:
            raise ValueError("bill_id must be positive")
        self.__bill_id = value

    @property
    def booking(self) -> Booking:
        return self.__booking

    @booking.setter
    def booking(self, value: Booking):
        if not isinstance(value, Booking):
            raise TypeError("booking must be a Booking instance")
        self.__booking = value

    @property
    def payment_method(self) -> Payment_Method:
        return self.__payment_method

    @payment_method.setter
    def payment_method(self, value: Payment_Method):
        if not isinstance(value, Payment_Method):
            raise TypeError("payment_method must be a Payment_Method instance")
        self.__payment_method = value

    @property
    def total(self) -> float:
        return self.__total

    @total.setter
    def total(self, value: float):
        if not isinstance(value, (int, float)):
            raise TypeError("total must be a number")
        if value < 0:
            raise ValueError("total cannot be negative")
        self.__total = float(value)
