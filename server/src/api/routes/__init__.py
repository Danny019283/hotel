from fastapi import APIRouter

from .bill_routes import router as bill_router
from .booking_routes import router as booking_router
from .client_routes import router as client_router
from .room_routes import router as room_router
from .user_routes import router as user_router
from .payment_method_routes import router as payment_method_router


api_router = APIRouter(prefix="/api/v1")
api_router.include_router(client_router)
api_router.include_router(room_router)
api_router.include_router(booking_router)
api_router.include_router(bill_router)
api_router.include_router(user_router)
api_router.include_router(payment_method_router)
