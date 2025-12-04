from typing import TypedDict, List, Dict


class NewsProcessingState(TypedDict, total=False):
    mode: str
    raw_articles: List[dict]
    parsed_articles: List[dict]
    unique_articles: List[dict]
    duplicate_groups: List[List[str]]
    entities: List[dict]
    article_entity_map: Dict[str, List[dict]]
    stock_impacts: List[dict]
    processing_stats: dict
    errors: List[str]


class QueryState(TypedDict, total=False):
    query: str
    top_k: int
    search_results: List[dict]
