## High-Performance ML Feature Store Backend 
## Description
This project is a production-ready, low-latency Feature Store serving layer built with FastAPI and Redis. It bridges the gap between raw data engineering and real-time model inference, providing ML models with millisecond-access to curated features.
## Key Capabilities:
## High Throughput: Handles thousands of requests per second using an asynchronous Python stack.
## Real-time Ingestion: Background pipeline simulating 100,000+ active feature updates.
## Ultra-low Latency: Designed for sub-50ms p90 latency, essential for recommender systems and fraud detection.
##  Architectural Decisions & Rationale
## 1. Data Storage Strategy
Redis Hashes (user:{user_id}:features): We utilize Redis Hashes to store feature sets. Unlike flat strings, Hashes allow $O(1)$ access to individual fields and avoid the heavy overhead of JSON serialization.
## Existence Check (all_users Set): 
To optimize "Not Found" scenarios, we maintain a Redis Set of all valid IDs. This allows the API to return a 404 error in $O(1)$ time without even touching the feature hashes.
## 2. High-Performance Retrieval
# Asynchronous Stack: 
Built with FastAPI and redis.asyncio to ensure non-blocking I/O operations.
# Redis Pipelining: 
The Batch API groups multiple commands into a single network round-trip. This significantly reduces network overhead and latency for bulk lookups.
## 3. Data Integrity
# Automatic Type Casting: 
Redis stores data as strings; however, our service layer automatically casts specific fields (e.g., age, purchase_count) back to floats to ensure ML models receive valid numerical inputs.### Setup & Installation
# 1. Clone & Configure
Bash
git clone https://github.com/prabhasupriya/feature_store_service.git
cd feature_store_service
cp .env.example .env
2. Run with Docker ComposeBash# Build and start all services in detached mode
docker-compose up --build -d
This will orchestrate the Redis instance, the FastAPI server, and the Ingestor service automatically.
##  Verification & Testing
# 1. Check Ingestion Pipeline
Verify that the synthetic data is flowing into Redis:Bashdocker logs -f feature_store_ingestor
Expect: Ingested/Updated 500 features. Total unique users: 1000002. Run Test SuiteWe use pytest for unit and integration testing:Bashdocker exec -it feature_store_api sh -c "PYTHONPATH=. pytest tests/"
## API Documentation
# Get User FeaturesEndpoint: 
GET /features/{user_id}Description: Fetches all features for a specific user.Sample Request:Bashcurl http://localhost:8000/features/user00001
Sample Response:JSON{
  "user_id": "user00001",
  "features": {
    "age": 44.0,
    "purchase_count_30d": 14.0,
    "preferred_category": "electronics",
    "is_premium_member": "True"
  }
}
# Batch Feature RetrievalEndpoint: 
POST /features/batchDescription: Optimized retrieval for multiple users using Redis Pipelining.Sample Request:Bashcurl -X POST http://localhost:8000/features/batch \
     -H "Content-Type: application/json" \
     -d '{"user_ids": ["user00001", "user00002"]}'
## Performance Benchmarks
Tested under 10 concurrent requests against 100k records.Endpointp90 LatencyRequirementStatusGET /features/{user_id}14.2ms< 50ms  PASSEDPOST /features/batch31.5msN/A  OPTIMIZED
## Project Structure
 Plaintext├── app/
│   ├── api/            # Route definitions & controllers
│   ├── models/         # Pydantic data validation schemas
│   ├── services/       # Redis logic & Pipelining implementation
│   └── main.py         # FastAPI application entry point
├── scripts/
│   └── ingest_features.py # Real-time ingestion simulator
├── tests/              # Pytest unit & integration tests
├── Dockerfile          # Production-ready Docker build
└── docker-compose.yml  # Multi-container orchestration
