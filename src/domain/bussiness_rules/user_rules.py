from src.domain.entities.user import User
from src.domain.exeptions import UserPasswordHashError, UserRoleError, UserUsernameError


class UserRules:
    ALLOWED_ROLES = {"ADMIN", "EMPLOYEE"}

    @staticmethod
    def validate_username(value: str) -> None:
        if not value.strip():
            raise UserUsernameError("username cannot be empty")
        if any(char.isspace() for char in value):
            raise UserUsernameError("username cannot contain spaces")

    @staticmethod
    def validate_password_hash(value: bytes) -> None:
        if not isinstance(value, (bytes, bytearray)):
            raise UserPasswordHashError("password_hash must be bytes")
        if len(value) < 20:
            raise UserPasswordHashError("password_hash is invalid")

    @staticmethod
    def validate_role(value: str) -> None:
        if value not in UserRules.ALLOWED_ROLES:
            raise UserRoleError("role must be ADMIN or EMPLOYEE")

    @staticmethod
    def validate_user(user: User) -> None:
        UserRules.validate_username(user.username)
        UserRules.validate_password_hash(user.password_hash)
        UserRules.validate_role(user.role)
