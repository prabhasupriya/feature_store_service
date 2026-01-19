import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_get_user_features_success():
    mock_features = {"age": 25.0, "gender": "male"}
    # Patch the service call in the endpoint
    with patch("app.api.endpoints.redis_service.get_features_for_user", new_callable=AsyncMock) as mock_get:
        mock_get.return_value = mock_features
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            response = await ac.get("/features/user123")
        
        assert response.status_code == 200
        assert response.json()["features"]["age"] == 25.0

@pytest.mark.asyncio
async def test_get_user_features_not_found():
    with patch("app.api.endpoints.redis_service.get_features_for_user", new_callable=AsyncMock) as mock_get:
        mock_get.return_value = None
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            response = await ac.get("/features/nonexistent")
        
        assert response.status_code == 404