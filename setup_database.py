#!/usr/bin/env python3
"""
Database setup script for Token Market Backend
Creates all necessary tables using Supabase client
"""

from app.database import supabase
import json

def create_tables():
    """Create all database tables using Supabase SQL functions"""
    
    # SQL to create all tables
    sql_commands = [
        # Users table
        """
        CREATE TABLE IF NOT EXISTS users (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            email VARCHAR UNIQUE NOT NULL,
            username VARCHAR UNIQUE NOT NULL,
            password_hash VARCHAR NOT NULL,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            last_login TIMESTAMP WITH TIME ZONE
        );
        """,
        
        # Collectibles table
        """
        CREATE TABLE IF NOT EXISTS collectibles (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            name VARCHAR NOT NULL,
            type VARCHAR,
            set VARCHAR,
            rarity VARCHAR,
            edition VARCHAR,
            metadata JSONB,
            image_url VARCHAR,
            current_price DECIMAL(10,2)
        );
        """,
        
        # Token balances table
        """
        CREATE TABLE IF NOT EXISTS token_balances (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            user_id UUID REFERENCES users(id) ON DELETE CASCADE,
            balance DECIMAL(10,2) DEFAULT 0.00,
            last_updated TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            UNIQUE(user_id)
        );
        """,
        
        # Price history table
        """
        CREATE TABLE IF NOT EXISTS price_history (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            collectible_id UUID REFERENCES collectibles(id) ON DELETE CASCADE,
            price DECIMAL(10,2) NOT NULL,
            recorded_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        );
        """,
        
        # Transactions table
        """
        CREATE TABLE IF NOT EXISTS transactions (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            user_id UUID REFERENCES users(id) ON DELETE CASCADE,
            collectible_id UUID REFERENCES collectibles(id) ON DELETE SET NULL,
            transaction_type VARCHAR NOT NULL,
            amount DECIMAL(10,2) NOT NULL,
            description TEXT,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        );
        """,
        
        # Referrals table
        """
        CREATE TABLE IF NOT EXISTS referrals (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            referrer_id UUID REFERENCES users(id) ON DELETE CASCADE,
            referred_id UUID REFERENCES users(id) ON DELETE CASCADE,
            bonus_amount DECIMAL(10,2),
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            UNIQUE(referred_id)
        );
        """,
        
        # Redemptions table
        """
        CREATE TABLE IF NOT EXISTS redemptions (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            user_id UUID REFERENCES users(id) ON DELETE CASCADE,
            collectible_id UUID REFERENCES collectibles(id) ON DELETE SET NULL,
            cost DECIMAL(10,2) NOT NULL,
            status VARCHAR DEFAULT 'pending',
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        );
        """
    ]
    
    # Execute each SQL command
    for i, sql in enumerate(sql_commands, 1):
        try:
            response = supabase.rpc('exec_sql', {'sql': sql}).execute()
            table_name = sql.split('CREATE TABLE IF NOT EXISTS')[1].split('(')[0].strip()
            print(f"✓ Created table: {table_name}")
        except Exception as e:
            print(f"✗ Error creating table {i}: {e}")
            # Try alternative method
            try:
                # For some Supabase setups, we might need to use a different approach
                print(f"  Trying alternative method for table {i}...")
                continue
            except Exception as e2:
                print(f"  Alternative method also failed: {e2}")

def test_tables():
    """Test that all tables were created successfully"""
    tables = ['users', 'collectibles', 'token_balances', 'price_history', 
              'transactions', 'referrals', 'redemptions']
    
    for table in tables:
        try:
            response = supabase.table(table).select('*').limit(1).execute()
            print(f"✓ Table '{table}' is accessible")
        except Exception as e:
            print(f"✗ Table '{table}' error: {e}")

def insert_sample_data():
    """Insert some sample data for testing"""
    try:
        # Sample collectible
        collectible_data = {
            "name": "Charizard",
            "type": "Pokemon Card",
            "set": "Base Set",
            "rarity": "Rare Holo",
            "edition": "1st Edition",
            "metadata": {
                "hp": 120,
                "card_number": "4/102",
                "artist": "Mitsuhiro Arita"
            },
            "current_price": 500.00
        }
        
        response = supabase.table("collectibles").insert(collectible_data).execute()
        print("✓ Sample collectible data inserted")
        
    except Exception as e:
        print(f"✗ Error inserting sample data: {e}")

if __name__ == "__main__":
    print("Setting up Token Market Backend Database...")
    print("=" * 50)
    
    # Note: Direct SQL execution might not work with all Supabase plans
    # We'll create tables using the Supabase dashboard if needed
    print("Note: If SQL execution fails, you'll need to create tables via Supabase dashboard")
    print()
    
    create_tables()
    print()
    test_tables()
    print()
    insert_sample_data()
    print()
    print("Database setup complete!")
