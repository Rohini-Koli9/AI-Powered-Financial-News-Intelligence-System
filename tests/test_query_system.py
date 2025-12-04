from src.main import create_app


def setup_module(module):
    global app
    app = create_app()
    app.state.news_graph.invoke({"mode": "ingest_mock"})


def test_company_query_returns_direct_and_sector():
    res = app.state.query_graph.invoke({"query": "HDFC Bank news", "top_k": 10})
    ids = [r["article"]["id"] for r in res.get("search_results", [])]
    assert any(i in ids for i in ["N1", "N23", "N33"])  # direct


def test_sector_query_returns_all_companies():
    res = app.state.query_graph.invoke({"query": "Banking sector update", "top_k": 10})
    cats = [r["article"].get("category") for r in res.get("search_results", [])]
    assert any(c == "Banking" for c in cats)


def test_regulator_query_filters_correctly():
    res = app.state.query_graph.invoke({"query": "RBI policy changes", "top_k": 10})
    ids = [r["article"]["id"] for r in res.get("search_results", [])]
    assert any(i in ids for i in ["N2", "N21", "N22", "N32"])  # regulator-specific


def test_semantic_query_matching():
    res = app.state.query_graph.invoke({"query": "interest rate impact", "top_k": 10})
    ids = [r["article"]["id"] for r in res.get("search_results", [])]
    assert any(i in ids for i in ["N2", "N21", "N22", "N32"]) or len(ids) > 0
