import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session, create_engine
from sqlmodel.pool import StaticPool
from app.main import app, get_session

# Cria um banco de dados SQLite em memória para os testes
sqlite_url = "sqlite://"
engine = create_engine(
    sqlite_url, 
    connect_args={"check_same_thread": False}, 
    poolclass=StaticPool
)

@pytest.fixture(name="session")
def session_fixture():
    # Cria as tabelas no banco em memória antes do teste
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    # Limpa o banco após o teste (opcional)
    SQLModel.metadata.drop_all(engine)

@pytest.fixture(name="client")
def client_fixture(session: Session):
    # Sobrescreve a dependência get_session para usar o banco em memória
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def test_criar_os_mecanica(client: TestClient):
    response = client.post("/os?descricao=Rolamento+com+vibracao")
    assert response.status_code == 200
    data = response.json()
    assert data["categoria"] == "Mecânica"
    assert data["status"] == "aberta"

def test_criar_os_eletrica(client: TestClient):
    response = client.post("/os?descricao=Fio+solto")
    assert response.status_code == 200
    data = response.json()
    assert data["categoria"] == "Elétrica"