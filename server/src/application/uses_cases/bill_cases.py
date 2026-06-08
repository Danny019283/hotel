from domain.bussiness_rules.booking_rules import BookingRules
from domain.bussiness_rules.bill_rules import BillRules
from domain.entities.bill import Bill
from domain.exeptions import DomainError
from application.dtos.bill_dto import BillResponseDTO, BillSummaryDTO, CreateBillDTO, UpdateBillPaymentMethodDTO
from domain.bussiness_rules.payment_method_rules import PaymentMethodRules
from infrastructure.repositories.bill_repo import Bill_repo
from infrastructure.repositories.booking_repo import Booking_repo
from infrastructure.repositories.payment_method_repo import Payment_Method_repo


class BillCases:
    def __init__(
        self,
        bill_repo: Bill_repo | None = None,
        booking_repo: Booking_repo | None = None,
        payment_method_repo: Payment_Method_repo | None = None,
    ):
        self.bill_repo = bill_repo or Bill_repo()
        self.booking_repo = booking_repo or Booking_repo()
        self.payment_method_repo = payment_method_repo or Payment_Method_repo()

    def register_payment(self, booking_id: int, payment_method_id: int) -> Bill:
        booking = self.booking_repo.get_by_id(booking_id)
        if booking is None:
            raise DomainError("booking not found")

        payment_method = self.payment_method_repo.get_by_id(payment_method_id)
        if payment_method is None:
            raise DomainError("payment method not found")

        existing_bill = self.bill_repo.get_by_booking_id(booking_id)
        BillRules.validate_not_duplicate(existing_bill)

        bill = Bill(
            bill_id=None,
            booking=booking,
            payment_method=payment_method,
            total=BookingRules.calculate_booking_total(booking),
        )
        BillRules.validate_bill(bill)
        self.bill_repo.add(bill)
        return bill

    def register_payment_dto(self, dto: CreateBillDTO) -> BillResponseDTO:
        bill = self.register_payment(dto.booking_id, dto.payment_method_id)
        return BillResponseDTO(
            bill_id=bill.bill_id,
            booking_id=bill.booking.booking_id,
            payment_method_id=bill.payment_method.payment_method_id,
            total=float(bill.total),
        )

    def create_bill(self, booking_id: int, payment_method_id: int) -> Bill:
        return self.register_payment(booking_id, payment_method_id)

    def create_bill_dto(self, dto: CreateBillDTO) -> BillResponseDTO:
        return self.register_payment_dto(dto)

    def consult_bill(self, bill_id: int) -> Bill | None:
        return self.bill_repo.get_by_id(bill_id)

    def consult_bill_dto(self, bill_id: int) -> BillResponseDTO | None:
        bill = self.consult_bill(bill_id)
        if bill is None:
            return None
        return BillResponseDTO(
            bill_id=bill.bill_id,
            booking_id=bill.booking.booking_id,
            payment_method_id=bill.payment_method.payment_method_id,
            total=float(bill.total),
        )

    def consult_bill_by_booking(self, booking_id: int) -> Bill | None:
        return self.bill_repo.get_by_booking_id(booking_id)

    def consult_bill_by_booking_dto(self, booking_id: int) -> BillResponseDTO | None:
        bill = self.consult_bill_by_booking(booking_id)
        if bill is None:
            return None
        return BillResponseDTO(
            bill_id=bill.bill_id,
            booking_id=bill.booking.booking_id,
            payment_method_id=bill.payment_method.payment_method_id,
            total=float(bill.total),
        )

    def bill_summary_dto(self, bill_id: int) -> BillSummaryDTO | None:
        bill = self.consult_bill(bill_id)
        if bill is None:
            return None
        return BillSummaryDTO(
            bill_id=bill.bill_id,
            booking_id=bill.booking.booking_id,
            client_id=bill.booking.client.client_id,
            room_numbers=[room.room_number for room in bill.booking.rooms],
            room_types=[room.room_type_name for room in bill.booking.rooms],
            payment_method_id=bill.payment_method.payment_method_id,
            total=float(bill.total),
        )

    def list_bills_dto(self) -> list[BillResponseDTO]:
        return [
            BillResponseDTO(
                bill_id=bill.bill_id,
                booking_id=bill.booking.booking_id,
                payment_method_id=bill.payment_method.payment_method_id,
                total=float(bill.total),
            )
            for bill in (self.bill_repo.get_all() or [])
        ]

    def update_payment_method_dto(
        self,
        bill_id: int,
        dto: UpdateBillPaymentMethodDTO,
    ) -> BillResponseDTO:
        bill = self.bill_repo.get_by_id(bill_id)
        if bill is None:
            raise DomainError("bill not found")

        payment_method = self.payment_method_repo.get_by_id(dto.payment_method_id)
        if payment_method is None:
            raise DomainError("payment method not found")
        PaymentMethodRules.validate_payment_method(payment_method)

        updated_bill = Bill(
            bill_id=bill.bill_id,
            booking=bill.booking,
            payment_method=payment_method,
            total=bill.total,
        )
        self.bill_repo.update(updated_bill)
        return BillResponseDTO(
            bill_id=updated_bill.bill_id,
            booking_id=updated_bill.booking.booking_id,
            payment_method_id=updated_bill.payment_method.payment_method_id,
            total=float(updated_bill.total),
        )

    def delete_bill(self, bill_id: int) -> None:
        if self.bill_repo.get_by_id(bill_id) is None:
            raise DomainError("bill not found")
        self.bill_repo.delete(bill_id)
