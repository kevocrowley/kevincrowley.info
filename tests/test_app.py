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


def test_resume_endpoint(client):
    response = client.get("/resume")
    assert response.status_code == 200
    assert response.content_type == "application/pdf"


def test_404_error(client):
    response = client.get("/nonexistent")
    assert response.status_code == 404
    assert b"404" in response.data


def test_blog_post_listed(client):
    response = client.get("/")
    html = response.data.decode("utf-8")
    assert "Blog" in html


def test_blog_post_detail(client):
    response = client.get("/blog/bedrock-observability")
    assert response.status_code == 200
    html = response.data.decode("utf-8")
    assert "Datadog Observability" in html


def test_blog_post_not_found(client):
    response = client.get("/blog/nonexistent-post")
    assert response.status_code == 404


def test_security_headers(client):
    response = client.get("/")
    assert response.headers.get("X-Content-Type-Options") == "nosniff"
    assert response.headers.get("X-Frame-Options") == "DENY"
