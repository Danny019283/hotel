from src.domain.entities.bill import Bill
from src.domain.exeptions import BillDuplicateError, BillTotalError, BillTotalMismatchError
from src.domain.bussiness_rules.booking_rules import BookingRules
from src.domain.bussiness_rules.payment_method_rules import PaymentMethodRules


class BillRules:
    @staticmethod
    def validate_total(value: float) -> None:
        if value < 0:
            raise BillTotalError("total cannot be negative")

    @staticmethod
    def validate_total_matches_booking(bill: Bill) -> None:
        expected_total = BookingRules.calculate_booking_total(bill.booking)
        if float(bill.total) != float(expected_total):
            raise BillTotalMismatchError("bill total does not match booking total")

    @staticmethod
    def validate_bill(bill: Bill) -> None:
        BillRules.validate_total(bill.total)
        PaymentMethodRules.validate_payment_method(bill.payment_method)
        BillRules.validate_total_matches_booking(bill)

    @staticmethod
    def validate_not_duplicate(existing_bill: Bill | None) -> None:
        if existing_bill is not None:
            raise BillDuplicateError("a bill already exists for this booking")
