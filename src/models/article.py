from pydantic import BaseModel
from typing import Optional, Dict, Any


class Article(BaseModel):
    id: str
    title: str
    content: str
    source: str
    published_at: str
    url: str
    category: Optional[str] = None
    metadata: Dict[str, Any] | None = None
