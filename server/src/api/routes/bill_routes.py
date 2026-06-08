from fastapi import APIRouter, Depends, HTTPException, status

from api.security import AuthenticatedUser, get_current_user, require_admin
from application.dtos.bill_dto import BillResponseDTO, BillSummaryDTO, CreateBillDTO, UpdateBillPaymentMethodDTO
from application.uses_cases.bill_cases import BillCases
from domain.exeptions import DomainError


router = APIRouter(prefix="/bills", tags=["Bills"])
bill_cases = BillCases()


@router.post("", response_model=BillResponseDTO, status_code=status.HTTP_201_CREATED)
def create_bill(dto: CreateBillDTO, _: AuthenticatedUser = Depends(get_current_user)):
    try:
        return bill_cases.create_bill_dto(dto)
    except DomainError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get("/booking/{booking_id}", response_model=BillResponseDTO)
def consult_bill_by_booking(booking_id: int, _: AuthenticatedUser = Depends(get_current_user)):
    bill = bill_cases.consult_bill_by_booking_dto(booking_id)
    if bill is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="bill not found")
    return bill


@router.get("", response_model=list[BillResponseDTO])
def list_bills(_: AuthenticatedUser = Depends(get_current_user)):
    return bill_cases.list_bills_dto()


@router.get("/{bill_id}/summary", response_model=BillSummaryDTO)
def bill_summary(bill_id: int, _: AuthenticatedUser = Depends(get_current_user)):
    bill = bill_cases.bill_summary_dto(bill_id)
    if bill is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="bill not found")
    return bill


@router.get("/{bill_id}", response_model=BillResponseDTO)
def consult_bill(bill_id: int, _: AuthenticatedUser = Depends(get_current_user)):
    bill = bill_cases.consult_bill_dto(bill_id)
    if bill is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="bill not found")
    return bill


@router.patch("/{bill_id}/payment-method", response_model=BillResponseDTO)
def update_bill_payment_method(
    bill_id: int,
    dto: UpdateBillPaymentMethodDTO,
    _: AuthenticatedUser = Depends(require_admin),
):
    try:
        return bill_cases.update_payment_method_dto(bill_id, dto)
    except DomainError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.delete("/{bill_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_bill(bill_id: int, _: AuthenticatedUser = Depends(require_admin)):
    try:
        bill_cases.delete_bill(bill_id)
    except DomainError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
