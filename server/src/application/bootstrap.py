import os

from application.uses_cases.user_cases import UserCases
from domain.entities.payment_method import Payment_Method
from infrastructure.repositories.payment_method_repo import Payment_Method_repo


def seed_initial_data() -> None:
    user_cases = UserCases()
    username = os.getenv("INITIAL_ADMIN_USERNAME", "admin").strip()
    password = os.getenv("INITIAL_ADMIN_PASSWORD", "admin123")

    if username and user_cases.user_repo.get_by_id(username) is None:
        user_cases.register_user(username, password, "ADMIN")

    payment_method_repo = Payment_Method_repo()
    methods = [(1, "Efectivo"), (2, "Tarjeta"), (3, "Transferencia")]
    for method_id, name in methods:
        if payment_method_repo.get_by_id(method_id) is None:
            payment_method_repo.add(Payment_Method(method_id, name, True))
