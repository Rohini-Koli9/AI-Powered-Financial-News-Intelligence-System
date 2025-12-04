from .base_agent import BaseAgent
from typing import List, Dict


class StorageIndexingAgent(BaseAgent):
    def __init__(self, db, vectordb, embedder):
        super().__init__()
        self.db = db
        self.vectordb = vectordb
        self.embedder = embedder

    def run(self, state: dict) -> dict:
        unique = state.get("unique_articles", [])
        article_entity_map = state.get("article_entity_map", {})
        impacts = state.get("stock_impacts", [])
        for a in unique:
            self.db.upsert_article(a)
            ents = article_entity_map.get(a["id"], [])
            self.db.link_article_entities(a["id"], ents)
        if unique:
            ids = [a["id"] for a in unique]
            docs = [a["title"] + "\n" + a["content"] for a in unique]
            metas = [{"article_id": a["id"], "title": a["title"], "source": a["source"], "category": a.get("category")}
                     for a in unique]
            self.vectordb.add(ids, docs, metas)
        if impacts:
            self.db.add_stock_impacts(impacts)
        return state
