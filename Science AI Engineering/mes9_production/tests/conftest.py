"""Configuration for pytest."""

import pytest
import os
from fastapi.testclient import TestClient


@pytest.fixture(scope="session")
def test_db():
    """Setup test database."""
    os.environ["DATABASE_URL"] = "sqlite:///./test.db"
    yield
    if os.path.exists("test.db"):
        os.remove("test.db")
