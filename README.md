# AI-Powered Financial News Intelligence System

An end-to-end, LangGraph-powered multi-agent system for real-time financial news intelligence: deduplication, entity extraction, stock impact mapping, hybrid search, and a query API.

## Features
- Intelligent deduplication using sentence-transformers embeddings + ChromaDB (RAG)
- Entity extraction via spaCy (companies, sectors, regulators, people, events)
- Stock impact mapping with confidence scores
- Hybrid semantic + entity search with context expansion
- LangGraph multi-agent workflows for processing and query
- FastAPI REST API with tests and demos (CLI + Streamlit)

## Tech Stack
- Agent framework: LangGraph
- Embeddings: sentence-transformers (all-MiniLM-L6-v2)
- Vector DB: ChromaDB
- Structured DB: SQLite (default)
- NER: spaCy (en_core_web_lg)
- API: FastAPI + Uvicorn
- Python: 3.10+

## Setup
1. Python 3.10+
2. Create and activate a virtualenv
3. Install dependencies:
   pip install -r requirements.txt
4. Optional: Download spaCy model:
   python -m spacy download en_core_web_lg
5. Copy .env.example to .env and set values as needed.

## Run API
uvicorn src.main:app --reload --port 8000

Health check:
GET http://localhost:8000/api/v1/health

## Quick Start (Local Data)
- Seed with mock data:
  python demo/cli_demo.py ingest-mock
- Query:
  python demo/cli_demo.py query "HDFC Bank news"

## Tests
pytest -q

## Project Structure
See ARCHITECTURE.md for diagrams and agent/workflow details.
