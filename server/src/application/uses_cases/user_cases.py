from bcrypt import checkpw, gensalt, hashpw

from application.dtos.user_dto import AuthResponseDTO, ChangePasswordDTO, LoginDTO, RegisterUserDTO, UpdateUserRoleDTO, UserResponseDTO
from api.security import create_access_token
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
        access_token, expires_in = create_access_token(user.username, user.role)
        return AuthResponseDTO(
            username=user.username,
            role=user.role,
            message="login successful",
            access_token=access_token,
            expires_in=expires_in,
        )

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

    def list_users_dto(self) -> list[UserResponseDTO]:
        return [
            UserResponseDTO(username=user.username, role=user.role)
            for user in (self.user_repo.get_all() or [])
        ]

    def update_role_dto(self, username: str, dto: UpdateUserRoleDTO) -> UserResponseDTO:
        user = self.user_repo.get_by_id(username)
        if user is None:
            raise DomainError("user not found")

        if user.role == "ADMIN" and dto.role != "ADMIN":
            admins = [item for item in (self.user_repo.get_all() or []) if item.role == "ADMIN"]
            if len(admins) <= 1:
                raise DomainError("cannot change the role of the last administrator")

        updated_user = User(username=user.username, password_hash=user.password_hash, role=dto.role)
        UserRules.validate_user(updated_user)
        self.user_repo.update(updated_user)
        return UserResponseDTO(username=updated_user.username, role=updated_user.role)

    def delete_user(self, username: str) -> None:
        user = self.user_repo.get_by_id(username)
        if user is None:
            raise DomainError("user not found")
        if user.role == "ADMIN":
            admins = [item for item in (self.user_repo.get_all() or []) if item.role == "ADMIN"]
            if len(admins) <= 1:
                raise DomainError("cannot delete the last administrator")
        self.user_repo.delete(username)
