from .base_agent import BaseAgent
from typing import List, Dict
from ..services.ner_service import NERService


class EntityExtractionAgent(BaseAgent):
    def __init__(self, ner: NERService, **kwargs):
        super().__init__(**kwargs)
        self.ner = ner

    def run(self, state: dict) -> dict:
        unique = state.get("unique_articles", [])
        all_entities: List[Dict] = []
        article_entity_map = {}
        for a in unique:
            ents = self.ner.extract(a["title"] + "\n" + a["content"])
            article_entity_map[a["id"]] = ents
            all_entities.extend(ents)
        state["entities"] = all_entities
        state["article_entity_map"] = article_entity_map
        return state
