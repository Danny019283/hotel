from domain.entities.client import Client
from domain.entities.room import Room
from datetime import date


class Booking:
    def __init__(self, booking_id: int | None, client: Client, rooms: list[Room], check_in: date, check_out: date):
        self.booking_id = booking_id
        self.client = client
        self.rooms = rooms
        self.check_in = check_in
        self.check_out = check_out

    @property
    def booking_id(self) -> int | None:
        return self.__booking_id

    @booking_id.setter
    def booking_id(self, value: int | None):
        if value is None:
            self.__booking_id = value
            return
        if not isinstance(value, int):
            raise TypeError("booking_id must be an int")
        if value <= 0:
            raise ValueError("booking_id must be positive")
        self.__booking_id = value

    @property
    def client(self) -> Client:
        return self.__client

    @client.setter
    def client(self, value: Client):
        if not isinstance(value, Client):
            raise TypeError("client must be a Client instance")
        self.__client = value

    @property
    def rooms(self) -> list[Room]:
        return self.__rooms

    @rooms.setter
    def rooms(self, value: list[Room]):
        if not isinstance(value, list):
            raise TypeError("rooms must be a list of Room instances")
        if not value:
            raise ValueError("rooms cannot be empty")
        if not all(isinstance(room, Room) for room in value):
            raise TypeError("rooms must contain only Room instances")
        self.__rooms = value

    @property
    def check_in(self) -> date:
        return self.__check_in

    @check_in.setter
    def check_in(self, value: date):
        if not isinstance(value, date):
            raise TypeError("check_in must be a date")
        self.__check_in = value

    @property
    def check_out(self) -> date:
        return self.__check_out

    @check_out.setter
    def check_out(self, value: date):
        if not isinstance(value, date):
            raise TypeError("check_out must be a date")
        if hasattr(self, '_Booking__check_in') and value < self.__check_in:
            raise ValueError("check_out cannot be before check_in")
        self.__check_out = value
