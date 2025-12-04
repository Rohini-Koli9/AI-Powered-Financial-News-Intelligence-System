import sqlite3
from typing import Any, Dict, List, Optional
import os
import json
import ast


class Database:
    def __init__(self, path: str):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        self.conn = sqlite3.connect(path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self._init()

    def _init(self):
        cur = self.conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS articles (
            id TEXT PRIMARY KEY,
            title TEXT,
            content TEXT,
            source TEXT,
            published_at TEXT,
            url TEXT,
            category TEXT,
            metadata TEXT
        );
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS entities (
            id TEXT PRIMARY KEY,
            type TEXT,
            name TEXT,
            normalized TEXT
        );
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS article_entities (
            article_id TEXT,
            entity_id TEXT
        );
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS stock_impacts (
            article_id TEXT,
            symbol TEXT,
            confidence REAL,
            type TEXT
        );
        """)
        self.conn.commit()

    def upsert_article(self, article: Dict[str, Any]):
        cur = self.conn.cursor()
        cur.execute(
            """INSERT OR REPLACE INTO articles (id, title, content, source, published_at, url, category, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                article["id"], article["title"], article["content"], article["source"],
                article["published_at"], article["url"], article.get("category"), str(article.get("metadata"))
            )
        )
        self.conn.commit()

    def get_article(self, article_id: str) -> Optional[Dict[str, Any]]:
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM articles WHERE id = ?", (article_id,))
        row = cur.fetchone()
        if not row:
            return None
        d = dict(row)
        d["metadata"] = self._deserialize_metadata(d.get("metadata"))
        return d

    def list_entities(self) -> List[Dict[str, Any]]:
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM entities")
        return [dict(r) for r in cur.fetchall()]

    def link_article_entities(self, article_id: str, entities: List[Dict[str, Any]]):
        cur = self.conn.cursor()
        for e in entities:
            cur.execute("INSERT OR REPLACE INTO entities (id, type, name, normalized) VALUES (?, ?, ?, ?)",
                        (e["id"], e["type"], e["name"], e.get("normalized")))
            cur.execute("INSERT INTO article_entities (article_id, entity_id) VALUES (?, ?)", (article_id, e["id"]))
        self.conn.commit()

    def add_stock_impacts(self, impacts: List[Dict[str, Any]]):
        cur = self.conn.cursor()
        for i in impacts:
            cur.execute("INSERT INTO stock_impacts (article_id, symbol, confidence, type) VALUES (?, ?, ?, ?)",
                        (i["article_id"], i["symbol"], i["confidence"], i["type"]))
        self.conn.commit()

    def list_news_by_stock(self, symbol: str, limit: int = 20) -> List[Dict[str, Any]]:
        cur = self.conn.cursor()
        cur.execute(
            """
            SELECT a.* FROM articles a
            JOIN stock_impacts s ON a.id = s.article_id
            WHERE s.symbol = ?
            ORDER BY a.published_at DESC
            LIMIT ?
            """, (symbol, limit)
        )
        return [dict(r) for r in cur.fetchall()]

    def list_news_by_sector(self, sector: str, limit: int = 20) -> List[Dict[str, Any]]:
        cur = self.conn.cursor()
        cur.execute(
            """
            SELECT DISTINCT a.* FROM articles a
            JOIN entities e ON e.id IN (
                SELECT entity_id FROM article_entities WHERE article_id = a.id
            )
            WHERE (e.type = 'SECTOR' AND LOWER(e.name) = LOWER(?))
               OR (a.category IS NOT NULL AND LOWER(a.category) = LOWER(?))
            ORDER BY a.published_at DESC
            LIMIT ?
            """, (sector, sector, limit)
        )
        return [dict(r) for r in cur.fetchall()]

    def list_news_by_entity(self, entity_type: str, name_or_normalized: str, limit: int = 20) -> List[Dict[str, Any]]:
        cur = self.conn.cursor()
        cur.execute(
            """
            SELECT DISTINCT a.* FROM articles a
            JOIN article_entities ae ON a.id = ae.article_id
            JOIN entities e ON e.id = ae.entity_id
            WHERE e.type = ? AND (
                (e.normalized IS NOT NULL AND LOWER(e.normalized) = LOWER(?))
                OR (e.normalized IS NULL AND LOWER(e.name) = LOWER(?))
            )
            ORDER BY a.published_at DESC
            LIMIT ?
            """,
            (entity_type, name_or_normalized, name_or_normalized, limit)
        )
        return [dict(r) for r in cur.fetchall()]

    def list_news_by_company(self, company_name: str, limit: int = 20) -> List[Dict[str, Any]]:
        return self.list_news_by_entity("COMPANY", company_name, limit)

    def list_news_by_regulator(self, regulator_name: str, limit: int = 20) -> List[Dict[str, Any]]:
        return self.list_news_by_entity("REGULATOR", regulator_name, limit)

    def stats(self) -> Dict[str, Any]:
        cur = self.conn.cursor()
        cur.execute("SELECT COUNT(*) AS c FROM articles")
        articles = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) AS c FROM entities")
        entities = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) AS c FROM stock_impacts")
        stocks = cur.fetchone()[0]
        cur.execute("SELECT MAX(published_at) FROM articles")
        last = cur.fetchone()[0]
        return {"articles": articles, "entities": entities, "stocks": stocks, "duplicates": 0, "last_ingested_at": last}

    def _deserialize_metadata(self, value: Any) -> Optional[Dict[str, Any]]:
        if value is None:
            return None
        if isinstance(value, dict):
            return value
        if isinstance(value, str):
            v = value.strip()
            if v.lower() == "none" or v == "":
                return None
            try:
                return json.loads(v)
            except Exception:
                try:
                    return ast.literal_eval(v)
                except Exception:
                    return None
        return None
