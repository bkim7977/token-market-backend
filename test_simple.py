#!/usr/bin/env python3
"""
Simplified Token Market Backend Test
Tests basic functionality without RLS complications for initial verification
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import asyncio
import uuid
from app.database import supabase

async def test_basic_database_connection():
    """Test basic database connection"""
    print("🔌 Testing Database Connection...")
    
    try:
        # Test basic connection with public table (collectibles)
        result = supabase.table("collectibles").select("*").limit(1).execute()
        print("✓ Database connection successful")
        print(f"✓ Found {len(result.data)} collectibles")
        return True
        
    except Exception as e:
        print(f"✗ Database connection failed: {e}")
        return False

async def test_user_operations():
    """Test basic user operations"""
    print("\n👤 Testing User Operations...")
    
    try:
        # Generate test data
        test_suffix = uuid.uuid4().hex[:8]
        test_user = {
            "id": str(uuid.uuid4()),
            "email": f"test.{test_suffix}@example.com",
            "username": f"testuser_{test_suffix}",
            "password_hash": "test_hash"
        }
        
        # Test user creation
        user_result = supabase.table("users").insert(test_user).execute()
        if user_result.data:
            print("✓ User creation successful")
            user_id = user_result.data[0]["id"]
            
            # Test token balance creation
            balance_data = {
                "user_id": user_id,
                "balance": 100.00
            }
            balance_result = supabase.table("token_balances").insert(balance_data).execute()
            if balance_result.data:
                print("✓ Token balance creation successful")
            
            return user_id
        else:
            print("✗ User creation failed")
            return None
            
    except Exception as e:
        print(f"✗ User operations failed: {e}")
        return None

async def test_collectibles():
    """Test collectible operations"""
    print("\n🎮 Testing Collectibles...")
    
    try:
        # Create test collectible
        collectible_data = {
            "id": str(uuid.uuid4()),
            "name": "Test Collectible",
            "set_name": "Test Set",
            "rarity": "common",
            "current_price": 10.00
        }
        
        result = supabase.table("collectibles").insert(collectible_data).execute()
        if result.data:
            print("✓ Collectible creation successful")
            return result.data[0]["id"]
        else:
            print("✗ Collectible creation failed")
            return None
            
    except Exception as e:
        print(f"✗ Collectible operations failed: {e}")
        return None

async def test_transactions(user_id: str, collectible_id: str):
    """Test transaction operations"""
    print("\n💰 Testing Transactions...")
    
    try:
        # Create test transaction
        transaction_data = {
            "id": str(uuid.uuid4()),
            "user_id": user_id,
            "collectible_id": collectible_id,
            "transaction_type": "purchase",
            "amount": 10.00
        }
        
        result = supabase.table("transactions").insert(transaction_data).execute()
        if result.data:
            print("✓ Transaction creation successful")
            return True
        else:
            print("✗ Transaction creation failed")
            return False
            
    except Exception as e:
        print(f"✗ Transaction operations failed: {e}")
        return False

async def run_simple_test():
    """Run comprehensive but simple test suite"""
    print("🚀 Simple Token Market Backend Test")
    print("=" * 50)
    
    # Test 1: Database Connection
    if not await test_basic_database_connection():
        print("\n❌ Database connection failed - stopping tests")
        return
    
    # Test 2: User Operations
    user_id = await test_user_operations()
    if not user_id:
        print("\n❌ User operations failed - stopping tests")
        return
    
    # Test 3: Collectibles
    collectible_id = await test_collectibles()
    if not collectible_id:
        print("\n❌ Collectible operations failed - stopping tests")
        return
    
    # Test 4: Transactions
    if not await test_transactions(user_id, collectible_id):
        print("\n❌ Transaction operations failed")
        return
    
    print("\n✅ All basic tests passed!")
    print("🎉 Database is working correctly!")

if __name__ == "__main__":
    asyncio.run(run_simple_test())
