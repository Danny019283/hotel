import os
import sys
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

SRC_PATH = Path(__file__).resolve().parent / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from api.routes import api_router
from application.bootstrap import seed_initial_data
from domain.exeptions import DomainError, MappingError, ValidationError
from infrastructure.database.connection import create_db_and_tables


def _get_allowed_origins() -> list[str]:
    origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:5173")
    return [origin.strip() for origin in origins.split(",") if origin.strip()]

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    seed_initial_data()
    yield


def _error_response(status_code: int, code: str, message: str, details=None) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={
            "code": code,
            "message": message,
            "details": details or [],
        },
    )

app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=_get_allowed_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_router)


@app.exception_handler(ValidationError)
async def validation_error_handler(request: Request, exc: ValidationError):
    return _error_response(status.HTTP_400_BAD_REQUEST, "validation_error", str(exc))


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return _error_response(exc.status_code, "http_error", str(exc.detail))


@app.exception_handler(MappingError)
async def mapping_error_handler(request: Request, exc: MappingError):
    return _error_response(status.HTTP_500_INTERNAL_SERVER_ERROR, "mapping_error", str(exc))


@app.exception_handler(DomainError)
async def domain_error_handler(request: Request, exc: DomainError):
    return _error_response(status.HTTP_400_BAD_REQUEST, "domain_error", str(exc))


@app.exception_handler(IntegrityError)
async def integrity_error_handler(request: Request, exc: IntegrityError):
    return _error_response(status.HTTP_409_CONFLICT, "integrity_error", "database integrity error")


@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    return _error_response(status.HTTP_400_BAD_REQUEST, "value_error", str(exc))


@app.exception_handler(TypeError)
async def type_error_handler(request: Request, exc: TypeError):
    return _error_response(status.HTTP_400_BAD_REQUEST, "type_error", str(exc))


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    return _error_response(status.HTTP_500_INTERNAL_SERVER_ERROR, "internal_error", "unexpected server error")
