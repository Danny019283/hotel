import os
import urllib
from pathlib import Path

from sqlalchemy import create_engine
from sqlmodel import SQLModel
from infrastructure.models.bill_model import Bill_model
from infrastructure.models.booking_room_model import Booking_Room_model
from infrastructure.models.booking import Booking_model
from infrastructure.models.client_model import Client_model
from infrastructure.models.payment_method_model import Payment_Method_Model
from infrastructure.models.room_model import Room_model
from infrastructure.models.user_model import User_model


def _load_dotenv() -> None:
    env_path = Path(__file__).resolve().parents[3] / ".env"
    if not env_path.exists():
        return

    for line in env_path.read_text(encoding="utf-8").splitlines():
        stripped_line = line.strip()
        if not stripped_line or stripped_line.startswith("#") or "=" not in stripped_line:
            continue

        key, value = stripped_line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


def _require_env(name: str) -> str:
    value = os.getenv(name)
    if value is None or not value.strip():
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value.strip()


_load_dotenv()


SERVER = _require_env("DB_SERVER")
DATABASE = _require_env("DB_NAME")
USERNAME = _require_env("DB_USERNAME")
PASSWORD = _require_env("DB_PASSWORD")
DRIVER = os.getenv("DB_DRIVER", "ODBC Driver 17 for SQL Server").strip()
TRUST_SERVER_CERTIFICATE = os.getenv("DB_TRUST_SERVER_CERTIFICATE", "yes").strip()
DB_ECHO = os.getenv("DB_ECHO", "false").strip().lower() == "true"

connection_string = (
    f"DRIVER={{{DRIVER}}};"
    f"SERVER={SERVER};"
    f"DATABASE={DATABASE};"
    f"UID={USERNAME};"
    f"PWD={PASSWORD};"
    f"TrustServerCertificate={TRUST_SERVER_CERTIFICATE};"
)

params = urllib.parse.quote_plus(connection_string)
connection_url = f"mssql+pyodbc:///?odbc_connect={params}"

engine = create_engine(connection_url, echo=DB_ECHO)


def create_db_and_tables():
    print(SQLModel.metadata.tables.keys())
    SQLModel.metadata.create_all(engine)
