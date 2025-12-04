import json
from typing import Dict, List
from pathlib import Path


class StockMapper:
    def __init__(self, data_dir: str):
        self.base = Path(data_dir)
        self._stock_map = {}
        self._sector_hierarchy = {}
        self._load()

    def _load(self):
        try:
            with open(self.base / "stock_mappings.json", "r", encoding="utf-8") as f:
                self._stock_map = json.load(f)
        except Exception:
            self._stock_map = {}
        try:
            with open(self.base / "sector_hierarchy.json", "r", encoding="utf-8") as f:
                self._sector_hierarchy = json.load(f)
        except Exception:
            self._sector_hierarchy = {}

    def company_to_symbol(self, name: str) -> List[str]:
        return self._stock_map.get("companies", {}).get(name, [])

    def sector_of_company(self, name: str) -> List[str]:
        return self._stock_map.get("company_to_sector", {}).get(name, [])

    def sector_children(self, sector: str) -> List[str]:
        return self._sector_hierarchy.get(sector, [])
