from fastapi import APIRouter, HTTPException, Body
from typing import List, Dict, Any
from pydantic import BaseModel, Field
from app.services.redis_service import RedisService

router = APIRouter()
redis_service = RedisService()

class UserIDList(BaseModel):
    user_ids: List[str] = Field(..., min_length=1, max_length=100)

@router.get("/features/{user_id}")
async def get_user_features(user_id: str):
    features = await redis_service.get_features_for_user(user_id)
    if features is None:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    return {"user_id": user_id, "features": features}

@router.post("/features/batch")
async def get_batch_features(payload: UserIDList = Body(...)):
    results = await redis_service.get_batch_features(payload.user_ids)
    return results