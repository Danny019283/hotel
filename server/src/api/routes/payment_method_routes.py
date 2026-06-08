from fastapi import APIRouter, Depends

from api.security import AuthenticatedUser, get_current_user
from application.dtos.payment_method_dto import PaymentMethodResponseDTO
from application.uses_cases.payment_method_cases import PaymentMethodCases


router = APIRouter(prefix="/payment-methods", tags=["Payment methods"])
payment_method_cases = PaymentMethodCases()


@router.get("", response_model=list[PaymentMethodResponseDTO])
def list_payment_methods(_: AuthenticatedUser = Depends(get_current_user)):
    return payment_method_cases.list_payment_methods_dto()
