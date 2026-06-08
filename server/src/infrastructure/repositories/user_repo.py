from sqlmodel import Session, select

from infrastructure.database.connection import engine
from domain.entities.user import User
from infrastructure.mappers.mapper_model import MapperModel
from infrastructure.models.user_model import User_model
from infrastructure.repositories.irepository import IRespository


class User_repo(IRespository[User]):
    def add(self, model: User) -> None:
        with Session(engine) as session:
            user_model = MapperModel.user_entity_to_model(model)
            session.add(user_model)
            session.flush()
            if model.user_id != user_model.user_id:
                model.user_id = user_model.user_id
            session.commit()
            session.refresh(user_model)

    def update(self, updated_model: User) -> None:
        with Session(engine) as session:
            user = session.get(User_model, updated_model.user_id)
            if user:
                session.merge(MapperModel.user_entity_to_model(updated_model))
                session.commit()

    def get_by_id(self, id: int) -> User | None:
        with Session(engine) as session:
            user = session.get(User_model, id)
            return MapperModel.user_model_to_entity(user) if user else None

    def get_by_username(self, username: str) -> User | None:
        with Session(engine) as session:
            statement = select(User_model).where(User_model.username == username)
            user = session.exec(statement).first()
            return MapperModel.user_model_to_entity(user) if user else None

    def get_all(self) -> list[User] | None:
        with Session(engine) as session:
            statement = select(User_model)
            users = session.exec(statement).all()
            return [MapperModel.user_model_to_entity(user) for user in users]

    def delete(self, id: int) -> None:
        with Session(engine) as session:
            user = session.get(User_model, id)
            if user:
                session.delete(user)
                session.commit()
