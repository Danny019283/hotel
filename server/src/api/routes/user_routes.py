from fastapi import APIRouter, Depends, HTTPException, status

from api.security import AuthenticatedUser, get_current_user, require_admin
from application.dtos.user_dto import AuthResponseDTO, ChangePasswordDTO, LoginDTO, RegisterUserDTO, UpdateUserRoleDTO, UserResponseDTO
from application.uses_cases.user_cases import UserCases
from domain.exeptions import DomainError


router = APIRouter(prefix="/auth", tags=["Auth"])
user_cases = UserCases()


@router.post("/register", response_model=UserResponseDTO, status_code=status.HTTP_201_CREATED)
def register_user(dto: RegisterUserDTO, _: AuthenticatedUser = Depends(require_admin)):
    try:
        return user_cases.register_user_dto(dto)
    except DomainError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/login", response_model=AuthResponseDTO)
def login(dto: LoginDTO):
    try:
        return user_cases.login_dto(dto)
    except DomainError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)) from exc


@router.put("/password", response_model=UserResponseDTO)
def change_password(dto: ChangePasswordDTO, current_user: AuthenticatedUser = Depends(get_current_user)):
    if current_user.role != "ADMIN" and current_user.username != dto.username:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="cannot change another user's password")
    try:
        return user_cases.change_password_dto(dto)
    except DomainError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get("/users", response_model=list[UserResponseDTO])
def list_users(_: AuthenticatedUser = Depends(require_admin)):
    return user_cases.list_users_dto()


@router.patch("/users/{username}/role", response_model=UserResponseDTO)
def update_user_role(
    username: str,
    dto: UpdateUserRoleDTO,
    _: AuthenticatedUser = Depends(require_admin),
):
    try:
        return user_cases.update_role_dto(username, dto)
    except DomainError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.delete("/users/{username}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    username: str,
    current_user: AuthenticatedUser = Depends(require_admin),
):
    if current_user.username == username:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="cannot delete the current user")
    try:
        user_cases.delete_user(username)
    except DomainError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
