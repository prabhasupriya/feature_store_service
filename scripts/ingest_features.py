import redis
import random
import time
import os

r = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    decode_responses=True
)

def ingest():
    print("Starting ingestion of 100,000 features...")
    pipe = r.pipeline()
    for i in range(100000):
        user_id = f"user{i:05d}"
        features = {
            "age": random.randint(18, 70),
            "purchase_count_30d": random.randint(0, 50),
            "preferred_category": random.choice(["tech", "fashion", "food"])
        }
        pipe.hset(f"user:{user_id}:features", mapping=features)
        pipe.sadd("all_users", user_id)
        
        # Batch execute every 1000 items for performance
        if i % 1000 == 0:
            pipe.execute()
            print(f"Progress: {i}/100000")
    
    pipe.execute()
    print("Ingestion complete.")

if __name__ == "__main__":
    ingest()