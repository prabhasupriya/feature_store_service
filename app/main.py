from fastapi import FastAPI
from app.api.endpoints import router as api_router

app = FastAPI(title="Real-Time Feature Store")

app.include_router(api_router)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}