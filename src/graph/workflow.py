from langgraph.graph import StateGraph, END
from .state import NewsProcessingState, QueryState
from .nodes import ingest_node, dedup_node, entity_node, impact_node, store_node, query_node


def build_news_processing_graph(db, vectordb, embedder, ner):
    ctx = {"db": db, "vectordb": vectordb, "embedder": embedder, "ner": ner}
    graph = StateGraph(NewsProcessingState)
    graph.add_node("ingest", ingest_node(ctx))
    graph.add_node("dedup", dedup_node(ctx))
    graph.add_node("entity", entity_node(ctx))
    graph.add_node("impact", impact_node(ctx))
    graph.add_node("store", store_node(ctx))

    graph.set_entry_point("ingest")
    graph.add_edge("ingest", "dedup")
    graph.add_edge("dedup", "entity")
    graph.add_edge("entity", "impact")
    graph.add_edge("impact", "store")
    graph.add_edge("store", END)

    return graph.compile()


def build_query_graph(db, vectordb, embedder, ner, llm):
    ctx = {"db": db, "vectordb": vectordb, "embedder": embedder, "ner": ner, "llm": llm}
    graph = StateGraph(QueryState)
    graph.add_node("query", query_node(ctx))
    graph.set_entry_point("query")
    graph.add_edge("query", END)
    return graph.compile()
