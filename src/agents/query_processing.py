from .base_agent import BaseAgent
from typing import List, Dict, Any


class QueryProcessingAgent(BaseAgent):
    def __init__(self, db, vectordb, ner, llm):
        super().__init__()
        self.db = db
        self.vectordb = vectordb
        self.ner = ner
        self.llm = llm

    def run(self, state: dict) -> dict:
        text: str = state.get("query", "")
        top_k: int = state.get("top_k", 10)
        ents = self.ner.extract(text)
        sectors = [e for e in ents if e["type"] == "SECTOR"]
        companies = [e for e in ents if e["type"] == "COMPANY"]
        regulators = [e for e in ents if e["type"] == "REGULATOR"]

        hits: Dict[str, Dict[str, Any]] = {}

        for c in companies:
            cname = c.get("normalized") or c["name"]
            for row in self.db.list_news_by_company(cname, limit=top_k):
                hits[row["id"]] = {"article": row, "score": hits.get(row["id"], {}).get("score", 0.0) + 0.6}
            for row in self.db.list_news_by_sector("Banking", limit=top_k):
                if row["id"] not in hits:
                    hits[row["id"]] = {"article": row, "score": 0.3}
                else:
                    hits[row["id"]]["score"] += 0.3

        for s in sectors:
            sname = s.get("normalized") or s["name"]
            for row in self.db.list_news_by_sector(sname, limit=top_k):
                if row["id"] not in hits:
                    hits[row["id"]] = {"article": row, "score": 0.5}
                else:
                    hits[row["id"]]["score"] += 0.5

        for r in regulators:
            rname = r.get("normalized") or r["name"]
            for row in self.db.list_news_by_regulator(rname, limit=top_k):
                if row["id"] not in hits:
                    hits[row["id"]] = {"article": row, "score": 0.5}
                else:
                    hits[row["id"]]["score"] += 0.5

        qres = self.vectordb.query(text, top_k=top_k)
        for r in qres:
            aid = r["metadata"].get("article_id") if isinstance(r.get("metadata"), dict) else None
            art = self.db.get_article(aid) if aid else None
            if art:
                base = 1.0 - float(r.get("distance", 0.0))
                if aid not in hits:
                    hits[aid] = {"article": art, "score": base}
                else:
                    hits[aid]["score"] += base

        results: List[Dict[str, Any]] = []
        for aid, item in hits.items():
            item["explanation"] = self.llm.explain(text, item["article"].get("title", ""))
            results.append(item)
        results.sort(key=lambda x: x.get("score", 0.0), reverse=True)
        state["search_results"] = results[:top_k]
        return state
