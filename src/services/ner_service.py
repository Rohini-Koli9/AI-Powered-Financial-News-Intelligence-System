import re
from typing import List, Dict


class NERService:
    def __init__(self):
        self.nlp = None
        try:
            import spacy
            try:
                self.nlp = spacy.load("en_core_web_lg")
            except Exception:
                self.nlp = spacy.load("en_core_web_sm")
        except Exception:
            self.nlp = None
        self.company_keywords = [
            "HDFC Bank", "ICICI Bank", "SBI", "State Bank of India", "Kotak", "Kotak Mahindra Bank", "Axis Bank",
            "TCS", "Infosys", "Wipro", "HCL Tech", "Sun Pharma", "Dr. Reddy's", "Cipla", "Tata Motors", "Maruti", "M&M",
            "Mahindra", "Reliance", "ONGC", "NTPC"
        ]
        self.regulator_keywords = ["RBI", "Reserve Bank of India", "SEBI", "Finance Ministry"]
        self.sector_keywords = [
            "Banking", "Financial Services", "IT", "Information Technology", "Pharma", "Automobile", "Auto", "Energy"
        ]

    def extract(self, text: str) -> List[Dict]:
        ents = []
        if self.nlp:
            doc = self.nlp(text)
            for e in doc.ents:
                ents.append({"id": f"{e.label_}:{e.text}", "type": e.label_, "name": e.text, "normalized": self._normalize(e.text)})
        for kw in self.company_keywords:
            if re.search(rf"\b{re.escape(kw)}\b", text, re.IGNORECASE):
                ents.append({"id": f"COMPANY:{kw}", "type": "COMPANY", "name": kw, "normalized": self._normalize(kw)})
        for kw in self.regulator_keywords:
            if re.search(rf"\b{re.escape(kw)}\b", text, re.IGNORECASE):
                ents.append({"id": f"REGULATOR:{kw}", "type": "REGULATOR", "name": kw, "normalized": self._normalize(kw)})
        for kw in self.sector_keywords:
            if re.search(rf"\b{re.escape(kw)}\b", text, re.IGNORECASE):
                ents.append({"id": f"SECTOR:{kw}", "type": "SECTOR", "name": kw, "normalized": self._normalize(kw)})
        seen = set()
        uniq = []
        for e in ents:
            k = (e["type"], e["normalized"] or e["name"].lower())
            if k not in seen:
                seen.add(k)
                uniq.append(e)
        return uniq

    def _normalize(self, name: str) -> str:
        m = name.strip().lower()
        if m in ["reserve bank", "reserve bank of india", "central bank"]:
            return "rbi"
        if m in ["auto", "automobile"]:
            return "automobile"
        return m
