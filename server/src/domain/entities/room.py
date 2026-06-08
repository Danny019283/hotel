from decimal import Decimal


class Room:
    def __init__(
        self,
        room_number: int,
        room_type_id: int,
        room_type_name: str,
        room_type_description: str,
        capacity: int,
        base_price,
        room_type_active: bool,
    ):
        self.room_number = room_number
        self.room_type_id = room_type_id
        self.room_type_name = room_type_name
        self.room_type_description = room_type_description
        self.capacity = capacity
        self.base_price = base_price
        self.room_type_active = room_type_active

    @property
    def room_number(self) -> int:
        return self.__room_number

    @room_number.setter
    def room_number(self, value: int):
        if not isinstance(value, int):
            raise TypeError("room_number must be an int")
        if value <= 0:
            raise ValueError("room_number must be positive")
        self.__room_number = value

    @property
    def room_type_id(self) -> int:
        return self.__room_type_id

    @room_type_id.setter
    def room_type_id(self, value: int):
        if not isinstance(value, int):
            raise TypeError("room_type_id must be an int")
        if value <= 0:
            raise ValueError("room_type_id must be positive")
        self.__room_type_id = value

    @property
    def room_type_name(self) -> str:
        return self.__room_type_name

    @room_type_name.setter
    def room_type_name(self, value: str):
        if not isinstance(value, str):
            raise TypeError("room_type_name must be a str")
        v = value.strip()
        if not v:
            raise ValueError("room_type_name cannot be empty")
        self.__room_type_name = v

    @property
    def room_type_description(self) -> str:
        return self.__room_type_description

    @room_type_description.setter
    def room_type_description(self, value: str):
        if not isinstance(value, str):
            raise TypeError("room_type_description must be a str")
        v = value.strip()
        if not v:
            raise ValueError("room_type_description cannot be empty")
        self.__room_type_description = v

    @property
    def capacity(self) -> int:
        return self.__capacity

    @capacity.setter
    def capacity(self, value: int):
        if not isinstance(value, int):
            raise TypeError("capacity must be an int")
        if value <= 0:
            raise ValueError("capacity must be positive")
        self.__capacity = value

    @property
    def base_price(self) -> Decimal:
        return self.__base_price

    @base_price.setter
    def base_price(self, value):
        price = Decimal(value)
        if price <= 0:
            raise ValueError("base_price must be greater than zero")
        self.__base_price = price.quantize(Decimal("0.01"))

    @property
    def room_type_active(self) -> bool:
        return self.__room_type_active

    @room_type_active.setter
    def room_type_active(self, value: bool):
        if not isinstance(value, bool):
            raise TypeError("room_type_active must be a bool")
        self.__room_type_active = value
