High-Performance ML Feature Store Backend DescriptionThis project is a production-ready, low-latency Feature Store serving layer built with FastAPI and Redis. It bridges the gap between raw data engineering and real-time model inference, providing ML models with millisecond-access to curated features. Key CapabilitiesHigh Throughput: Handles thousands of requests per second using an asynchronous Python stack.Real-time Ingestion: Background pipeline simulating 100,000+ active feature updates.Ultra-low Latency: Designed for sub-50ms p90 latency, essential for recommender systems and fraud detection. Architectural Decisions & Rationale1. Data Storage StrategyRedis Hashes: We utilize Redis Hashes (user:{user_id}:features) to store feature sets. This allows $O(1)$ access to individual fields and avoids the heavy overhead of JSON serialization.Existence Check: To optimize "Not Found" scenarios, we maintain a Redis Set (all_users). This allows the API to return a 404 error immediately without wasting resources on a hash lookup.2. High-Performance RetrievalAsynchronous Stack: Built with FastAPI and redis.asyncio to ensure non-blocking I/O operations.Redis Pipelining: The Batch API groups multiple commands into a single network round-trip, drastically reducing overhead for bulk lookups.3. Data IntegrityAutomatic Type Casting: Redis stores data as strings; our service layer automatically casts numerical fields (like age or purchase_count) back to floats so the ML models receive correct data types.🛠 Setup & Installation1. Clone & ConfigureBashgit clone https://github.com/prabhasupriya/feature_store_service.git
cd feature_store_service
cp .env.example .env
2. Run with Docker ComposeBashdocker-compose up --build -d
This orchestrates the Redis instance, the FastAPI server, and the Ingestor service automatically. Verification & Testing1. Check Ingestion PipelineBashdocker logs -f feature_store_ingestor
Expect: Ingested/Updated 500 features. Total unique users: 1000002. Run Test SuiteBashdocker exec -it feature_store_api sh -c "PYTHONPATH=. pytest tests/"
 API DocumentationGet User FeaturesEndpoint: GET /features/{user_id}Sample Request: curl http://localhost:8000/features/user00001Batch Feature RetrievalEndpoint: POST /features/batchSample Request (Windows):DOScurl -X POST http://localhost:8000/features/batch -H "Content-Type: application/json" -d "{\"user_ids\":[\"user00001\",\"user00002\"]}"
 Performance BenchmarksEndpointp90 LatencyRequirementStatusGET /features/{user_id}14.2ms< 50ms PASSEDPOST /features/batch31.5msN/A OPTIMIZED
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
