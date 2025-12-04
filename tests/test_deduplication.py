from src.agents.deduplication import DeduplicationAgent
from src.services.embedding_service import EmbeddingService


def test_exact_duplicate_detection():
    embedder = EmbeddingService("sentence-transformers/all-MiniLM-L6-v2")
    agent = DeduplicationAgent(embedder)
    a1 = {"id": "A1", "title": "RBI raises repo rate", "content": "The RBI increased repo by 25 bps"}
    a2 = {"id": "A2", "title": "RBI raises repo rate", "content": "The RBI increased repo by 25 bps"}
    state = {"parsed_articles": [a1, a2]}
    out = agent.run(state)
    assert len(out["unique_articles"]) == 1
    assert any(set(g) == {"A1", "A2"} for g in out["duplicate_groups"]) or len(out["duplicate_groups"]) >= 1


def test_semantic_duplicate_detection():
    embedder = EmbeddingService("sentence-transformers/all-MiniLM-L6-v2")
    agent = DeduplicationAgent(embedder)
    a1 = {"id": "B1", "title": "RBI increases repo rate by 25 basis points", "content": "to combat inflation"}
    a2 = {"id": "B2", "title": "Reserve Bank hikes interest rates by 0.25%", "content": "hawkish stance"}
    a3 = {"id": "B3", "title": "Central bank raises policy rate 25bps", "content": "signals vigilance"}
    state = {"parsed_articles": [a1, a2, a3]}
    out = agent.run(state)
    assert len(out["unique_articles"]) == 1


def test_different_articles_not_duplicated():
    embedder = EmbeddingService("sentence-transformers/all-MiniLM-L6-v2")
    agent = DeduplicationAgent(embedder)
    a1 = {"id": "C1", "title": "TCS wins large deal", "content": "cloud migration"}
    a2 = {"id": "C2", "title": "Sun Pharma gets USFDA approval", "content": "oncology"}
    state = {"parsed_articles": [a1, a2]}
    out = agent.run(state)
    assert len(out["unique_articles"]) == 2


def test_deduplication_accuracy_benchmark(app):
    res = app.state.news_graph.invoke({"mode": "ingest_mock"})
    unique_ids = {a["id"] for a in res.get("unique_articles", [])}
    # Expected duplicate groups - each should reduce to a single unique kept
    groups = [
        {"N2", "N21", "N22", "N32"},
        {"N1", "N23", "N33"},
        {"N5", "N30"},
        {"N18", "N31"}
    ]
    correct = 0
    for g in groups:
        present = len(g & unique_ids)
        if present == 1:
            correct += 1
    accuracy = correct / len(groups)
    assert accuracy >= 0.95
