from pydantic import BaseModel
from typing import Optional


class Entity(BaseModel):
    id: str
    type: str
    name: str
    normalized: Optional[str] = None


class StockImpact(BaseModel):
    article_id: str
    symbol: str
    confidence: float
    type: str  # direct, sector, regulator
