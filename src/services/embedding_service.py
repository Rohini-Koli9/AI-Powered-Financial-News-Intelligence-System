from typing import List

class EmbeddingService:
    def __init__(self, model_name: str):
        self.model_name = model_name
        self._model = None
        try:
            from sentence_transformers import SentenceTransformer
            self._model = SentenceTransformer(model_name)
            self.dim = self._model.get_sentence_embedding_dimension()
        except Exception:
            self._model = None
            self.dim = 384

    def embed(self, texts: List[str]) -> List[List[float]]:
        if self._model is not None:
            return [v.tolist() for v in self._model.encode(texts, convert_to_numpy=True, normalize_embeddings=True)]
        return [self._fallback_embed(t) for t in texts]

    def _fallback_embed(self, text: str) -> List[float]:
        tokens = self._tokenize(text)
        vec = [0.0] * self.dim
        for i, tok in enumerate(tokens):
            idx = (hash(tok) % self.dim)
            vec[idx] += 1.0
            if i + 1 < len(tokens):
                bigram = tok + "_" + tokens[i + 1]
                bidx = (hash(bigram) % self.dim)
                vec[bidx] += 0.5
        norm = sum(v * v for v in vec) ** 0.5
        if norm > 0:
            vec = [v / norm for v in vec]
        return vec

    def _tokenize(self, text: str) -> List[str]:
        import re
        text = text.lower()
        # Basic cleanup of numbers like 25bps -> 25 bps, 0.25% -> 0.25 %
        text = re.sub(r"(\d)([a-zA-Z]+)", r"\1 \2", text)
        text = re.sub(r"[^a-z0-9%]+", " ", text)
        toks = [t for t in text.split() if t]
        return toks
