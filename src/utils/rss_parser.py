from typing import List, Dict
import os
import feedparser


DEFAULT_FEEDS = [
    "https://www.moneycontrol.com/rss/MCtopnews.xml",
    "https://economictimes.indiatimes.com/rssfeedsdefault.cms",
    "https://www.livemint.com/rss/markets",
]

_feeds_env = os.getenv("RSS_FEEDS")
RSS_FEEDS = [s.strip() for s in _feeds_env.split(",")] if _feeds_env else DEFAULT_FEEDS


def fetch_rss_articles() -> List[Dict]:
    items: List[Dict] = []
    for url in RSS_FEEDS:
        try:
            feed = feedparser.parse(url)
            for e in feed.entries[:50]:
                items.append({
                    "id": getattr(e, "id", getattr(e, "guid", getattr(e, "link", ""))),
                    "title": getattr(e, "title", ""),
                    "content": getattr(e, "summary", ""),
                    "source": feed.feed.get("title", url),
                    "published_at": getattr(e, "published", getattr(e, "updated", "")),
                    "url": getattr(e, "link", url),
                    "category": ""
                })
        except Exception:
            continue
    return items
