from pydantic import BaseModel
from typing import List, Optional, Dict, Any


class ProcessArticleRequest(BaseModel):
    title: str
    content: str
    source: str
    published_at: str
    url: str
    category: Optional[str] = None


class QueryRequest(BaseModel):
    q: str
    top_k: int = 10


class ArticleResponse(BaseModel):
    id: str
    title: str
    content: str
    source: str
    published_at: str
    url: str
    category: Optional[str] = None
    metadata: Dict[str, Any] | None = None


class QueryResponseItem(BaseModel):
    article: ArticleResponse
    score: float
    explanation: Optional[str] = None


class QueryResponse(BaseModel):
    results: List[QueryResponseItem]


class StatsResponse(BaseModel):
    articles: int
    entities: int
    stocks: int
    duplicates: int
    last_ingested_at: Optional[str] = None
