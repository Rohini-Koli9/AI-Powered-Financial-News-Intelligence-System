from fastapi import FastAPI
import asyncio
import logging
from .config import settings
from .api.routes import router as api_router
from .services.database import Database
from .services.embedding_service import EmbeddingService
from .services.vector_db import VectorDB
from .services.ner_service import NERService
from .services.llm_service import LLMService
from .graph.workflow import build_news_processing_graph, build_query_graph


def create_app() -> FastAPI:
    app = FastAPI(title="Financial News Intelligence", version="0.1.0")

    db = Database(settings.db_path)
    embedder = EmbeddingService(settings.embedding_model)
    vectordb = VectorDB(settings.vector_db_path, embedder)
    ner = NERService()
    llm = LLMService(settings.llm_provider)

    news_graph = build_news_processing_graph(db, vectordb, embedder, ner)
    query_graph = build_query_graph(db, vectordb, embedder, ner, llm)

    app.state.db = db
    app.state.embedder = embedder
    app.state.vectordb = vectordb
    app.state.ner = ner
    app.state.llm = llm
    app.state.news_graph = news_graph
    app.state.query_graph = query_graph

    app.include_router(api_router, prefix="/api/v1")
    logger = logging.getLogger("rss_poller")

    async def _rss_poller():
        interval = max(5, int(settings.rss_poll_interval_sec))
        while True:
            try:
                app.state.news_graph.invoke({"mode": "ingest_rss"})
            except Exception:
                logger.exception("RSS poller run failed")
            await asyncio.sleep(interval)

    async def _on_startup():
        if settings.rss_poll_enabled:
            app.state._rss_poller_task = asyncio.create_task(_rss_poller())

    async def _on_shutdown():
        task = getattr(app.state, "_rss_poller_task", None)
        if task:
            task.cancel()
            try:
                await task
            except Exception:
                pass

    app.add_event_handler("startup", _on_startup)
    app.add_event_handler("shutdown", _on_shutdown)
    return app


app = create_app()
