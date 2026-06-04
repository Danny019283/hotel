from fastapi import APIRouter, HTTPException, status

from application.dtos.user_dto import AuthResponseDTO, ChangePasswordDTO, LoginDTO, RegisterUserDTO, UserResponseDTO
from application.uses_cases.user_cases import UserCases
from domain.exeptions import DomainError


router = APIRouter(prefix="/auth", tags=["Auth"])
user_cases = UserCases()


@router.post("/register", response_model=UserResponseDTO, status_code=status.HTTP_201_CREATED)
def register_user(dto: RegisterUserDTO):
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
def change_password(dto: ChangePasswordDTO):
    try:
        return user_cases.change_password_dto(dto)
    except DomainError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
