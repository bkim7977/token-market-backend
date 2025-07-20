#!/usr/bin/env python3
"""
Direct Database Access Examples
Using the database service layer directly
"""

import sys
import os
import asyncio
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.db_service import DatabaseService
from app.database import supabase

async def direct_database_demo():
    """Demonstrate direct database access"""
    print("🗄️ Direct Database Access Demo")
    print("=" * 50)
    
    # Initialize database service
    db_service = DatabaseService()
    
    # 1. Create a user with JWT
    print("\n1️⃣ Creating user with JWT authentication...")
    user_result = await db_service.create_user_with_jwt(
        email="direct.access@example.com",
        password="DirectPassword123!",
        username="direct_user"
    )
    
    if user_result["success"]:
        print(f"✅ User created: {user_result['user']['username']}")
        print(f"🔑 JWT Token: {user_result['access_token'][:50]}...")
        user_id = user_result['user']['id']
    else:
        print(f"❌ User creation failed: {user_result['error']}")
        return
    
    # 2. Authenticate user
    print("\n2️⃣ Authenticating user...")
    auth_result = await db_service.authenticate_user_with_jwt(
        email="direct.access@example.com",
        password="DirectPassword123!"
    )
    
    if auth_result["success"]:
        print(f"✅ Authentication successful")
        print(f"🔑 New JWT Token: {auth_result['access_token'][:50]}...")
    
    # 3. Direct database queries (using Supabase client)
    print("\n3️⃣ Direct database queries...")
    
    # Get user data
    user_data = supabase.table("users").select("*").eq("id", user_id).execute()
    if user_data.data:
        user = user_data.data[0]
        print(f"👤 User: {user['username']} ({user['email']})")
    
    # Get token balance
    balance_data = supabase.table("token_balances").select("*").eq("user_id", user_id).execute()
    if balance_data.data:
        balance = balance_data.data[0]
        print(f"💰 Balance: {balance['balance']} tokens")
    
    # Get all collectibles
    collectibles = supabase.table("collectibles").select("*").execute()
    print(f"🎮 Total collectibles in database: {len(collectibles.data)}")
    
    # 4. Create a transaction
    print("\n4️⃣ Creating a sample transaction...")
    if collectibles.data:
        collectible_id = collectibles.data[0]['id']
        transaction_data = {
            "id": f"txn_{user_id[:8]}",
            "user_id": user_id,
            "collectible_id": collectible_id,
            "transaction_type": "purchase",
            "amount": 25.00
        }
        
        try:
            txn_result = supabase.table("transactions").insert(transaction_data).execute()
            if txn_result.data:
                print(f"✅ Transaction created: ${transaction_data['amount']}")
            else:
                print(f"❌ Transaction failed")
        except Exception as e:
            print(f"⚠️ Transaction failed (might be RLS restriction): {e}")
    
    print("\n🎯 Direct Database Access Methods:")
    print("✅ DatabaseService methods (recommended)")
    print("✅ Direct Supabase client queries")
    print("✅ SQLAlchemy ORM (available)")
    print("✅ Raw SQL queries (if needed)")

if __name__ == "__main__":
    asyncio.run(direct_database_demo())
