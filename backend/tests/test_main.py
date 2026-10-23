import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_criar_os_mecanica():
    response = client.post("/os?descricao=Rolamento+com+vibracao")
    assert response.status_code == 200
    data = response.json()
    assert data["categoria"] == "Mecânica"
    assert data["status"] == "aberta"

def test_criar_os_eletrica():
    response = client.post("/os?descricao=Fio+solto")
    assert response.status_code == 200
    data = response.json()
    assert data["categoria"] == "Elétrica"