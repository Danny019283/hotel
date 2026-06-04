from fastapi import APIRouter, HTTPException, status

from application.dtos.bill_dto import BillResponseDTO, BillSummaryDTO, CreateBillDTO
from application.uses_cases.bill_cases import BillCases
from domain.exeptions import DomainError


router = APIRouter(prefix="/bills", tags=["Bills"])
bill_cases = BillCases()


@router.post("", response_model=BillResponseDTO, status_code=status.HTTP_201_CREATED)
def create_bill(dto: CreateBillDTO):
    try:
        return bill_cases.create_bill_dto(dto)
    except DomainError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get("/{bill_id}", response_model=BillResponseDTO)
def consult_bill(bill_id: int):
    bill = bill_cases.consult_bill_dto(bill_id)
    if bill is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="bill not found")
    return bill


@router.get("/booking/{booking_id}", response_model=BillResponseDTO)
def consult_bill_by_booking(booking_id: int):
    bill = bill_cases.consult_bill_by_booking_dto(booking_id)
    if bill is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="bill not found")
    return bill


@router.get("/{bill_id}/summary", response_model=BillSummaryDTO)
def bill_summary(bill_id: int):
    bill = bill_cases.bill_summary_dto(bill_id)
    if bill is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="bill not found")
    return bill
