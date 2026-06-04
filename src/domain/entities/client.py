class Client:
    def __init__(self, client_id: str, name: str, last_name: str, phone: int, email: str):
        self.client_id = client_id
        self.name = name
        self.last_name = last_name
        self.phone = phone
        self.email = email

    @property
    def client_id(self) -> str:
        return self.__client_id

    @client_id.setter
    def client_id(self, value: str):
        if not isinstance(value, str):
            raise TypeError("client_id must be a str")
        v = value.strip()
        if not v:
            raise ValueError("client_id cannot be empty")
        self.__client_id = v

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str):
        if not isinstance(value, str):
            raise TypeError("name must be a str")
        if not value.strip():
            raise ValueError("name cannot be empty")
        self.__name = value.strip()

    @property
    def last_name(self) -> str:
        return self.__last_name

    @last_name.setter
    def last_name(self, value: str):
        if not isinstance(value, str):
            raise TypeError("last_name must be a str")
        if not value.strip():
            raise ValueError("last_name cannot be empty")
        self.__last_name = value.strip()

    @property
    def phone(self) -> int:
        return self.__phone

    @phone.setter
    def phone(self, value: int):
        if not isinstance(value, int):
            raise TypeError("phone must be an int")
        if value <= 0:
            raise ValueError("phone must be positive")
        self.__phone = value

    @property
    def email(self) -> str:
        return self.__email

    @email.setter
    def email(self, value: str):
        if not isinstance(value, str):
            raise TypeError("email must be a str")
        v = value.strip()
        if not v:
            raise ValueError("email cannot be empty")
        # minimal email validation
        if "@" not in v or "." not in v.split("@")[-1]:
            raise ValueError("email is not valid")
        self.__email = v

    
