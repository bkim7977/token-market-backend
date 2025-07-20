# Token Market Backend - Database Setup Guide

Since direct SQL execution through the Supabase Python client requires additional setup, please create the tables manually through the Supabase dashboard.

## Step 1: Access Supabase Dashboard
1. Go to https://supabase.com/dashboard
2. Navigate to your project: `rrhdrkmomngxcjsatcpy`
3. Go to the "SQL Editor" or "Database" section

## Step 2: Execute the following SQL commands

### 1. Users Table
```sql
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR UNIQUE NOT NULL,
    username VARCHAR UNIQUE NOT NULL,
    password_hash VARCHAR NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_login TIMESTAMP WITH TIME ZONE
);
```

### 2. Collectibles Table
```sql
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
```

### 3. Token Balances Table
```sql
CREATE TABLE IF NOT EXISTS token_balances (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    balance DECIMAL(10,2) DEFAULT 0.00,
    last_updated TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id)
);
```

### 4. Price History Table
```sql
CREATE TABLE IF NOT EXISTS price_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    collectible_id UUID REFERENCES collectibles(id) ON DELETE CASCADE,
    price DECIMAL(10,2) NOT NULL,
    recorded_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### 5. Transactions Table
```sql
CREATE TABLE IF NOT EXISTS transactions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    collectible_id UUID REFERENCES collectibles(id) ON DELETE SET NULL,
    transaction_type VARCHAR NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### 6. Referrals Table
```sql
CREATE TABLE IF NOT EXISTS referrals (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    referrer_id UUID REFERENCES users(id) ON DELETE CASCADE,
    referred_id UUID REFERENCES users(id) ON DELETE CASCADE,
    bonus_amount DECIMAL(10,2),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(referred_id)
);
```

### 7. Redemptions Table
```sql
CREATE TABLE IF NOT EXISTS redemptions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    collectible_id UUID REFERENCES collectibles(id) ON DELETE SET NULL,
    cost DECIMAL(10,2) NOT NULL,
    status VARCHAR DEFAULT 'pending',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

## Step 3: Enable Row Level Security (RLS)
After creating the tables, you should enable RLS for security:

```sql
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE collectibles ENABLE ROW LEVEL SECURITY;
ALTER TABLE token_balances ENABLE ROW LEVEL SECURITY;
ALTER TABLE price_history ENABLE ROW LEVEL SECURITY;
ALTER TABLE transactions ENABLE ROW LEVEL SECURITY;
ALTER TABLE referrals ENABLE ROW LEVEL SECURITY;
ALTER TABLE redemptions ENABLE ROW LEVEL SECURITY;
```

## Step 4: Test the Setup
Once you've created the tables, run:
```bash
python test_database.py
```

This will verify that all tables are accessible and insert some sample data.
