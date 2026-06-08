from typing import Literal

from pydantic import BaseModel, Field


class RegisterUserDTO(BaseModel):
    username: str = Field(min_length=3, max_length=50, description="Unique username", examples=["admin01"])
    password: str = Field(min_length=8, max_length=128, description="Raw password", examples=["StrongPass123"])
    role: Literal["ADMIN", "EMPLOYEE"] = Field(description="User role")


class LoginDTO(BaseModel):
    username: str = Field(min_length=3, max_length=50, description="Unique username", examples=["admin01"])
    password: str = Field(min_length=8, max_length=128, description="Raw password", examples=["StrongPass123"])


class ChangePasswordDTO(BaseModel):
    username: str = Field(min_length=3, max_length=50, description="Unique username", examples=["admin01"])
    current_password: str = Field(min_length=8, max_length=128, description="Current password", examples=["StrongPass123"])
    new_password: str = Field(min_length=8, max_length=128, description="New password", examples=["NewStrongPass456"])


class UserResponseDTO(BaseModel):
    username: str = Field(description="Unique username", examples=["admin01"])
    role: Literal["ADMIN", "EMPLOYEE"] = Field(description="User role")


class AuthResponseDTO(BaseModel):
    username: str = Field(description="Unique username", examples=["admin01"])
    role: Literal["ADMIN", "EMPLOYEE"] = Field(description="User role")
    message: str = Field(description="Authentication result message", examples=["login successful"])
    access_token: str = Field(description="Bearer access token")
    token_type: Literal["bearer"] = Field(default="bearer")
    expires_in: int = Field(gt=0, description="Token lifetime in seconds")


class UpdateUserRoleDTO(BaseModel):
    role: Literal["ADMIN", "EMPLOYEE"] = Field(description="Updated user role")
