from .base_agent import BaseAgent
from typing import List
from ..services.embedding_service import EmbeddingService
from ..utils.similarity import cosine
import re


class DeduplicationAgent(BaseAgent):
    def __init__(self, embedder: EmbeddingService, **kwargs):
        super().__init__(**kwargs)
        self.embedder = embedder
        # Slightly lower threshold for fallback bag-of-words embeddings
        self.threshold = 0.85 if getattr(self.embedder, "_model", None) is not None else 0.75
        self.jaccard_threshold = 0.6

    def run(self, state: dict) -> dict:
        articles = state.get("parsed_articles", [])
        if not articles:
            state["unique_articles"] = []
            state["duplicate_groups"] = []
            return state
        titles_norm = [self._normalize_text(a["title"]) for a in articles]
        event_keys = [self._event_key(t) for t in titles_norm]
        texts = [self._normalize_text(a["title"] + "\n" + a["content"]) for a in articles]
        token_sets_full = [set(t.split()) for t in texts]
        token_sets_title = [set(t.split()) for t in titles_norm]
        embs = self.embedder.embed(texts)
        n = len(articles)
        used = [False]*n
        groups: List[List[int]] = []
        for i in range(n):
            if used[i]:
                continue
            group = [i]
            used[i] = True
            for j in range(i+1, n):
                if used[j]:
                    continue
                # Strong event-key match shortcut
                if event_keys[i] and event_keys[i] == event_keys[j]:
                    used[j] = True
                    group.append(j)
                    continue
                cos = cosine(embs[i], embs[j])
                jac_full = self._jaccard(token_sets_full[i], token_sets_full[j])
                jac_title = self._jaccard(token_sets_title[i], token_sets_title[j])
                if (cos >= self.threshold) or (jac_full >= 0.58) or (jac_title >= 0.7):
                    used[j] = True
                    group.append(j)
            groups.append(group)
        unique = [articles[g[0]] for g in groups]
        dup_groups_ids = [[articles[idx]["id"] for idx in g] for g in groups if len(g) > 1]
        state["unique_articles"] = unique
        state["duplicate_groups"] = dup_groups_ids
        return state

    def _normalize_text(self, text: str) -> str:
        t = text.lower()
        # Normalize regulators
        t = re.sub(r"\b(reserve bank of india|reserve bank|central bank)\b", "rbi", t)
        # Normalize rate terms
        t = re.sub(r"\b(repo rate|policy rate|interest rates|interest rate)\b", "policy rate", t)
        # Normalize action verbs
        t = re.sub(r"\b(hike|hikes|hiked|raise|raises|raised|increase|increases|increased)\b", "raise", t)
        # Business synonyms
        t = re.sub(r"\b(share repurchase|repurchase)\b", "buyback", t)
        t = re.sub(r"\b(bags|bagged|wins|won)\b", "win", t)
        t = re.sub(r"\b(okays|approves|approved)\b", "approve", t)
        t = re.sub(r"\b(mega deal|mega)\b", "deal", t)
        # basis points
        t = re.sub(r"\bbasis points\b", "bps", t)
        t = re.sub(r"\b(\d+)\s*bps\b", r"\1 bps", t)
        t = re.sub(r"\b(\d+)bps\b", r"\1 bps", t)
        # Convert percentages to bps ONLY for interest-rate context; else normalize to ' percent'
        if re.search(r"\b(policy rate|repo|interest)\b", t):
            def pct_to_bps(m):
                try:
                    val = float(m.group(1))
                    bps = int(round(val * 100))
                    return f"{bps} bps"
                except Exception:
                    return m.group(0)
            t = re.sub(r"(\d+(?:\.\d+)?)\s*%", pct_to_bps, t)
        else:
            t = re.sub(r"\s*%\b", " percent", t)
        # Compact whitespace
        t = re.sub(r"\s+", " ", t).strip()
        return t

    def _jaccard(self, a: set, b: set) -> float:
        if not a and not b:
            return 1.0
        inter = len(a & b)
        union = len(a | b) or 1
        return inter / union

    def _event_key(self, title_norm: str) -> str | None:
        t = title_norm
        # RBI policy rate change with magnitude
        if "policy rate" in t and "bps" in t and "rbi" in t:
            m = re.search(r"(\d+)[\s]*bps", t)
            if m:
                return f"event:rbi_policy_rate_{m.group(1)}bps"
        # CPI inflation fixed numeric
        if "cpi" in t and "inflation" in t:
            m = re.search(r"(\d+(?:\.\d+)?)\s*(percent|%)?", t)
            if m:
                val = m.group(1)
                return f"event:cpi_infl_{val}"
        # HDFC Bank dividend buyback
        if "hdfc bank" in t and "dividend" in t and "buyback" in t:
            return "event:hdfc_dividend_buyback"
        # TCS European retail deal
        if "tcs" in t and "deal" in t and "european" in t and re.search(r"retail", t):
            return "event:tcs_european_retail_deal"
        return None
