from sqlmodel import Session, select

from infrastructure.database.connection import engine
from domain.entities.payment_method import Payment_Method
from infrastructure.mappers.mapper_model import MapperModel
from infrastructure.models.payment_method_model import Payment_Method_Model
from infrastructure.repositories.irepository import IRespository


class Payment_Method_repo(IRespository[Payment_Method]):
    def add(self, model: Payment_Method) -> None:
        with Session(engine) as session:
            payment_method_model = MapperModel.payment_method_entity_to_model(model)
            session.add(payment_method_model)
            session.commit()
            session.refresh(payment_method_model)

    def update(self, updated_model: Payment_Method) -> None:
        with Session(engine) as session:
            payment_method = session.get(Payment_Method_Model, updated_model.payment_method_id)
            if payment_method:
                session.merge(MapperModel.payment_method_entity_to_model(updated_model))
                session.commit()

    def get_by_id(self, id: int) -> Payment_Method | None:
        with Session(engine) as session:
            payment_method = session.get(Payment_Method_Model, id)
            return MapperModel.payment_method_model_to_entity(payment_method) if payment_method else None

    def get_all(self) -> list[Payment_Method] | None:
        with Session(engine) as session:
            statement = select(Payment_Method_Model)
            payment_methods = session.exec(statement).all()
            return [MapperModel.payment_method_model_to_entity(payment_method) for payment_method in payment_methods]

    def delete(self, id: int) -> None:
        with Session(engine) as session:
            payment_method = session.get(Payment_Method_Model, id)
            if payment_method:
                session.delete(payment_method)
                session.commit()
