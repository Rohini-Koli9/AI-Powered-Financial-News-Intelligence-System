# Architecture

## Overview
The system comprises 6 LangGraph agents connected into two workflows: News Processing and Query. Storage is backed by SQLite; embeddings are indexed in ChromaDB for semantic RAG. Entities and relationships enable context-aware retrieval.

## Agents
- News Ingestion Agent: Fetches/normalizes RSS and mock data.
- Deduplication Agent: Embeds, finds near-duplicates (cosine > 0.85), consolidates.
- Entity Extraction Agent: spaCy NER + normalization (e.g., Reserve Bank -> RBI).
- Stock Impact Analysis Agent: Maps entities to NSE/BSE symbols with confidence.
- Storage & Indexing Agent: Persists articles and entities; updates ChromaDB and inverted indexes.
- Query Processing Agent: Parses NL queries, expands context, hybrid search, ranks, explains.

## Workflows
1) News Processing: ingest -> deduplicate -> extract_entities -> analyze_impact -> store
2) Query: parse_query -> expand_context -> search -> rank -> explain

## Data Model
- Article(id, title, content, source, published_at, url, category, embedding, metadata)
- Entity(id, type, name, normalized)
- StockImpact(article_id, symbol, confidence, type)

## Vector Index
- Sentence-transformers all-MiniLM-L6-v2
- ChromaDB collection: articles

## API
FastAPI routes under /api/v1 supporting ingestion, processing, queries, entities, sectors, stocks, health, stats.

## Testing
- Unit tests for deduplication, entity extraction, query system
- Integration tests for pipeline + API

