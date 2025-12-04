from .state import NewsProcessingState, QueryState
from ..agents.news_ingestion import NewsIngestionAgent
from ..agents.deduplication import DeduplicationAgent
from ..agents.entity_extraction import EntityExtractionAgent
from ..agents.stock_impact import StockImpactAgent
from ..agents.storage_indexing import StorageIndexingAgent
from ..agents.query_processing import QueryProcessingAgent


def ingest_node(ctx):
    agent = NewsIngestionAgent()
    def _run(state: NewsProcessingState) -> NewsProcessingState:
        return agent.run(state)
    return _run


def dedup_node(ctx):
    agent = DeduplicationAgent(embedder=ctx["embedder"]) 
    def _run(state: NewsProcessingState) -> NewsProcessingState:
        return agent.run(state)
    return _run


def entity_node(ctx):
    agent = EntityExtractionAgent(ner=ctx["ner"]) 
    def _run(state: NewsProcessingState) -> NewsProcessingState:
        return agent.run(state)
    return _run


def impact_node(ctx):
    agent = StockImpactAgent(data_dir="data")
    def _run(state: NewsProcessingState) -> NewsProcessingState:
        return agent.run(state)
    return _run


def store_node(ctx):
    agent = StorageIndexingAgent(db=ctx["db"], vectordb=ctx["vectordb"], embedder=ctx["embedder"]) 
    def _run(state: NewsProcessingState) -> NewsProcessingState:
        return agent.run(state)
    return _run


def query_node(ctx):
    agent = QueryProcessingAgent(db=ctx["db"], vectordb=ctx["vectordb"], ner=ctx["ner"], llm=ctx["llm"]) 
    def _run(state: QueryState) -> QueryState:
        return agent.run(state)
    return _run
