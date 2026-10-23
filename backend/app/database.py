from sqlmodel import SQLModel, create_engine, Session
import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@db:5432/osdb"
)

engine = create_engine(DATABASE_URL, echo=False)


def criar_tabelas():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session