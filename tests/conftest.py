import os
import pytest
from src.main import create_app


@pytest.fixture(scope="session")
def app():
    os.environ.setdefault("DB_PATH", "./data/test_news.db")
    os.environ.setdefault("VECTOR_DB_PATH", "./data/test_vector_store")
    return create_app()
