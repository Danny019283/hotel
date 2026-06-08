import os

from application.uses_cases.user_cases import UserCases
from domain.entities.payment_method import Payment_Method
from domain.entities.room_type import RoomType
from infrastructure.repositories.payment_method_repo import Payment_Method_repo
from infrastructure.repositories.room_type_repo import RoomType_repo


def seed_initial_data() -> None:
    user_cases = UserCases()
    username = os.getenv("INITIAL_ADMIN_USERNAME", "admin").strip()
    password = os.getenv("INITIAL_ADMIN_PASSWORD", "admin123")

    if username and user_cases.user_repo.get_by_username(username) is None:
        user_cases.register_user(username, password, "ADMIN")

    payment_method_repo = Payment_Method_repo()
    methods = [(1, "Efectivo"), (2, "Tarjeta"), (3, "Transferencia")]
    for method_id, name in methods:
        if payment_method_repo.get_by_id(method_id) is None:
            payment_method_repo.add(Payment_Method(method_id, name, True))

    room_type_repo = RoomType_repo()
    room_types = [
        ("Suite", "Habitacion premium con amenidades ampliadas.", 4, "225.00"),
        ("Doble", "Habitacion comoda para dos huespedes.", 2, "140.00"),
        ("Individual", "Habitacion practica para una persona.", 1, "95.00"),
    ]
    for name, description, capacity, base_price in room_types:
        if room_type_repo.get_by_name(name) is None:
            room_type_repo.add(RoomType(None, name, description, capacity, base_price, True))
