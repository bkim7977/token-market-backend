"""
Minimal Railway test API
Just to verify deployment works
"""

from fastapi import FastAPI
import os

app = FastAPI(title="Railway Test", version="1.0.0")

@app.get("/")
async def root():
    return {
        "message": "Railway deployment test",
        "status": "working",
        "environment": os.getenv("ENVIRONMENT", "unknown")
    }

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": "minimal-test"
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
