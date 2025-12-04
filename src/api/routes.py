from fastapi import APIRouter, Depends, Request, HTTPException
from .schemas import ProcessArticleRequest, QueryRequest, QueryResponse, ArticleResponse, StatsResponse
from typing import List

router = APIRouter()


@router.get("/health")
def health():
    return {"status": "ok"}


@router.post("/news/ingest")
async def ingest_news(request: Request, mode: str = "ingest_mock"):
    app = request.app
    m = "ingest_rss" if mode in ("rss", "ingest_rss") else "ingest_mock"
    result = app.state.news_graph.invoke({"mode": m})
    return {"ingested": len(result.get("parsed_articles", [])), "unique": len(result.get("unique_articles", []))}


@router.post("/news/process")
async def process_news(request: Request, body: ProcessArticleRequest):
    app = request.app
    state = {"mode": "single_article", "raw_articles": [body.dict()]}
    result = app.state.news_graph.invoke(state)
    return {"unique_processed": len(result.get("unique_articles", []))}


@router.get("/query", response_model=QueryResponse)
async def query_news(request: Request, q: str, top_k: int = 10):
    app = request.app
    result = app.state.query_graph.invoke({"query": q, "top_k": top_k})
    items = []
    for hit in result.get("search_results", []):
        a = hit.get("article", {})
        aid = a.get("id")
        article = app.state.db.get_article(aid) if aid else a
        items.append({
            "article": article,
            "score": hit.get("score", 0.0),
            "explanation": hit.get("explanation")
        })
    return {"results": items}


@router.get("/news/{article_id}", response_model=ArticleResponse)
async def get_article(request: Request, article_id: str):
    app = request.app
    article = app.state.db.get_article(article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Not found")
    return article


@router.get("/entities")
async def list_entities(request: Request):
    app = request.app
    return app.state.db.list_entities()


@router.get("/stocks/{symbol}/news")
async def news_by_stock(request: Request, symbol: str, top_k: int = 20):
    app = request.app
    return app.state.db.list_news_by_stock(symbol, limit=top_k)


@router.get("/sectors/{sector}/news")
async def news_by_sector(request: Request, sector: str, top_k: int = 20):
    app = request.app
    return app.state.db.list_news_by_sector(sector, limit=top_k)


@router.get("/stats", response_model=StatsResponse)
async def stats(request: Request):
    app = request.app
    return app.state.db.stats()
