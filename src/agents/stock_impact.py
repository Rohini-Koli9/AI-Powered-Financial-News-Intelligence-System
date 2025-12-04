from .base_agent import BaseAgent
from typing import List, Dict
from ..utils.stock_mapper import StockMapper


class StockImpactAgent(BaseAgent):
    def __init__(self, data_dir: str = "data"):
        super().__init__()
        self.mapper = StockMapper(data_dir)

    def run(self, state: dict) -> dict:
        article_entity_map: Dict[str, List[Dict]] = state.get("article_entity_map", {})
        impacts: List[Dict] = []
        for aid, ents in article_entity_map.items():
            seen_symbols = set()
            for e in ents:
                if e["type"] == "COMPANY":
                    symbols = self.mapper.company_to_symbol(e["name"]) or self.mapper.company_to_symbol(e.get("normalized", ""))
                    for s in symbols:
                        if s not in seen_symbols:
                            impacts.append({"article_id": aid, "symbol": s, "confidence": 1.0, "type": "direct"})
                            seen_symbols.add(s)
                if e["type"] == "SECTOR":
                    sector = e.get("normalized") or e["name"]
                    for comp, secs in self.mapper._stock_map.get("company_to_sector", {}).items():
                        if sector.lower() in [x.lower() for x in secs]:
                            for s in self.mapper.company_to_symbol(comp):
                                if s not in seen_symbols:
                                    impacts.append({"article_id": aid, "symbol": s, "confidence": 0.7, "type": "sector"})
                                    seen_symbols.add(s)
                if e["type"] == "REGULATOR":
                    for comp in self.mapper._stock_map.get("companies", {}).keys():
                        for s in self.mapper.company_to_symbol(comp):
                            if s not in seen_symbols:
                                impacts.append({"article_id": aid, "symbol": s, "confidence": 0.4, "type": "regulator"})
                                seen_symbols.add(s)
        state["stock_impacts"] = impacts
        return state
