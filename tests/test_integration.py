from fastapi.testclient import TestClient
from src.main import create_app


def test_api_endpoints_integration():
    app = create_app()
    client = TestClient(app)

    r = client.get("/api/v1/health")
    assert r.status_code == 200 and r.json().get("status") == "ok"

    r = client.post("/api/v1/news/ingest")
    assert r.status_code == 200

    r = client.get("/api/v1/query", params={"q": "HDFC Bank news", "top_k": 5})
    assert r.status_code == 200
    data = r.json()
    assert "results" in data

    r = client.get("/api/v1/entities")
    assert r.status_code == 200

    r = client.get("/api/v1/stats")
    assert r.status_code == 200


def test_full_pipeline_processing():
    app = create_app()
    article = {
        "id": "X1",
        "title": "RBI increases repo rate by 25 bps",
        "content": "Reserve Bank hiked policy rate to curb inflation.",
        "source": "Test",
        "published_at": "2024-05-01T00:00:00Z",
        "url": "https://example.com/x1",
        "category": "Regulatory"
    }
    res = app.state.news_graph.invoke({"mode": "single_article", "raw_articles": [article]})
    assert len(res.get("unique_articles", [])) == 1
    saved = app.state.db.get_article("X1")
    assert saved is not None
