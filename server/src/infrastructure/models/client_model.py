from sqlmodel import SQLModel, Field

class Client_model(SQLModel, table=True):
    __tablename__ =  "Clients"
    client_id: str = Field(primary_key=True, max_length=10)
    name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    phone: int = Field(max_digits=8)
    email: str = Field(max_length=50)
