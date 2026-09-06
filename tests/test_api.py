from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert "Agentic URL Shortener API is running" in response.json()["message"]


def test_shorten_and_redirect():
    payload = {"url": "https://example.com"}
    shorten_response = client.post("/shorten", json=payload)
    assert shorten_response.status_code == 200
    short_code = shorten_response.json()["short_code"]
    assert short_code

    redirect_response = client.get(f"/r/{short_code}", follow_redirects=False)
    assert redirect_response.status_code == 307
    assert redirect_response.headers["location"] == "https://example.com"

    stats_response = client.get(f"/stats/{short_code}")
    assert stats_response.status_code == 200
    assert stats_response.json()["clicks"] >= 1
