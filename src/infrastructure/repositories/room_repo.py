from sqlmodel import Session, select

from infrastructure.database.connection import engine
from domain.entities.room import Room
from infrastructure.mappers.mapper_model import MapperModel
from infrastructure.models.room_model import Room_model
from infrastructure.repositories.irepository import IRespository


class Room_repo(IRespository[Room]):
    def add(self, model: Room) -> None:
        with Session(engine) as session:
            room_model = MapperModel.room_entity_to_model(model)
            session.add(room_model)
            session.commit()
            session.refresh(room_model)

    def update(self, updated_model: Room) -> None:
        with Session(engine) as session:
            room = session.get(Room_model, updated_model.room_number)
            if room:
                session.merge(MapperModel.room_entity_to_model(updated_model))
                session.commit()

    def get_by_id(self, id: int) -> Room | None:
        with Session(engine) as session:
            room = session.get(Room_model, id)
            return MapperModel.room_model_to_entity(room) if room else None

    def get_all(self) -> list[Room] | None:
        with Session(engine) as session:
            statement = select(Room_model)
            rooms = session.exec(statement).all()
            return [MapperModel.room_model_to_entity(room) for room in rooms]

    def delete(self, id: int) -> None:
        with Session(engine) as session:
            room = session.get(Room_model, id)
            if room:
                session.delete(room)
                session.commit()
