import base64
import hashlib
import hmac
import json
import os
import time
from dataclasses import dataclass

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from infrastructure.repositories.user_repo import User_repo


TOKEN_TTL_SECONDS = int(os.getenv("AUTH_TOKEN_TTL_SECONDS", "28800"))
TOKEN_SECRET = os.getenv("AUTH_SECRET", "hotel-manager-cr-development-secret").encode("utf-8")
bearer_scheme = HTTPBearer(auto_error=False)


@dataclass(frozen=True)
class AuthenticatedUser:
    username: str
    role: str


def _encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode("ascii").rstrip("=")


def _decode(value: str) -> bytes:
    padding = "=" * (-len(value) % 4)
    return base64.urlsafe_b64decode(value + padding)


def create_access_token(username: str, role: str) -> tuple[str, int]:
    expires_at = int(time.time()) + TOKEN_TTL_SECONDS
    payload = _encode(
        json.dumps(
            {"sub": username, "role": role, "exp": expires_at},
            separators=(",", ":"),
        ).encode("utf-8")
    )
    signature = _encode(hmac.new(TOKEN_SECRET, payload.encode("ascii"), hashlib.sha256).digest())
    return f"{payload}.{signature}", TOKEN_TTL_SECONDS


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> AuthenticatedUser:
    unauthorized = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid or expired authentication token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise unauthorized

    try:
        payload_part, signature_part = credentials.credentials.split(".", 1)
        expected = _encode(
            hmac.new(TOKEN_SECRET, payload_part.encode("ascii"), hashlib.sha256).digest()
        )
        if not hmac.compare_digest(signature_part, expected):
            raise unauthorized

        payload = json.loads(_decode(payload_part))
        if int(payload["exp"]) < int(time.time()):
            raise unauthorized

        user = User_repo().get_by_id(str(payload["sub"]))
        if user is None:
            raise unauthorized
        return AuthenticatedUser(username=user.username, role=user.role)
    except HTTPException:
        raise
    except (KeyError, TypeError, ValueError, json.JSONDecodeError):
        raise unauthorized


def require_admin(current_user: AuthenticatedUser = Depends(get_current_user)) -> AuthenticatedUser:
    if current_user.role != "ADMIN":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="administrator role required")
    return current_user
