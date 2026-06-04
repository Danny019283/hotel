from domain.entities.client import Client
from domain.bussiness_rules.client_rules import ClientRules
from domain.exeptions import DomainError
from application.dtos.client_dto import ClientResponseDTO, CreateClientDTO, UpdateClientDTO
from infrastructure.repositories.client_repo import Client_repo


class ClientCases:
    def __init__(self, client_repo: Client_repo | None = None):
        self.client_repo = client_repo or Client_repo()

    def register_client(self, client_id: str, name: str, last_name: str, phone: int, email: str) -> Client:
        if self.client_repo.get_by_id(client_id) is not None:
            raise DomainError("client already exists")

        client = Client(client_id, name, last_name, phone, email)
        ClientRules.validate_client(client)
        self.client_repo.add(client)
        return client

    def register_client_dto(self, dto: CreateClientDTO) -> ClientResponseDTO:
        client = self.register_client(dto.client_id, dto.name, dto.last_name, dto.phone, dto.email)
        return ClientResponseDTO(
            client_id=client.client_id,
            name=client.name,
            last_name=client.last_name,
            phone=client.phone,
            email=client.email,
        )

    def consult_client(self, client_id: str) -> Client | None:
        return self.client_repo.get_by_id(client_id)

    def consult_client_dto(self, client_id: str) -> ClientResponseDTO | None:
        client = self.consult_client(client_id)
        if client is None:
            return None
        return ClientResponseDTO(
            client_id=client.client_id,
            name=client.name,
            last_name=client.last_name,
            phone=client.phone,
            email=client.email,
        )

    def update_client(self, client_id: str, name: str, last_name: str, phone: int, email: str) -> Client:
        if self.client_repo.get_by_id(client_id) is None:
            raise DomainError("client not found")

        client = Client(client_id, name, last_name, phone, email)
        ClientRules.validate_client(client)
        self.client_repo.update(client)
        return client

    def update_client_dto(self, client_id: str, dto: UpdateClientDTO) -> ClientResponseDTO:
        client = self.update_client(client_id, dto.name, dto.last_name, dto.phone, dto.email)
        return ClientResponseDTO(
            client_id=client.client_id,
            name=client.name,
            last_name=client.last_name,
            phone=client.phone,
            email=client.email,
        )

    def delete_client(self, client_id: str) -> None:
        if self.client_repo.get_by_id(client_id) is None:
            raise DomainError("client not found")
        self.client_repo.delete(client_id)

    def list_clients(self) -> list[Client]:
        return self.client_repo.get_all() or []

    def list_clients_dto(self) -> list[ClientResponseDTO]:
        return [
            ClientResponseDTO(
                client_id=client.client_id,
                name=client.name,
                last_name=client.last_name,
                phone=client.phone,
                email=client.email,
            )
            for client in self.list_clients()
        ]
