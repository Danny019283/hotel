import re

from src.domain.entities.client import Client
from src.domain.exeptions import ClientEmailError, ClientLastNameError, ClientNameError, ClientPhoneError


class ClientRules:
    _email_pattern = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")

    @staticmethod
    def validate_name(value: str) -> None:
        if any(char.isdigit() for char in value):
            raise ClientNameError("name cannot contain numbers")

    @staticmethod
    def validate_last_name(value: str) -> None:
        if any(char.isdigit() for char in value):
            raise ClientLastNameError("last_name cannot contain numbers")

    @staticmethod
    def validate_email(value: str) -> None:
        if not ClientRules._email_pattern.match(value.strip()):
            raise ClientEmailError("email is not valid")

    @staticmethod
    def validate_phone(value: int) -> None:
        if not isinstance(value, int):
            raise ClientPhoneError("phone must be an integer")
        if value < 10000000 or value > 99999999:
            raise ClientPhoneError("phone must have exactly 8 digits")

    @staticmethod
    def validate_client(client: Client) -> None:
        ClientRules.validate_name(client.name)
        ClientRules.validate_last_name(client.last_name)
        ClientRules.validate_email(client.email)
        ClientRules.validate_phone(client.phone)
