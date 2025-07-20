#!/usr/bin/env python3
"""
Token Market Database Usage Examples
Complete guide for interacting with your JWT-authenticated database
"""

import requests
import json

# API Base URL
API_BASE = "http://localhost:8000"

class TokenMarketClient:
    def __init__(self):
        self.base_url = API_BASE
        self.access_token = None
        self.headers = {"Content-Type": "application/json"}
    
    def register_user(self, email, password, username):
        """Register a new user and get JWT token"""
        data = {
            "email": email,
            "password": password,
            "username": username
        }
        response = requests.post(f"{self.base_url}/auth/register", 
                               json=data, headers=self.headers)
        
        if response.status_code == 200:
            result = response.json()
            self.access_token = result["access_token"]
            self.headers["Authorization"] = f"Bearer {self.access_token}"
            print(f"✅ User registered: {result['user']['username']}")
            return result
        else:
            print(f"❌ Registration failed: {response.text}")
            return None
    
    def login_user(self, email, password):
        """Login user and get JWT token"""
        data = {"email": email, "password": password}
        response = requests.post(f"{self.base_url}/auth/login", 
                               json=data, headers=self.headers)
        
        if response.status_code == 200:
            result = response.json()
            self.access_token = result["access_token"]
            self.headers["Authorization"] = f"Bearer {self.access_token}"
            print(f"✅ Login successful: {result['user']['username']}")
            return result
        else:
            print(f"❌ Login failed: {response.text}")
            return None
    
    def get_user_balance(self):
        """Get current user's token balance (requires authentication)"""
        if not self.access_token:
            print("❌ Not authenticated. Login first.")
            return None
        
        response = requests.get(f"{self.base_url}/profile/balance", 
                              headers=self.headers)
        
        if response.status_code == 200:
            balance = response.json()
            print(f"💰 Balance: {balance['balance']} tokens")
            return balance
        else:
            print(f"❌ Failed to get balance: {response.text}")
            return None
    
    def get_collectibles(self):
        """Get all collectibles (public endpoint)"""
        response = requests.get(f"{self.base_url}/collectibles")
        
        if response.status_code == 200:
            collectibles = response.json()
            print(f"🎮 Found {len(collectibles)} collectibles:")
            for item in collectibles:
                print(f"  - {item['name']} ({item['set_name']}) - ${item.get('current_price', 'N/A')}")
            return collectibles
        else:
            print(f"❌ Failed to get collectibles: {response.text}")
            return None

def demo_usage():
    """Demonstrate complete database usage"""
    print("🎮 Token Market Database Demo")
    print("=" * 50)
    
    # Initialize client
    client = TokenMarketClient()
    
    # 1. Register a new user
    print("\n1️⃣ Registering new user...")
    import uuid
    test_suffix = uuid.uuid4().hex[:6]
    user_data = client.register_user(
        email=f"demo.user.{test_suffix}@example.com",
        password="SecurePassword123!",
        username=f"demo_user_{test_suffix}"
    )
    
    if not user_data:
        print("Demo failed at registration")
        return
    
    # 2. Get user balance
    print("\n2️⃣ Getting user balance...")
    client.get_user_balance()
    
    # 3. View available collectibles
    print("\n3️⃣ Browsing collectibles...")
    client.get_collectibles()
    
    # 4. Login with same user (demonstrates token refresh)
    print("\n4️⃣ Testing login...")
    client.access_token = None  # Clear token
    client.headers.pop("Authorization", None)  # Remove auth header
    
    login_result = client.login_user(
        email=user_data["user"]["email"],
        password="SecurePassword123!"
    )
    
    if login_result:
        print("\n5️⃣ Accessing protected data after login...")
        client.get_user_balance()
    
    print("\n🎉 Database demo complete!")
    print("\n📊 Your database supports:")
    print("✅ User registration with JWT authentication")
    print("✅ Secure login system")
    print("✅ Protected user data (balances, transactions)")
    print("✅ Public data access (collectibles)")
    print("✅ Row Level Security (users only see their own data)")

if __name__ == "__main__":
    demo_usage()
