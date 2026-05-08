import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_homepage_loads(client):
    response = client.get("/")
    assert response.status_code == 200


def test_profile_data(client):
    response = client.get("/")
    html = response.data.decode("utf-8")
    assert "Kevin Crowley" in html
    assert "Platform Engineer" in html
