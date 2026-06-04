from fastapi import APIRouter, HTTPException, status

from application.dtos.client_dto import ClientResponseDTO, CreateClientDTO, UpdateClientDTO
from application.uses_cases.client_cases import ClientCases
from domain.exeptions import DomainError


router = APIRouter(prefix="/clients", tags=["Clients"])
client_cases = ClientCases()


@router.post("", response_model=ClientResponseDTO, status_code=status.HTTP_201_CREATED)
def register_client(dto: CreateClientDTO):
    try:
        return client_cases.register_client_dto(dto)
    except DomainError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get("/{client_id}", response_model=ClientResponseDTO)
def consult_client(client_id: str):
    client = client_cases.consult_client_dto(client_id)
    if client is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="client not found")
    return client


@router.put("/{client_id}", response_model=ClientResponseDTO)
def update_client(client_id: str, dto: UpdateClientDTO):
    try:
        return client_cases.update_client_dto(client_id, dto)
    except DomainError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.delete("/{client_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_client(client_id: str):
    try:
        client_cases.delete_client(client_id)
    except DomainError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.get("", response_model=list[ClientResponseDTO])
def list_clients():
    return client_cases.list_clients_dto()
