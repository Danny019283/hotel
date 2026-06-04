class Room:
    def __init__(self, room_number: int, room_type: str, price: float, available: bool):
        self.room_number = room_number
        self.room_type = room_type
        self.price = price
        self.available = available

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
    def room_type(self) -> str:
        return self.__room_type

    @room_type.setter
    def room_type(self, value: str):
        if not isinstance(value, str):
            raise TypeError("room_type must be a str")
        v = value.strip()
        if not v:
            raise ValueError("room_type cannot be empty")
        self.__room_type = v

    @property
    def price(self) -> float:
        return self.__price

    @price.setter
    def price(self, value: float):
        if not isinstance(value, (int, float)):
            raise TypeError("price must be a number")
        if value < 0:
            raise ValueError("price cannot be negative")
        self.__price = float(value)

    @property
    def available(self) -> bool:
        return self.__available

    @available.setter
    def available(self, value: bool):
        if not isinstance(value, bool):
            raise TypeError("available must be a bool")
        self.__available = value
