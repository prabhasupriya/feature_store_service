import pytest
from app.services.redis_service import RedisService
from unittest.mock import AsyncMock, patch, MagicMock
import redis.asyncio as redis

@pytest.mark.asyncio
async def test_redis_logic():
    service = RedisService()
    mock_redis_instance = AsyncMock()
    mock_redis_instance.sismember.return_value = True
    mock_redis_instance.hgetall.return_value = {"age": "30"}

    with patch("redis.asyncio.Redis") as mock_redis_class:
        mock_redis_class.return_value.__aenter__.return_value = mock_redis_instance
        result = await service.get_features_for_user("user1")
        assert result is not None
        assert result["age"] == 30.0

@pytest.mark.asyncio
async def test_batch_logic():
    service = RedisService()
    mock_redis_instance = AsyncMock()
    mock_pipe = MagicMock()
    
    # Force pipeline() to return a mock object, not a coroutine
    mock_redis_instance.pipeline = MagicMock(return_value=mock_pipe)
    # Mock the execution result
    mock_pipe.execute = AsyncMock(return_value=[{"age": "25"}, {"age": "40"}])

    with patch("redis.asyncio.Redis") as mock_redis_class:
        mock_redis_class.return_value.__aenter__.return_value = mock_redis_instance
        
        result = await service.get_batch_features(["user1", "user2"])
        
        assert len(result) == 2
        assert result[0]["user_id"] == "user1"
        # Expecting float 25.0 because of our service logic
        assert result[0]["features"]["age"] == 25.0