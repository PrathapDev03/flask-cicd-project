
import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


def test_home_page(client):
    response = client.get("/")

    assert response.status_code == 200

    data = response.get_json()

    assert data["message"] == "Welcome to Flask CI/CD Pipeline!"
    assert data["application"] == "Flask Demo Application"


def test_health_check(client):
    response = client.get("/health")

    assert response.status_code == 200

    data = response.get_json()

    assert data["status"] == "healthy"


def test_health_failure_simulation(client, monkeypatch):
    monkeypatch.setenv("SIMULATE_HEALTH_FAILURE", "true")

    response = client.get("/health")

    assert response.status_code == 500

    data = response.get_json()

    assert data["status"] == "unhealthy"
