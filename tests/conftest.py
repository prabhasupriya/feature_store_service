import pytest
import asyncio
from unittest.mock import MagicMock
from app.services.redis_service import RedisService

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
def mock_redis_service():
    """
    Provides a mocked RedisService to avoid 
    actual database connections during unit tests.
    """
    service = MagicMock(spec=RedisService)
    return service

@pytest.fixture
def sample_feature_data():
    """Returns a standard feature set for testing consistency."""
    return {
        "age": 30.0,
        "gender": "female",
        "purchase_count_30d": 5.0,
        "preferred_category": "electronics"
    }