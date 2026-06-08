from sqlmodel import Session, select

from domain.entities.room_type import RoomType
from infrastructure.database.connection import engine
from infrastructure.mappers.mapper_model import MapperModel
from infrastructure.models.room_type_model import Room_Type_model
from infrastructure.repositories.irepository import IRespository


class RoomType_repo(IRespository[RoomType]):
    def add(self, model: RoomType) -> None:
        with Session(engine) as session:
            room_type_model = MapperModel.room_type_entity_to_model(model)
            session.add(room_type_model)
            session.flush()
            if model.room_type_id != room_type_model.room_type_id:
                model.room_type_id = room_type_model.room_type_id
            session.commit()
            session.refresh(room_type_model)

    def update(self, updated_model: RoomType) -> None:
        with Session(engine) as session:
            room_type = session.get(Room_Type_model, updated_model.room_type_id)
            if room_type:
                session.merge(MapperModel.room_type_entity_to_model(updated_model))
                session.commit()

    def get_by_id(self, id: int) -> RoomType | None:
        with Session(engine) as session:
            room_type = session.get(Room_Type_model, id)
            return MapperModel.room_type_model_to_entity(room_type) if room_type else None

    def get_by_name(self, name: str) -> RoomType | None:
        with Session(engine) as session:
            statement = select(Room_Type_model).where(Room_Type_model.name == name)
            room_type = session.exec(statement).first()
            return MapperModel.room_type_model_to_entity(room_type) if room_type else None

    def get_all(self) -> list[RoomType] | None:
        with Session(engine) as session:
            statement = select(Room_Type_model)
            room_types = session.exec(statement).all()
            return [MapperModel.room_type_model_to_entity(room_type) for room_type in room_types]

    def delete(self, id: int) -> None:
        with Session(engine) as session:
            room_type = session.get(Room_Type_model, id)
            if room_type:
                session.delete(room_type)
                session.commit()
