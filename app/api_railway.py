"""
Railway-optimized FastAPI application
Handles missing database connections gracefully for health checks
"""

from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
from typing import List, Optional
import logging
import os

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI app
app = FastAPI(title="Token Market Backend", version="1.0.0")
security = HTTPBearer()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import database services with error handling
db_service = None
try:
    from app.db_service import db_service
    from app.auth import extract_user_id_from_token
    DATABASE_AVAILABLE = True
    logger.info("Database services loaded successfully")
except Exception as e:
    logger.warning(f"Database services not available: {e}")
    DATABASE_AVAILABLE = False

# Pydantic Models
class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class CollectibleCreate(BaseModel):
    name: str
    type: str
    set_name: str
    rarity: str
    edition: Optional[str] = None
    metadata: Optional[dict] = None
    image_url: Optional[str] = None
    current_price: float

class TransactionCreate(BaseModel):
    collectible_id: Optional[str] = None
    transaction_type: str
    amount: float
    description: str

# Authentication dependency
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Extract user from JWT token"""
    if not DATABASE_AVAILABLE:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database service unavailable"
        )
    
    try:
        token = credentials.credentials
        user_id = extract_user_id_from_token(token)
        
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return {"user_id": user_id}
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

# Health and Status Endpoints (Always Available)
@app.get("/")
async def root():
    return {
        "message": "Token Market Backend API",
        "version": "1.0.0",
        "database_status": "available" if DATABASE_AVAILABLE else "unavailable",
        "environment": os.getenv("ENVIRONMENT", "development")
    }

@app.get("/health")
async def health_check():
    """Health check endpoint for deployment platforms"""
    return {
        "status": "healthy",
        "message": "Token Market Backend is running",
        "version": "1.0.0",
        "database_available": DATABASE_AVAILABLE,
        "timestamp": str(datetime.now()) if 'datetime' in globals() else "unknown"
    }

@app.get("/status")
async def status_check():
    """Detailed status endpoint"""
    return {
        "service": "token-market-backend",
        "status": "running",
        "database_available": DATABASE_AVAILABLE,
        "environment": os.getenv("ENVIRONMENT", "development"),
        "debug": os.getenv("DEBUG", "false"),
        "features": {
            "authentication": DATABASE_AVAILABLE,
            "user_management": DATABASE_AVAILABLE,
            "collectibles": DATABASE_AVAILABLE,
            "transactions": DATABASE_AVAILABLE
        }
    }

# Public Endpoints (Database Required)
@app.get("/collectibles", response_model=List[dict])
async def get_collectibles():
    """Get all collectibles (public access)"""
    if not DATABASE_AVAILABLE:
        return []  # Return empty list instead of error
    
    try:
        collectibles = db_service.get_all_collectibles()
        return collectibles
    except Exception as e:
        logger.error(f"Error fetching collectibles: {e}")
        return []

@app.get("/collectibles/{collectible_id}")
async def get_collectible(collectible_id: str):
    """Get specific collectible (public access)"""
    if not DATABASE_AVAILABLE:
        raise HTTPException(
            status_code=503,
            detail="Database service unavailable"
        )
    
    collectible = db_service.get_collectible_by_id(collectible_id)
    if not collectible:
        raise HTTPException(status_code=404, detail="Collectible not found")
    return collectible

# Authentication Endpoints (Database Required)
@app.post("/auth/register")
async def register_user(user_data: UserCreate):
    """Register new user with JWT authentication"""
    if not DATABASE_AVAILABLE:
        raise HTTPException(
            status_code=503,
            detail="Database service unavailable - registration disabled"
        )
    
    result = await db_service.create_user_with_jwt(
        email=user_data.email,
        password=user_data.password,
        username=user_data.username
    )
    
    if result["success"]:
        return {
            "message": "User created successfully",
            "access_token": result["access_token"],
            "token_type": result["token_type"],
            "user": {
                "id": result["user"]["id"],
                "email": result["user"]["email"],
                "username": result["user"]["username"]
            }
        }
    else:
        raise HTTPException(
            status_code=400,
            detail=result["error"]
        )

@app.post("/auth/login")
async def login_user(login_data: UserLogin):
    """Login user and return JWT token"""
    if not DATABASE_AVAILABLE:
        raise HTTPException(
            status_code=503,
            detail="Database service unavailable - login disabled"
        )
    
    result = await db_service.authenticate_user_with_jwt(
        email=login_data.email,
        password=login_data.password
    )
    
    if result["success"]:
        return {
            "message": "Login successful",
            "access_token": result["access_token"],
            "token_type": result["token_type"],
            "user": result["user"]
        }
    else:
        raise HTTPException(
            status_code=401,
            detail=result["error"]
        )

# Import datetime for timestamps
try:
    from datetime import datetime
except ImportError:
    pass

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
