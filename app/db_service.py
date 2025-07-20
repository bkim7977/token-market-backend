"""
Database service module with production-ready RLS support
Handles authentication, user management, and secure data operations
"""

from app.database import supabase
from app.auth import get_password_hash, verify_password, create_access_token
from typing import Optional, List, Dict, Any
import uuid
from datetime import datetime

class DatabaseService:
    """Production-ready database service with RLS support"""
    
    def __init__(self):
        self.supabase = supabase
    
    # Authentication Methods
    def set_test_user_context(self, user_id: str):
        """Set user context for testing (simulates authentication)"""
        # For RLS to work, we need to set the user context
        # This simulates what happens when a user is authenticated
        try:
            self.current_user_id = user_id
            # Set the Supabase client to use this user context
            # Note: In a real app, this would be handled by JWT tokens
            return True
        except Exception as e:
            print(f"Error setting user context: {e}")
            return False

    async def create_test_user(self, email: str, password: str, username: str) -> Dict[str, Any]:
        """Create a test user without email confirmation (for testing only)"""
        try:
            # For testing, we'll create a user directly in the database
            # with a known UUID and bypass Supabase auth temporarily
            import uuid
            user_id = str(uuid.uuid4())
            
            # Create user profile directly
            profile_data = {
                "id": user_id,
                "email": email,
                "username": username,
                "password_hash": "test_password_hash"
            }
            
            profile_response = self.supabase.table("users").insert(profile_data).execute()
            
            if profile_response.data:
                # Create initial token balance
                balance_data = {
                    "user_id": user_id,
                    "balance": 0.00
                }
                self.supabase.table("token_balances").insert(balance_data).execute()
                
                return {
                    "success": True, 
                    "user": {"id": user_id, "email": email, "username": username},
                    "test_mode": True
                }
            
            return {"success": False, "error": "Failed to create test user profile"}
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def create_user_with_jwt(self, email: str, password: str, username: str) -> Dict[str, Any]:
        """Create a new user with JWT authentication (local database)"""
        try:
            # Check if user already exists
            existing_user = self.supabase.table("users").select("*").eq("email", email).execute()
            if existing_user.data:
                return {"success": False, "error": "User already exists"}
            
            # Hash password
            hashed_password = get_password_hash(password)
            user_id = str(uuid.uuid4())
            
            # Create user profile
            profile_data = {
                "id": user_id,
                "email": email,
                "username": username,
                "password_hash": hashed_password
            }
            
            profile_response = self.supabase.table("users").insert(profile_data).execute()
            
            if profile_response.data:
                # Create initial token balance
                balance_data = {
                    "user_id": user_id,
                    "balance": 0.00
                }
                self.supabase.table("token_balances").insert(balance_data).execute()
                
                # Generate JWT token
                access_token = create_access_token(data={"sub": user_id, "email": email})
                
                return {
                    "success": True, 
                    "user": profile_response.data[0],
                    "access_token": access_token,
                    "token_type": "bearer"
                }
            
            return {"success": False, "error": "Failed to create user profile"}
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def authenticate_user_with_jwt(self, email: str, password: str) -> Dict[str, Any]:
        """Authenticate user with email/password and return JWT token"""
        try:
            # Get user from database
            user_response = self.supabase.table("users").select("*").eq("email", email).execute()
            
            if not user_response.data:
                return {"success": False, "error": "User not found"}
            
            user = user_response.data[0]
            
            # Verify password
            if not verify_password(password, user["password_hash"]):
                return {"success": False, "error": "Invalid password"}
            
            # Generate JWT token
            access_token = create_access_token(data={"sub": user["id"], "email": email})
            
            return {
                "success": True,
                "access_token": access_token,
                "token_type": "bearer",
                "user": {
                    "id": user["id"],
                    "email": user["email"],
                    "username": user["username"]
                }
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def create_user(self, email: str, password: str, username: str) -> Dict[str, Any]:
        """Create a new user with authentication"""
        try:
            # Create auth user
            auth_response = self.supabase.auth.sign_up({
                "email": email,
                "password": password
            })
            
            if not auth_response.user:
                return {"success": False, "error": "Failed to create auth user"}
            
            user_id = auth_response.user.id
            
            # Create user profile (this will work because auth.uid() = id in policy)
            profile_data = {
                "id": user_id,
                "email": email,
                "username": username,
                "password_hash": "handled_by_auth"  # Supabase handles password hashing
            }
            
            profile_response = self.supabase.table("users").insert(profile_data).execute()
            
            if profile_response.data:
                # Create initial token balance
                balance_data = {
                    "user_id": user_id,
                    "balance": 0.00
                }
                self.supabase.table("token_balances").insert(balance_data).execute()
                
                return {
                    "success": True, 
                    "user": profile_response.data[0],
                    "auth_user": auth_response.user
                }
            
            return {"success": False, "error": "Failed to create user profile"}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def sign_in_user(self, email: str, password: str) -> Dict[str, Any]:
        """Sign in user"""
        try:
            auth_response = self.supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            
            if auth_response.user:
                return {
                    "success": True,
                    "user": auth_response.user,
                    "session": auth_response.session
                }
            
            return {"success": False, "error": "Invalid credentials"}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    # Collectible Methods (Public Read)
    def get_all_collectibles(self) -> List[Dict[str, Any]]:
        """Get all collectibles (public access)"""
        try:
            response = self.supabase.table("collectibles").select("*").execute()
            return response.data
        except Exception as e:
            print(f"Error fetching collectibles: {e}")
            return []
    
    def get_collectible_by_id(self, collectible_id: str) -> Optional[Dict[str, Any]]:
        """Get specific collectible (public access)"""
        try:
            response = self.supabase.table("collectibles").select("*").eq("id", collectible_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error fetching collectible: {e}")
            return None
    
    def create_collectible(self, collectible_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create new collectible (requires authentication)"""
        try:
            response = self.supabase.table("collectibles").insert(collectible_data).execute()
            if response.data:
                # Add to price history
                price_history_data = {
                    "collectible_id": response.data[0]["id"],
                    "price": collectible_data.get("current_price", 0)
                }
                self.supabase.table("price_history").insert(price_history_data).execute()
                
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error creating collectible: {e}")
            return None
    
    # User-specific Methods (RLS Protected)
    def get_user_balance(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user's token balance (user can only see their own)"""
        try:
            response = self.supabase.table("token_balances").select("*").eq("user_id", user_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error fetching balance: {e}")
            return None
    
    def update_user_balance(self, user_id: str, new_balance: float) -> bool:
        """Update user's balance (user can only update their own)"""
        try:
            response = self.supabase.table("token_balances").update({
                "balance": new_balance,
                "last_updated": datetime.now().isoformat()
            }).eq("user_id", user_id).execute()
            return len(response.data) > 0
        except Exception as e:
            print(f"Error updating balance: {e}")
            return False
    
    def create_transaction(self, transaction_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create new transaction (user can only create their own)"""
        try:
            response = self.supabase.table("transactions").insert(transaction_data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error creating transaction: {e}")
            return None
    
    def get_user_transactions(self, user_id: str) -> List[Dict[str, Any]]:
        """Get user's transactions (user can only see their own)"""
        try:
            response = self.supabase.table("transactions").select(
                "*, collectibles(name, type, current_price)"
            ).eq("user_id", user_id).order("created_at", desc=True).execute()
            return response.data
        except Exception as e:
            print(f"Error fetching transactions: {e}")
            return []
    
    # Price History Methods (Public Read)
    def get_price_history(self, collectible_id: str) -> List[Dict[str, Any]]:
        """Get price history for a collectible (public access)"""
        try:
            response = self.supabase.table("price_history").select("*").eq(
                "collectible_id", collectible_id
            ).order("recorded_at", desc=True).execute()
            return response.data
        except Exception as e:
            print(f"Error fetching price history: {e}")
            return []
    
    def add_price_record(self, collectible_id: str, price: float) -> bool:
        """Add price record (requires authentication)"""
        try:
            price_data = {
                "collectible_id": collectible_id,
                "price": price
            }
            response = self.supabase.table("price_history").insert(price_data).execute()
            
            # Also update current price in collectibles table
            self.supabase.table("collectibles").update({
                "current_price": price
            }).eq("id", collectible_id).execute()
            
            return len(response.data) > 0
        except Exception as e:
            print(f"Error adding price record: {e}")
            return False
    
    # Referral Methods (RLS Protected)
    def create_referral(self, referrer_id: str, referred_id: str, bonus_amount: float) -> Optional[Dict[str, Any]]:
        """Create referral (user can only create referrals where they are the referrer)"""
        try:
            referral_data = {
                "referrer_id": referrer_id,
                "referred_id": referred_id,
                "bonus_amount": bonus_amount
            }
            response = self.supabase.table("referrals").insert(referral_data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error creating referral: {e}")
            return None
    
    def get_user_referrals(self, user_id: str) -> List[Dict[str, Any]]:
        """Get referrals where user is involved (referrer or referred)"""
        try:
            response = self.supabase.table("referrals").select(
                "*, referrer:referrer_id(username), referred:referred_id(username)"
            ).or_(f"referrer_id.eq.{user_id},referred_id.eq.{user_id}").execute()
            return response.data
        except Exception as e:
            print(f"Error fetching referrals: {e}")
            return []
    
    # Redemption Methods (RLS Protected)
    def create_redemption(self, user_id: str, collectible_id: str, cost: float) -> Optional[Dict[str, Any]]:
        """Create redemption (user can only create their own)"""
        try:
            redemption_data = {
                "user_id": user_id,
                "collectible_id": collectible_id,
                "cost": cost,
                "status": "pending"
            }
            response = self.supabase.table("redemptions").insert(redemption_data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error creating redemption: {e}")
            return None
    
    def get_user_redemptions(self, user_id: str) -> List[Dict[str, Any]]:
        """Get user's redemptions (user can only see their own)"""
        try:
            response = self.supabase.table("redemptions").select(
                "*, collectibles(name, type, current_price)"
            ).eq("user_id", user_id).order("created_at", desc=True).execute()
            return response.data
        except Exception as e:
            print(f"Error fetching redemptions: {e}")
            return []

# Global instance
db_service = DatabaseService()
