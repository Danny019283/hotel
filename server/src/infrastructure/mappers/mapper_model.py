from sqlmodel import Session, select

from domain.bussiness_rules.booking_rules import BookingRules
from domain.exeptions import MappingError
from domain.entities.bill import Bill
from domain.entities.booking import Booking
from domain.entities.client import Client
from domain.entities.payment_method import Payment_Method
from domain.entities.room import Room
from domain.entities.user import User
from infrastructure.models.bill_model import Bill_model
from infrastructure.models.booking import Booking_model
from infrastructure.models.booking_room_model import Booking_Room_model
from infrastructure.models.client_model import Client_model
from infrastructure.models.payment_method_model import Payment_Method_Model
from infrastructure.models.room_model import Room_model
from infrastructure.models.user_model import User_model


class MapperModel:
    @staticmethod
    def client_model_to_entity(model: Client_model) -> Client:
        return Client(
            client_id=model.client_id,
            name=model.name,
            last_name=model.last_name,
            phone=model.phone,
            email=model.email,
        )

    @staticmethod
    def client_entity_to_model(entity: Client) -> Client_model:
        return Client_model(
            client_id=entity.client_id,
            name=entity.name,
            last_name=entity.last_name,
            phone=entity.phone,
            email=entity.email,
        )

    @staticmethod
    def room_model_to_entity(model: Room_model) -> Room:
        return Room(
            room_number=model.room_number,
            room_type=model.room_type,
            price=model.price,
            available=model.available,
        )

    @staticmethod
    def room_entity_to_model(entity: Room) -> Room_model:
        return Room_model(
            room_number=entity.room_number,
            room_type=entity.room_type,
            price=entity.price,
            available=entity.available,
        )

    @staticmethod
    def payment_method_model_to_entity(model: Payment_Method_Model) -> Payment_Method:
        return Payment_Method(
            payment_method_id=model.payment_method_id,
            name=model.name,
            active=model.active,
        )

    @staticmethod
    def payment_method_entity_to_model(entity: Payment_Method) -> Payment_Method_Model:
        return Payment_Method_Model(
            payment_method_id=entity.payment_method_id,
            name=entity.name,
            active=entity.active,
        )

    @staticmethod
    def _rooms_for_booking(session: Session, booking_id: int) -> list[Room]:
        booking_rooms = session.exec(
            select(Booking_Room_model).where(Booking_Room_model.booking_id == booking_id)
        ).all()
        if not booking_rooms:
            raise MappingError(f"Booking {booking_id} has no related room")

        rooms: list[Room] = []
        for booking_room in booking_rooms:
            room_model = session.get(Room_model, booking_room.room_number)
            if room_model is None:
                raise MappingError(f"Room {booking_room.room_number} not found for booking {booking_id}")
            rooms.append(MapperModel.room_model_to_entity(room_model))

        return rooms

    @staticmethod
    def booking_model_to_entity(session: Session, model: Booking_model) -> Booking:
        client_model = session.get(Client_model, model.client_id)
        if client_model is None:
            raise MappingError(f"Client {model.client_id} not found for booking {model.booking_id}")

        if model.booking_id is None:
            raise MappingError("booking_id cannot be None when mapping to entity")

        return Booking(
            booking_id=model.booking_id,
            client=MapperModel.client_model_to_entity(client_model),
            rooms=MapperModel._rooms_for_booking(session, model.booking_id),
            check_in=model.check_in,
            check_out=model.check_out,
        )

    @staticmethod
    def booking_entity_to_model(entity: Booking) -> Booking_model:
        return Booking_model(
            booking_id=entity.booking_id,
            check_in=entity.check_in,
            check_out=entity.check_out,
            client_id=entity.client.client_id,
        )

    @staticmethod
    def booking_entity_to_booking_room_models(entity: Booking) -> list[Booking_Room_model]:
        booking_rooms: list[Booking_Room_model] = []
        for room in entity.rooms:
            booking_rooms.append(
                Booking_Room_model(
                    booking_id=entity.booking_id,
                    room_number=room.room_number,
                    price_per_night=room.price,
                    subtotal=BookingRules.calculate_room_subtotal(room, entity.check_in, entity.check_out),
                )
            )

        return booking_rooms

    @staticmethod
    def bill_model_to_entity(session: Session, model: Bill_model) -> Bill:
        if model.bill_id is None:
            raise MappingError("bill_id cannot be None when mapping to entity")

        booking_model = session.get(Booking_model, model.booking_id)
        if booking_model is None:
            raise MappingError(f"Booking {model.booking_id} not found for bill {model.bill_id}")

        payment_method_model = session.get(Payment_Method_Model, model.payment_method_id)
        if payment_method_model is None:
            raise MappingError(
                f"Payment method {model.payment_method_id} not found for bill {model.bill_id}"
            )

        return Bill(
            bill_id=model.bill_id,
            booking=MapperModel.booking_model_to_entity(session, booking_model),
            payment_method=MapperModel.payment_method_model_to_entity(payment_method_model),
            total=model.total,
        )

    @staticmethod
    def bill_entity_to_model(entity: Bill) -> Bill_model:
        return Bill_model(
            bill_id=entity.bill_id,
            booking_id=entity.booking.booking_id,
            payment_method_id=entity.payment_method.payment_method_id,
            total=entity.total,
        )

    @staticmethod
    def user_model_to_entity(model: User_model) -> User:
        return User(
            username=model.username,
            password_hash=model.password_hash,
            role=model.role,
        )

    @staticmethod
    def user_entity_to_model(entity: User) -> User_model:
        return User_model(
            username=entity.username,
            password_hash=entity.password_hash,
            role=entity.role,
        )
