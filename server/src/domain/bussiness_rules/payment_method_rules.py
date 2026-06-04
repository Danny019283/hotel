from src.domain.entities.payment_method import Payment_Method
from src.domain.exeptions import PaymentMethodActiveError, PaymentMethodNameError


class PaymentMethodRules:
    @staticmethod
    def validate_name(value: str) -> None:
        if not value.strip():
            raise PaymentMethodNameError("payment method name cannot be empty")

    @staticmethod
    def validate_active(payment_method: Payment_Method) -> None:
        if not payment_method.active:
            raise PaymentMethodActiveError("payment method must be active")

    @staticmethod
    def validate_payment_method(payment_method: Payment_Method) -> None:
        PaymentMethodRules.validate_name(payment_method.name)
        PaymentMethodRules.validate_active(payment_method)
