from sqlmodel import Session, select

from infrastructure.database.connection import engine
from domain.entities.booking import Booking
from infrastructure.mappers.mapper_model import MapperModel
from infrastructure.models.booking import Booking_model
from infrastructure.models.booking_room_model import Booking_Room_model
from infrastructure.models.room_model import Room_model
from infrastructure.repositories.irepository import IRespository


class Booking_repo(IRespository[Booking]):
    def _set_rooms_availability(self, session: Session, room_numbers: list[int], available: bool) -> None:
        for room_number in room_numbers:
            room = session.get(Room_model, room_number)
            if room is not None:
                room.available = available

    def exists_overlap(
        self,
        room_number: int,
        check_in,
        check_out,
        exclude_booking_id: int | None = None,
    ) -> bool:
        with Session(engine) as session:
            booking_rooms = session.exec(
                select(Booking_Room_model).where(Booking_Room_model.room_number == room_number)
            ).all()

            for booking_room in booking_rooms:
                if exclude_booking_id is not None and booking_room.booking_id == exclude_booking_id:
                    continue

                booking = session.get(Booking_model, booking_room.booking_id)
                if booking is None:
                    continue

                has_overlap = check_in < booking.check_out and check_out > booking.check_in
                if has_overlap:
                    return True

            return False

    def add(self, model: Booking) -> None:
        with Session(engine) as session:
            try:
                booking_model = MapperModel.booking_entity_to_model(model)
                session.add(booking_model)
                session.flush()

                if model.booking_id != booking_model.booking_id:
                    model.booking_id = booking_model.booking_id

                booking_room_models = MapperModel.booking_entity_to_booking_room_models(model)
                for booking_room_model in booking_room_models:
                    session.add(booking_room_model)
                self._set_rooms_availability(
                    session,
                    [room.room_number for room in model.rooms],
                    available=False,
                )
                session.commit()
                session.refresh(booking_model)
            except Exception:
                session.rollback()
                raise

    def update(self, updated_model: Booking) -> None:
        with Session(engine) as session:
            try:
                booking = session.get(Booking_model, updated_model.booking_id)
                if booking:
                    session.merge(MapperModel.booking_entity_to_model(updated_model))
                    existing_booking_rooms = session.exec(
                        select(Booking_Room_model).where(Booking_Room_model.booking_id == updated_model.booking_id)
                    ).all()
                    previous_room_numbers = [booking_room.room_number for booking_room in existing_booking_rooms]
                    for existing_booking_room in existing_booking_rooms:
                        session.delete(existing_booking_room)
                    booking_room_models = MapperModel.booking_entity_to_booking_room_models(updated_model)
                    for booking_room_model in booking_room_models:
                        session.add(booking_room_model)
                    self._set_rooms_availability(session, previous_room_numbers, available=True)
                    self._set_rooms_availability(
                        session,
                        [room.room_number for room in updated_model.rooms],
                        available=False,
                    )
                    session.commit()
            except Exception:
                session.rollback()
                raise

    def get_by_id(self, id: int) -> Booking | None:
        with Session(engine) as session:
            booking = session.get(Booking_model, id)
            return MapperModel.booking_model_to_entity(session, booking) if booking else None

    def get_all(self) -> list[Booking] | None:
        with Session(engine) as session:
            statement = select(Booking_model)
            bookings = session.exec(statement).all()
            result: list[Booking] = []
            for booking in bookings:
                result.append(MapperModel.booking_model_to_entity(session, booking))
            return result

    def delete(self, id: int) -> None:
        with Session(engine) as session:
            booking = session.get(Booking_model, id)
            if booking:
                booking_rooms = session.exec(
                    select(Booking_Room_model).where(Booking_Room_model.booking_id == id)
                ).all()
                self._set_rooms_availability(
                    session,
                    [booking_room.room_number for booking_room in booking_rooms],
                    available=True,
                )
                for booking_room in booking_rooms:
                    session.delete(booking_room)
                session.flush()
                session.delete(booking)
                session.commit()
