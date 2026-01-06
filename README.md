# 🚀 AI-Powered Financial News Intelligence System

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![LangGraph](https://img.shields.io/badge/LangGraph-Multi--Agent-orange.svg)](https://langchain-ai.github.io/langgraph/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

> 🧠 **Transform financial news into actionable intelligence with advanced AI agents**

An end-to-end, LangGraph-powered multi-agent system that processes real-time financial news through intelligent deduplication, entity extraction, stock impact mapping, and hybrid semantic search. Built for financial analysts, traders, and researchers who need instant insights from market news.

## ✨ Key Features

### 🤖 **Multi-Agent Intelligence**
- **News Ingestion Agent**: Automatically fetches and normalizes RSS feeds and mock data
- **Deduplication Agent**: Eliminates duplicate content using advanced embedding similarity
- **Entity Extraction Agent**: Identifies companies, sectors, regulators, people, and events
- **Stock Impact Analysis Agent**: Maps news to stock symbols with confidence scoring
- **Storage & Indexing Agent**: Manages data persistence across SQLite and ChromaDB
- **Query Processing Agent**: Delivers intelligent search with context expansion

### 🔍 **Advanced Search Capabilities**
- **Semantic Search**: Find related content using sentence-transformer embeddings
- **Entity-Based Search**: Query by company names, stock symbols, or sectors
- **Hybrid Search**: Combine semantic and entity-based approaches for optimal results
- **Context Expansion**: Automatically broaden search scope with related entities

### 📊 **Real-Time Processing**
- **Automatic RSS Polling**: Continuous news ingestion from configured feeds
- **Live API**: RESTful endpoints for integration with external systems
- **Interactive Demos**: Both CLI and Streamlit web interfaces

## 🛠 Tech Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Agent Framework** | 🦜 LangGraph | Multi-agent workflow orchestration |
| **Embeddings** | 🔄 sentence-transformers (all-MiniLM-L6-v2) | Semantic similarity and search |
| **Vector Database** | 🗃️ ChromaDB | High-performance vector storage and retrieval |
| **Structured Database** | 🗄️ SQLite | Article metadata and entity relationships |
| **NER Processing** | 🧠 spaCy (en_core_web_lg) | Named entity recognition and normalization |
| **API Framework** | ⚡ FastAPI + Uvicorn | High-performance REST API |
| **Web Interface** | 🌊 Streamlit | Interactive demo and visualization |
| **Python Version** | 🐍 3.10+ | Core runtime environment |

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- Git (for cloning)
- Basic command-line familiarity

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Rohini-Koli9/AI-Powered-Financial-News-Intelligence-System.git
   cd AI-Powered-Financial-News-Intelligence-System
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # macOS/Linux
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Download spaCy language model**
   ```bash
   python -m spacy download en_core_web_lg
   ```

5. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

### Running the System

#### 🌐 Start the API Server
```bash
uvicorn src.main:app --reload --port 8000
```
**Health Check**: `GET http://localhost:8000/api/v1/health`

#### 🎯 Quick Demo with Mock Data
```bash
# Ingest sample financial news
python demo/cli_demo.py ingest-mock

# Query the system
python demo/cli_demo.py query "HDFC Bank news"
python demo/cli_demo.py query "Reserve Bank of India policy"
python demo/cli_demo.py query "IT sector stocks"
```

#### 🌊 Interactive Web Interface
```bash
# Set Python path for module discovery
export PYTHONPATH="."  # macOS/Linux
$env:PYTHONPATH = "."  # Windows PowerShell

# Launch Streamlit demo
streamlit run demo/web_demo.py
```
Visit `http://localhost:8501` for the interactive interface.

## 📖 Usage Examples

### CLI Commands
```bash
# Ingest real RSS feeds
python demo/cli_demo.py ingest-rss

# Search with custom parameters
python demo/cli_demo.py query "banking sector" --top_k 15

# View system statistics
python demo/cli_demo.py stats

# List all extracted entities
python demo/cli_demo.py entities

# View specific article details
python demo/cli_demo.py article <article_id>
```

### API Endpoints
```bash
# Health check
curl http://localhost:8000/api/v1/health

# Search news
curl "http://localhost:8000/api/v1/search?q=HDFC%20Bank&top_k=10"

# Get statistics
curl http://localhost:8000/api/v1/stats

# List entities
curl http://localhost:8000/api/v1/entities
```

## 🏗 System Architecture

### Agent Workflows

**📰 News Processing Pipeline**
```
RSS/Mock Data → Deduplication → Entity Extraction → Stock Impact Analysis → Storage
```

**🔍 Query Processing Pipeline**
```
User Query → Context Expansion → Hybrid Search → Ranking → Explanation
```

### Data Flow
1. **Ingestion**: News articles are fetched from RSS feeds or mock data sources
2. **Deduplication**: Similar articles are identified and consolidated using cosine similarity (>0.85)
3. **Entity Extraction**: spaCy identifies and normalizes entities (companies, people, sectors, events)
4. **Impact Analysis**: Entities are mapped to stock symbols with confidence scores
5. **Indexing**: Articles are stored in SQLite, embeddings in ChromaDB
6. **Query Processing**: Natural language queries are expanded and searched using hybrid approach

## 🧪 Testing

```bash
# Run all tests
pytest -q

# Run specific test categories
pytest tests/test_deduplication.py
pytest tests/test_entity_extraction.py
pytest tests/test_query_system.py
pytest tests/test_api.py
```

## 📁 Project Structure

```
financial-news-intelligence/
├── src/                    # Core application code
│   ├── agents/            # LangGraph agent implementations
│   ├── api/               # FastAPI routes and endpoints
│   ├── graph/             # Workflow definitions
│   ├── models/            # Data models and schemas
│   ├── services/          # Business logic services
│   └── utils/             # Utility functions
├── demo/                  # Demo applications
│   ├── cli_demo.py       # Command-line interface
│   └── web_demo.py       # Streamlit web interface
├── data/                  # Configuration and reference data
│   ├── mock_news.json    # Sample news articles
│   ├── stock_mappings.json # Stock symbol mappings
│   └── sector_hierarchy.json # Industry sector definitions
├── tests/                 # Test suite
├── docs/                  # Documentation
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── README.md             # This file
└── ARCHITECTURE.md        # Detailed technical architecture
```

## 🔧 Configuration

### Environment Variables (.env)
```bash
# Environment
ENVIRONMENT=development

# Database paths
DB_PATH=./data/news.db
VECTOR_DB_PATH=./data/vector_store

# Model configurations
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
LLM_PROVIDER=none  # Can be: openai, anthropic, none

# API Keys (if using LLM provider)
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key

# RSS polling
RSS_POLL_ENABLED=true
RSS_POLL_INTERVAL_SEC=300  # 5 minutes
```

## 🎯 Use Cases

### 👨‍💼 For Financial Analysts
- **Market Monitoring**: Track news affecting specific stocks or sectors
- **Competitive Intelligence**: Monitor competitor mentions and developments
- **Regulatory Tracking**: Stay updated on regulatory changes and announcements

### 📈 For Traders
- **Event Detection**: Identify market-moving news in real-time
- **Sentiment Analysis**: Gauge market sentiment through news aggregation
- **Risk Assessment**: Monitor news affecting portfolio holdings

### 🔬 For Researchers
- **Trend Analysis**: Study news patterns and entity relationships
- **Event Studies**: Analyze market reactions to specific news events
- **Data Mining**: Extract structured data from unstructured news

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **LangChain Team** for the excellent LangGraph framework
- **spaCy** for powerful NER capabilities
- **Sentence Transformers** for high-quality embeddings
- **ChromaDB** for efficient vector storage

## 📞 Support

- 📧 Email: [your-email@example.com]
- 🐛 Issues: [GitHub Issues](https://github.com/Rohini-Koli9/AI-Powered-Financial-News-Intelligence-System/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/Rohini-Koli9/AI-Powered-Financial-News-Intelligence-System/discussions)

---

⭐ **If this project helps you, please give it a star on GitHub!**
