import redis.asyncio as redis
from typing import Dict, Any, Optional, List
from app.config import settings

class RedisService:
    def __init__(self):
        self.pool = redis.ConnectionPool(
            host=settings.redis_host, 
            port=settings.redis_port, 
            decode_responses=True
        )

    async def get_features_for_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        async with redis.Redis(connection_pool=self.pool) as r:
            is_active = await r.sismember("all_users", user_id)
            if not is_active:
                return None
            
            features = await r.hgetall(f"user:{user_id}:features")
            
            # Convert numeric strings to floats
            for k, v in features.items():
                if k in ["age", "purchase_count_30d", "avg_session_duration_min"]:
                    features[k] = float(v)
            return features

    async def get_batch_features(self, user_ids: List[str]) -> List[Dict[str, Any]]:
        async with redis.Redis(connection_pool=self.pool) as r:
            pipe = r.pipeline()
            for uid in user_ids:
                pipe.hgetall(f"user:{uid}:features")
            
            raw_results = await pipe.execute()
            
            final_results = []
            for idx, features in enumerate(raw_results):
                processed_features = {}
                # Ensure data types are correct (floats)
                for k, v in features.items():
                    if k in ["age", "purchase_count_30d", "avg_session_duration_min"]:
                        processed_features[k] = float(v)
                    else:
                        processed_features[k] = v
                
                final_results.append({
                    "user_id": user_ids[idx],
                    "features": processed_features
                })
            return final_results