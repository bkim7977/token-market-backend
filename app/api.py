"""
Production-Ready FastAPI Endpoints with RLS Security
Example endpoints for the Token Market Backend
"""

from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from app.db_service import DatabaseService
from app.auth import extract_user_id_from_token

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from app.db_service import db_service
import jwt

app = FastAPI(title="Token Market Backend", version="1.0.0")
security = HTTPBearer()

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

# Public Endpoints (No Authentication Required)
@app.get("/")
async def root():
    return {"message": "Token Market Backend API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    """Health check endpoint for deployment platforms"""
    return {
        "status": "healthy",
        "message": "Token Market Backend is running",
        "version": "1.0.0"
    }

@app.get("/collectibles", response_model=List[dict])
async def get_collectibles():
    """Get all collectibles (public access)"""
    collectibles = db_service.get_all_collectibles()
    return collectibles

@app.get("/collectibles/{collectible_id}")
async def get_collectible(collectible_id: str):
    """Get specific collectible (public access)"""
    collectible = db_service.get_collectible_by_id(collectible_id)
    if not collectible:
        raise HTTPException(status_code=404, detail="Collectible not found")
    return collectible

@app.get("/collectibles/{collectible_id}/price-history")
async def get_price_history(collectible_id: str):
    """Get price history for collectible (public access)"""
    history = db_service.get_price_history(collectible_id)
    return history

# Authentication Endpoints
@app.post("/auth/register")
async def register_user(user_data: UserCreate):
    """Register new user with JWT authentication"""
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

# Protected Endpoints (Authentication Required)
@app.get("/profile/balance")
async def get_user_balance(current_user: dict = Depends(get_current_user)):
    """Get current user's token balance"""
    balance = db_service.get_user_balance(current_user["user_id"])
    if not balance:
        raise HTTPException(status_code=404, detail="Balance not found")
    return balance

@app.put("/profile/balance/{new_balance}")
async def update_balance(new_balance: float, current_user: dict = Depends(get_current_user)):
    """Update user's balance"""
    success = db_service.update_user_balance(current_user["user_id"], new_balance)
    if success:
        return {"message": "Balance updated successfully"}
    else:
        raise HTTPException(status_code=400, detail="Failed to update balance")

@app.get("/profile/transactions")
async def get_user_transactions(current_user: dict = Depends(get_current_user)):
    """Get current user's transactions"""
    transactions = db_service.get_user_transactions(current_user["user_id"])
    return transactions

@app.post("/transactions")
async def create_transaction(
    transaction_data: TransactionCreate,
    current_user: dict = Depends(get_current_user)
):
    """Create new transaction"""
    transaction_dict = transaction_data.dict()
    transaction_dict["user_id"] = current_user["user_id"]
    
    transaction = db_service.create_transaction(transaction_dict)
    if transaction:
        return {"message": "Transaction created", "transaction": transaction}
    else:
        raise HTTPException(status_code=400, detail="Failed to create transaction")

@app.get("/profile/referrals")
async def get_user_referrals(current_user: dict = Depends(get_current_user)):
    """Get user's referrals"""
    referrals = db_service.get_user_referrals(current_user["user_id"])
    return referrals

@app.get("/profile/redemptions")
async def get_user_redemptions(current_user: dict = Depends(get_current_user)):
    """Get user's redemptions"""
    redemptions = db_service.get_user_redemptions(current_user["user_id"])
    return redemptions

@app.post("/collectibles")
async def create_collectible(
    collectible_data: CollectibleCreate,
    current_user: dict = Depends(get_current_user)
):
    """Create new collectible (authenticated users only)"""
    collectible_dict = collectible_data.dict()
    collectible = db_service.create_collectible(collectible_dict)
    
    if collectible:
        return {"message": "Collectible created", "collectible": collectible}
    else:
        raise HTTPException(status_code=400, detail="Failed to create collectible")

@app.post("/collectibles/{collectible_id}/price")
async def update_price(
    collectible_id: str,
    price: float,
    current_user: dict = Depends(get_current_user)
):
    """Update collectible price (authenticated users only)"""
    success = db_service.add_price_record(collectible_id, price)
    
    if success:
        return {"message": "Price updated successfully"}
    else:
        raise HTTPException(status_code=400, detail="Failed to update price")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
