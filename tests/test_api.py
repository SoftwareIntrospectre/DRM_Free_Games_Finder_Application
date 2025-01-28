import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_game():
    response = client.get("/game/DOOM")
    assert response.status_code == 200
    assert response.json() == {"name": "DOOM", "on_steam": True, "on_gog": False}
