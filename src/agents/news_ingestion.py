import json
from pathlib import Path
from .base_agent import BaseAgent
from ..utils.rss_parser import fetch_rss_articles


class NewsIngestionAgent(BaseAgent):
    def run(self, state: dict) -> dict:
        mode = state.get("mode", "ingest_mock")
        if mode == "single_article":
            state["raw_articles"] = state.get("raw_articles", [])
            state["parsed_articles"] = [self._normalize(a) for a in state["raw_articles"]]
            return state
        if mode == "ingest_rss":
            raw = fetch_rss_articles()
            state["raw_articles"] = raw
        else:
            p = Path("data/mock_news.json")
            if p.exists():
                with open(p, "r", encoding="utf-8") as f:
                    state["raw_articles"] = json.load(f)
            else:
                state["raw_articles"] = []
        state["parsed_articles"] = [self._normalize(a) for a in state["raw_articles"]]
        return state

    def _normalize(self, a: dict) -> dict:
        aid = a.get("id") or a.get("url") or a.get("title")
        return {
            "id": str(aid),
            "title": a.get("title", "").strip(),
            "content": a.get("content", "").strip(),
            "source": a.get("source", ""),
            "published_at": a.get("published_at", ""),
            "url": a.get("url", ""),
            "category": a.get("category"),
        }
