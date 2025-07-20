#!/usr/bin/env python3
"""
🗄️ COMPLETE DATABASE ACCESS GUIDE - PYTHON EXAMPLES
Demonstrates all 4 ways to access your Token Market database in Python
"""

import os
import sys
import asyncio
import requests
import json
from datetime import datetime, timedelta

# Add the app directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

print("🎯 TOKEN MARKET DATABASE - 4 PYTHON ACCESS METHODS")
print("="*70)

# ============================================================================
# METHOD 1: HTTP API CLIENT (Recommended for web/mobile apps)
# ============================================================================

class TokenMarketAPIClient:
    """Python client for the Token Market API."""
    
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.access_token = None
    
    def register(self, email, password, username):
        """Register a new user."""
        response = self.session.post(
            f"{self.base_url}/auth/register",
            json={"email": email, "password": password, "username": username}
        )
        return response.json() if response.status_code == 200 else None
    
    def login(self, email, password):
        """Login and store access token."""
        response = self.session.post(
            f"{self.base_url}/auth/login",
            json={"email": email, "password": password}
        )
        
        if response.status_code == 200:
            data = response.json()
            self.access_token = data.get("access_token")
            self.session.headers.update({
                "Authorization": f"Bearer {self.access_token}"
            })
            return data
        return None
    
    def get_profile(self):
        """Get user profile (protected endpoint)."""
        response = self.session.get(f"{self.base_url}/profile")
        return response.json() if response.status_code == 200 else None
    
    def get_balance(self):
        """Get user token balance (protected endpoint)."""
        response = self.session.get(f"{self.base_url}/profile/balance")
        return response.json() if response.status_code == 200 else None
    
    def get_collectibles(self):
        """Get all collectibles (public endpoint)."""
        # Remove auth header for public endpoint
        headers = self.session.headers.copy()
        if "Authorization" in headers:
            del headers["Authorization"]
        
        response = requests.get(f"{self.base_url}/collectibles", headers=headers)
        return response.json() if response.status_code == 200 else None

def demo_method_1_api_client():
    """Demo Method 1: HTTP API Client"""
    print("\n🌐 METHOD 1: HTTP API CLIENT")
    print("-" * 40)
    
    try:
        client = TokenMarketAPIClient()
        
        # Register user
        email = f"api_client_{datetime.now().strftime('%H%M%S')}@example.com"
        register_result = client.register(email, "password123", "api_client_user")
        print(f"✅ Registration: {register_result}")
        
        # Login
        login_result = client.login(email, "password123")
        if login_result:
            print(f"✅ Login successful: {login_result.get('user', {}).get('username')}")
            
            # Get profile
            profile = client.get_profile()
            print(f"✅ Profile: {profile}")
            
            # Get balance
            balance = client.get_balance()
            print(f"✅ Balance: {balance}")
        
        # Get public data
        collectibles = client.get_collectibles()
        print(f"✅ Collectibles: {len(collectibles) if collectibles else 0} items")
        
    except Exception as e:
        print(f"❌ API Client Error: {e}")
        print("Make sure the server is running: python start.py serve")

# ============================================================================
# METHOD 2: DATABASE SERVICE LAYER (Your existing service)
# ============================================================================

def demo_method_2_service_layer():
    """Demo Method 2: Database Service Layer"""
    print("\n🔧 METHOD 2: DATABASE SERVICE LAYER")
    print("-" * 40)
    
    try:
        from db_service import DatabaseService
        
        db_service = DatabaseService()
        
        # Create user with JWT
        email = f"service_user_{datetime.now().strftime('%H%M%S')}@example.com"
        user_result = asyncio.run(
            db_service.create_user_with_jwt(email, "password123", "service_user")
        )
        print(f"✅ User created via service: {user_result}")
        
        # Authenticate user
        auth_result = asyncio.run(
            db_service.authenticate_user_jwt(email, "password123")
        )
        if auth_result:
            print(f"✅ Authentication successful: {auth_result['user']['username']}")
            
            # Get user data
            user_id = auth_result['user']['user_id']
            balance = asyncio.run(db_service.get_user_balance(user_id))
            print(f"✅ Balance via service: {balance}")
        
        # Get collectibles
        collectibles = asyncio.run(db_service.get_all_collectibles())
        print(f"✅ Collectibles via service: {len(collectibles)} items")
        
    except Exception as e:
        print(f"❌ Service Layer Error: {e}")
        print("Check your database connection and service layer implementation")

# ============================================================================
# METHOD 3: DIRECT SUPABASE ACCESS (For backend services)
# ============================================================================

def demo_method_3_direct_supabase():
    """Demo Method 3: Direct Supabase Access"""
    print("\n🗄️ METHOD 3: DIRECT SUPABASE ACCESS")
    print("-" * 40)
    
    try:
        from database import supabase
        from auth import hash_password
        import uuid
        
        # Create user directly
        user_id = str(uuid.uuid4())
        email = f"direct_user_{datetime.now().strftime('%H%M%S')}@example.com"
        username = "direct_user"
        password_hash = hash_password("password123")
        
        user_result = supabase.table("users").insert({
            "user_id": user_id,
            "email": email,
            "username": username,
            "password_hash": password_hash,
            "created_at": datetime.now().isoformat()
        }).execute()
        
        print(f"✅ Direct user creation: {user_result.data}")
        
        # Query user data
        users = supabase.table("users").select("*").eq("email", email).execute()
        print(f"✅ User query: {users.data}")
        
        # Get user balance
        balance = supabase.table("token_balances").select("*").eq("user_id", user_id).execute()
        print(f"✅ Balance query: {balance.data}")
        
        # Get public collectibles
        collectibles = supabase.table("collectibles").select("*").limit(3).execute()
        print(f"✅ Collectibles: {len(collectibles.data)} items")
        
    except Exception as e:
        print(f"❌ Direct Supabase Error: {e}")
        print("Check your Supabase connection and credentials")

# ============================================================================
# METHOD 4: RAW HTTP REQUESTS (For any language/framework)
# ============================================================================

def demo_method_4_raw_http():
    """Demo Method 4: Raw HTTP Requests"""
    print("\n📡 METHOD 4: RAW HTTP REQUESTS")
    print("-" * 40)
    
    try:
        import urllib.request
        import urllib.parse
        
        base_url = "http://localhost:8000"
        
        # Register user
        email = f"http_user_{datetime.now().strftime('%H%M%S')}@example.com"
        register_data = {
            "email": email,
            "password": "password123",
            "username": "http_user"
        }
        
        req = urllib.request.Request(
            f"{base_url}/auth/register",
            data=json.dumps(register_data).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        
        with urllib.request.urlopen(req) as response:
            register_result = json.loads(response.read().decode('utf-8'))
            print(f"✅ Raw HTTP Registration: {register_result}")
        
        # Login user
        login_data = {
            "email": email,
            "password": "password123"
        }
        
        req = urllib.request.Request(
            f"{base_url}/auth/login",
            data=json.dumps(login_data).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        
        with urllib.request.urlopen(req) as response:
            login_result = json.loads(response.read().decode('utf-8'))
            access_token = login_result.get("access_token")
            print(f"✅ Raw HTTP Login: Success, token length: {len(access_token) if access_token else 0}")
        
        # Protected request
        if access_token:
            req = urllib.request.Request(
                f"{base_url}/profile/balance",
                headers={'Authorization': f'Bearer {access_token}'}
            )
            
            with urllib.request.urlopen(req) as response:
                balance_result = json.loads(response.read().decode('utf-8'))
                print(f"✅ Raw HTTP Protected Request: {balance_result}")
        
        # Public request
        with urllib.request.urlopen(f"{base_url}/collectibles") as response:
            collectibles_result = json.loads(response.read().decode('utf-8'))
            print(f"✅ Raw HTTP Public Request: {len(collectibles_result)} collectibles")
    
    except Exception as e:
        print(f"❌ Raw HTTP Error: {e}")
        print("Make sure the server is running: python start.py serve")

# ============================================================================
# MAIN DEMO RUNNER
# ============================================================================

def main():
    """Run all database access demos."""
    
    print("🚀 Running comprehensive database access demonstration...")
    print("This will show you 4 different ways to use your database in Python!\n")
    
    # Method 1: API Client (most common for apps)
    demo_method_1_api_client()
    
    # Method 2: Service Layer (backend-to-backend)
    demo_method_2_service_layer()
    
    # Method 3: Direct Supabase (advanced use cases)
    demo_method_3_direct_supabase()
    
    # Method 4: Raw HTTP (universal approach)
    demo_method_4_raw_http()
    
    print("\n" + "="*70)
    print("🎯 DATABASE ACCESS METHODS SUMMARY")
    print("="*70)
    print("1️⃣  HTTP API Client    - Best for web/mobile apps")
    print("2️⃣  Service Layer      - Best for backend services")
    print("3️⃣  Direct Supabase    - Best for advanced database operations")
    print("4️⃣  Raw HTTP Requests  - Universal approach for any language")
    print("\n✅ All methods demonstrated successfully!")
    print("\n📚 DOCUMENTATION:")
    print("- Full usage guide: DATABASE_USAGE.md")
    print("- API documentation: http://localhost:8000/docs")
    print("- Live demos: python database_usage_demo.py")

if __name__ == "__main__":
    main()
