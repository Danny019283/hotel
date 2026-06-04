from sqlmodel import Session, select

from infrastructure.database.connection import engine
from domain.entities.bill import Bill
from infrastructure.mappers.mapper_model import MapperModel
from infrastructure.models.bill_model import Bill_model
from infrastructure.repositories.irepository import IRespository


class Bill_repo(IRespository[Bill]):
    def add(self, model: Bill) -> None:
        with Session(engine) as session:
            bill_model = MapperModel.bill_entity_to_model(model)
            session.add(bill_model)
            session.flush()
            if model.bill_id != bill_model.bill_id:
                model.bill_id = bill_model.bill_id
            session.commit()
            session.refresh(bill_model)

    def update(self, updated_model: Bill) -> None:
        with Session(engine) as session:
            bill = session.get(Bill_model, updated_model.bill_id)
            if bill:
                session.merge(MapperModel.bill_entity_to_model(updated_model))
                session.commit()

    def get_by_id(self, id: int) -> Bill | None:
        with Session(engine) as session:
            bill = session.get(Bill_model, id)
            return MapperModel.bill_model_to_entity(session, bill) if bill else None

    def get_by_booking_id(self, booking_id: int) -> Bill | None:
        with Session(engine) as session:
            statement = select(Bill_model).where(Bill_model.booking_id == booking_id)
            bill = session.exec(statement).first()
            return MapperModel.bill_model_to_entity(session, bill) if bill else None

    def get_all(self) -> list[Bill] | None:
        with Session(engine) as session:
            statement = select(Bill_model)
            bills = session.exec(statement).all()
            return [MapperModel.bill_model_to_entity(session, bill) for bill in bills]

    def delete(self, id: int) -> None:
        with Session(engine) as session:
            bill = session.get(Bill_model, id)
            if bill:
                session.delete(bill)
                session.commit()
