from sqlmodel import Session, select

from infrastructure.database.connection import engine
from domain.entities.client import Client
from infrastructure.mappers.mapper_model import MapperModel
from infrastructure.models.client_model import Client_model
from infrastructure.repositories.irepository import IRespository

class Client_repo(IRespository[Client]):
    def add(self, model: Client) -> None:
        with Session(engine) as session:
            client_model = MapperModel.client_entity_to_model(model)
            session.add(client_model)
            session.commit()
            session.refresh(client_model)
            
    def update(self, updated_model: Client) -> None:
        with Session(engine) as session:
            client = session.get(Client_model, updated_model.client_id)
            if client:
                session.merge(MapperModel.client_entity_to_model(updated_model))
                session.commit()
        
    def get_by_id(self, id: str) -> Client|None:
        with Session(engine) as session:
            client = session.get(Client_model, id)
            return MapperModel.client_model_to_entity(client) if client else None
        
    def get_all(self) -> list[Client]|None:
        with Session(engine) as session:
            statement = select(Client_model)
            clients = session.exec(statement).all()
            return [MapperModel.client_model_to_entity(client) for client in clients]
        
    def delete(self, id: str) -> None:
        with Session(engine) as session:
            client = session.get(Client_model, id)
            if client:
                session.delete(client)
                session.commit()
