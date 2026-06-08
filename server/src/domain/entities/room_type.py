from decimal import Decimal


class RoomType:
    def __init__(
        self,
        room_type_id: int | None,
        name: str,
        description: str,
        capacity: int,
        base_price: Decimal,
        active: bool,
    ):
        self.room_type_id = room_type_id
        self.name = name
        self.description = description
        self.capacity = capacity
        self.base_price = base_price
        self.active = active

    @property
    def room_type_id(self) -> int | None:
        return self.__room_type_id

    @room_type_id.setter
    def room_type_id(self, value: int | None):
        if value is None:
            self.__room_type_id = value
            return
        if not isinstance(value, int):
            raise TypeError("room_type_id must be an int")
        if value <= 0:
            raise ValueError("room_type_id must be positive")
        self.__room_type_id = value

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str):
        if not isinstance(value, str):
            raise TypeError("name must be a str")
        value = value.strip()
        if not value:
            raise ValueError("name cannot be empty")
        self.__name = value

    @property
    def description(self) -> str:
        return self.__description

    @description.setter
    def description(self, value: str):
        if not isinstance(value, str):
            raise TypeError("description must be a str")
        value = value.strip()
        if not value:
            raise ValueError("description cannot be empty")
        self.__description = value

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
    def active(self) -> bool:
        return self.__active

    @active.setter
    def active(self, value: bool):
        if not isinstance(value, bool):
            raise TypeError("active must be a bool")
        self.__active = value
