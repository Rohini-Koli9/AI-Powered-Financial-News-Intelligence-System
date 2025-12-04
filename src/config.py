import os
from pydantic import BaseModel


class Settings(BaseModel):
    environment: str = os.getenv("ENVIRONMENT", "development")
    db_path: str = os.getenv("DB_PATH", "./data/news.db")
    vector_db_path: str = os.getenv("VECTOR_DB_PATH", "./data/vector_store")
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
    llm_provider: str = os.getenv("LLM_PROVIDER", "none")
    openai_api_key: str | None = os.getenv("OPENAI_API_KEY")
    anthropic_api_key: str | None = os.getenv("ANTHROPIC_API_KEY")
    rss_poll_enabled: bool = os.getenv("RSS_POLL_ENABLED", "false").lower() in ("1", "true", "yes", "on")
    rss_poll_interval_sec: int = int(os.getenv("RSS_POLL_INTERVAL_SEC", "600"))


settings = Settings()
