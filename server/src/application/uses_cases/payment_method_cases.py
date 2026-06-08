from application.dtos.payment_method_dto import PaymentMethodResponseDTO
from infrastructure.repositories.payment_method_repo import Payment_Method_repo


class PaymentMethodCases:
    def __init__(self, payment_method_repo: Payment_Method_repo | None = None):
        self.payment_method_repo = payment_method_repo or Payment_Method_repo()

    def list_payment_methods_dto(self) -> list[PaymentMethodResponseDTO]:
        return [
            PaymentMethodResponseDTO(
                payment_method_id=method.payment_method_id,
                name=method.name,
                active=method.active,
            )
            for method in (self.payment_method_repo.get_all() or [])
        ]
