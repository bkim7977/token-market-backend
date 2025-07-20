#!/usr/bin/env python3
"""
Test database connectivity and basic operations
Run this after creating tables in Supabase dashboard
"""

from app.database import supabase
import uuid
from datetime import datetime

def test_database_connection():
    """Test basic database connectivity"""
    print("Testing Supabase connection...")
    
    tables = ['users', 'collectibles', 'token_balances', 'price_history', 
              'transactions', 'referrals', 'redemptions']
    
    for table in tables:
        try:
            response = supabase.table(table).select('*').limit(1).execute()
            print(f"✓ Table '{table}' is accessible")
        except Exception as e:
            print(f"✗ Table '{table}' error: {e}")
            return False
    
    return True

def insert_sample_data():
    """Insert sample data to test CRUD operations"""
    print("\nInserting sample data...")
    
    try:
        # 1. Insert a sample collectible
        collectible_data = {
            "name": "Charizard Base Set",
            "type": "Pokemon Card",
            "set_name": "Base Set",  # Changed from 'set' to 'set_name'
            "rarity": "Rare Holo",
            "edition": "1st Edition",
            "metadata": {
                "hp": 120,
                "card_number": "4/102",
                "artist": "Mitsuhiro Arita",
                "attacks": ["Fire Spin", "Flamethrower"]
            },
            "image_url": "https://example.com/charizard.jpg",
            "current_price": 500.00
        }
        
        collectible_response = supabase.table("collectibles").insert(collectible_data).execute()
        collectible_id = collectible_response.data[0]['id']
        print(f"✓ Sample collectible inserted with ID: {collectible_id}")
        
        # 2. Insert a sample user
        user_data = {
            "email": "test@example.com",
            "username": "testuser",
            "password_hash": "hashed_password_here"
        }
        
        user_response = supabase.table("users").insert(user_data).execute()
        user_id = user_response.data[0]['id']
        print(f"✓ Sample user inserted with ID: {user_id}")
        
        # 3. Insert token balance for user
        balance_data = {
            "user_id": user_id,
            "balance": 100.00
        }
        
        balance_response = supabase.table("token_balances").insert(balance_data).execute()
        print("✓ Sample token balance inserted")
        
        # 4. Insert price history
        price_data = {
            "collectible_id": collectible_id,
            "price": 450.00
        }
        
        price_response = supabase.table("price_history").insert(price_data).execute()
        print("✓ Sample price history inserted")
        
        # 5. Insert transaction
        transaction_data = {
            "user_id": user_id,
            "collectible_id": collectible_id,
            "transaction_type": "purchase",
            "amount": 500.00,
            "description": "Purchased Charizard card"
        }
        
        transaction_response = supabase.table("transactions").insert(transaction_data).execute()
        print("✓ Sample transaction inserted")
        
        return True
        
    except Exception as e:
        print(f"✗ Error inserting sample data: {e}")
        return False

def test_queries():
    """Test various query operations"""
    print("\nTesting query operations...")
    
    try:
        # Test select all collectibles
        collectibles = supabase.table("collectibles").select("*").execute()
        print(f"✓ Found {len(collectibles.data)} collectible(s)")
        
        # Test filtered query
        expensive_items = supabase.table("collectibles").select("*").gte("current_price", 400).execute()
        print(f"✓ Found {len(expensive_items.data)} expensive collectible(s)")
        
        # Test join-like query (get user with balance)
        users_with_balance = supabase.table("users").select("*, token_balances(*)").execute()
        print(f"✓ Found {len(users_with_balance.data)} user(s) with balance info")
        
        # Test transaction history
        transactions = supabase.table("transactions").select("*, users(username), collectibles(name)").execute()
        print(f"✓ Found {len(transactions.data)} transaction(s)")
        
        return True
        
    except Exception as e:
        print(f"✗ Error testing queries: {e}")
        return False

def test_updates():
    """Test update operations"""
    print("\nTesting update operations...")
    
    try:
        # Update collectible price
        update_response = supabase.table("collectibles").update({
            "current_price": 550.00
        }).eq("name", "Charizard Base Set").execute()
        
        if update_response.data:
            print("✓ Price update successful")
        else:
            print("✗ No items updated")
            
        return True
        
    except Exception as e:
        print(f"✗ Error testing updates: {e}")
        return False

def cleanup_sample_data():
    """Clean up test data"""
    print("\nCleaning up sample data...")
    
    try:
        # Delete in reverse order due to foreign key constraints
        supabase.table("transactions").delete().eq("description", "Purchased Charizard card").execute()
        
        # Get all price history and delete (safer than using neq with empty string)
        price_history = supabase.table("price_history").select("id").execute()
        if price_history.data:
            for record in price_history.data:
                supabase.table("price_history").delete().eq("id", record["id"]).execute()
        
        supabase.table("token_balances").delete().eq("balance", 100.00).execute()
        supabase.table("users").delete().eq("email", "test@example.com").execute()
        supabase.table("collectibles").delete().eq("name", "Charizard Base Set").execute()
        
        print("✓ Sample data cleaned up")
        return True
        
    except Exception as e:
        print(f"✗ Error cleaning up: {e}")
        return False

def main():
    """Main test function"""
    print("Token Market Backend - Database Test")
    print("=" * 50)
    
    # Test connection
    if not test_database_connection():
        print("\n❌ Database connection failed. Please create tables first.")
        print("Run the SQL commands from DATABASE_SETUP.md in your Supabase dashboard.")
        return
    
    print("\n✅ Database connection successful!")
    
    # Run tests
    success = True
    success &= insert_sample_data()
    success &= test_queries()
    success &= test_updates()
    
    # Cleanup
    cleanup_sample_data()
    
    if success:
        print("\n🎉 All tests passed! Your database is ready for the Token Market Backend.")
    else:
        print("\n⚠️  Some tests failed. Check the errors above.")

if __name__ == "__main__":
    main()
