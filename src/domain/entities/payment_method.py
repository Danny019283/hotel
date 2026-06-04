class Payment_Method:
    def __init__(self, payment_method_id: int, name: str, active: bool):
        self.payment_method_id = payment_method_id
        self.name = name
        self.active = active

    @property
    def payment_method_id(self) -> int:
        return self.__payment_method_id

    @payment_method_id.setter
    def payment_method_id(self, value: int):
        if not isinstance(value, int):
            raise TypeError("payment_method_id must be an int")
        if value <= 0:
            raise ValueError("payment_method_id must be positive")
        self.__payment_method_id = value

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str):
        if not isinstance(value, str):
            raise TypeError("name must be a str")
        v = value.strip()
        if not v:
            raise ValueError("name cannot be empty")
        self.__name = v

    @property
    def active(self) -> bool:
        return self.__active

    @active.setter
    def active(self, value: bool):
        if not isinstance(value, bool):
            raise TypeError("active must be a bool")
        self.__active = value
