from bcrypt import checkpw, gensalt, hashpw

from application.dtos.user_dto import AuthResponseDTO, ChangePasswordDTO, LoginDTO, RegisterUserDTO, UserResponseDTO
from domain.bussiness_rules.user_rules import UserRules
from domain.entities.user import User
from domain.exeptions import DomainError
from infrastructure.repositories.user_repo import User_repo


class UserCases:
    def __init__(self, user_repo: User_repo | None = None):
        self.user_repo = user_repo or User_repo()

    def register_user(self, username: str, password: str, role: str) -> User:
        if self.user_repo.get_by_id(username) is not None:
            raise DomainError("user already exists")

        user = User(username=username, password_hash=hashpw(password.encode("utf-8"), gensalt()), role=role)
        UserRules.validate_user(user)
        self.user_repo.add(user)
        return user

    def register_user_dto(self, dto: RegisterUserDTO) -> UserResponseDTO:
        user = self.register_user(dto.username, dto.password, dto.role)
        return UserResponseDTO(username=user.username, role=user.role)

    def login(self, username: str, password: str) -> User:
        user = self.user_repo.get_by_id(username)
        if user is None:
            raise DomainError("invalid credentials")

        if not checkpw(password.encode("utf-8"), user.password_hash):
            raise DomainError("invalid credentials")

        return user

    def login_dto(self, dto: LoginDTO) -> AuthResponseDTO:
        user = self.login(dto.username, dto.password)
        return AuthResponseDTO(username=user.username, role=user.role, message="login successful")

    def change_password(self, username: str, current_password: str, new_password: str) -> User:
        user = self.user_repo.get_by_id(username)
        if user is None:
            raise DomainError("user not found")

        if not checkpw(current_password.encode("utf-8"), user.password_hash):
            raise DomainError("invalid credentials")

        updated_user = User(
            username=user.username,
            password_hash=hashpw(new_password.encode("utf-8"), gensalt()),
            role=user.role,
        )
        UserRules.validate_user(updated_user)
        self.user_repo.update(updated_user)
        return updated_user

    def change_password_dto(self, dto: ChangePasswordDTO) -> UserResponseDTO:
        user = self.change_password(dto.username, dto.current_password, dto.new_password)
        return UserResponseDTO(username=user.username, role=user.role)
