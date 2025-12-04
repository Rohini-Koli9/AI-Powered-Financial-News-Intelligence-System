from typing import List, Dict, Any
import os


class VectorDB:
    def __init__(self, persist_path: str, embedder):
        self.persist_path = persist_path
        self.embedder = embedder
        self._collection = None
        self._init()

    def _init(self):
        try:
            os.makedirs(self.persist_path, exist_ok=True)
            import chromadb
            from chromadb.config import Settings
            client = chromadb.PersistentClient(path=self.persist_path, settings=Settings(anonymized_telemetry=False))
            name = "articles"
            if name in [c.name for c in client.list_collections()]:
                self._collection = client.get_collection(name)
            else:
                self._collection = client.create_collection(name)
        except Exception:
            self._collection = None
            self._mem_store = {}

    def add(self, ids: List[str], documents: List[str], metadatas: List[Dict[str, Any]]):
        if self._collection is not None:
            embeddings = self.embedder.embed(documents)
            self._collection.add(ids=ids, embeddings=embeddings, metadatas=metadatas, documents=documents)
        else:
            for i, d, m in zip(ids, documents, metadatas):
                self._mem_store[i] = {"doc": d, "meta": m}

    def query(self, text: str, top_k: int = 10) -> List[Dict[str, Any]]:
        if self._collection is not None:
            q = self._collection.query(query_embeddings=self.embedder.embed([text]), n_results=top_k)
            out = []
            for i in range(len(q["ids"][0])):
                out.append({
                    "id": q["ids"][0][i],
                    "distance": q.get("distances", [[0]])[0][i] if q.get("distances") else 0.0,
                    "document": q["documents"][0][i],
                    "metadata": q["metadatas"][0][i],
                })
            return out
        scored = []
        for i, v in self._mem_store.items():
            scored.append({"id": i, "distance": 0.0, "document": v["doc"], "metadata": v["meta"]})
        return scored[:top_k]
