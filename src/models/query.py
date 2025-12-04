from pydantic import BaseModel


class Query(BaseModel):
    text: str
    top_k: int = 10
