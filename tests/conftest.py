import pytest
from fastapi.testclient import TestClient

from boilerplate.main import app


@pytest.fixture()
def client():
    """Cliente de testes para a API."""
    return TestClient(app)


@pytest.fixture()
def seed(client):
    """Cria dados básicos de teste via API e retorna a lista criada."""
    items = []
    payloads = [
        {"title": "Seed 1", "description": "", "completed": False},
        {"title": "Seed 2", "description": "", "completed": True},
    ]
    for p in payloads:
        resp = client.post("/api/v1/todos", json=p)
        assert resp.status_code == 201
        items.append(resp.json())
    return items
