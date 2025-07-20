# Token Market Backend - Database Setup Guide

Execute these SQL commands one by one in your Supabase SQL Editor.

## Step 1: Access Supabase Dashboard
1. Go to https://supabase.com/dashboard
2. Navigate to your project: rrhdrkmomngxcjsatcpy
3. Go to the SQL Editor

## Step 2: Create Tables (Run each command separately)

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
    set_name VARCHAR,
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

## Step 3: Enable Row Level Security
Run each ALTER statement separately:

```sql
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
```

```sql
ALTER TABLE collectibles ENABLE ROW LEVEL SECURITY;
```

```sql
ALTER TABLE token_balances ENABLE ROW LEVEL SECURITY;
```

```sql
ALTER TABLE price_history ENABLE ROW LEVEL SECURITY;
```

```sql
ALTER TABLE transactions ENABLE ROW LEVEL SECURITY;
```

```sql
ALTER TABLE referrals ENABLE ROW LEVEL SECURITY;
```

```sql
ALTER TABLE redemptions ENABLE ROW LEVEL SECURITY;
```

## Step 4: Create Production-Ready RLS Policies

### Users Table Policies
```sql
CREATE POLICY "Users can view their own profile" ON users
FOR SELECT USING (auth.uid() = id);
```

```sql
CREATE POLICY "Users can insert their own profile" ON users
FOR INSERT WITH CHECK (auth.uid() = id);
```

```sql
CREATE POLICY "Users can update their own profile" ON users
FOR UPDATE USING (auth.uid() = id);
```

### Collectibles Table Policies
```sql
CREATE POLICY "Anyone can view collectibles" ON collectibles
FOR SELECT USING (true);
```

```sql
CREATE POLICY "Only authenticated users can insert collectibles" ON collectibles
FOR INSERT WITH CHECK (auth.role() = 'authenticated');
```

```sql
CREATE POLICY "Only authenticated users can update collectibles" ON collectibles
FOR UPDATE USING (auth.role() = 'authenticated');
```

### Token Balances Table Policies
```sql
CREATE POLICY "Users can view their own balance" ON token_balances
FOR SELECT USING (auth.uid() = user_id);
```

```sql
CREATE POLICY "Users can insert their own balance" ON token_balances
FOR INSERT WITH CHECK (auth.uid() = user_id);
```

```sql
CREATE POLICY "Users can update their own balance" ON token_balances
FOR UPDATE USING (auth.uid() = user_id);
```

### Price History Table Policies
```sql
CREATE POLICY "Anyone can view price history" ON price_history
FOR SELECT USING (true);
```

```sql
CREATE POLICY "Authenticated users can insert price history" ON price_history
FOR INSERT WITH CHECK (auth.role() = 'authenticated');
```

### Transactions Table Policies
```sql
CREATE POLICY "Users can view their own transactions" ON transactions
FOR SELECT USING (auth.uid() = user_id);
```

```sql
CREATE POLICY "Users can insert their own transactions" ON transactions
FOR INSERT WITH CHECK (auth.uid() = user_id);
```

### Referrals Table Policies
```sql
CREATE POLICY "Users can view referrals they're involved in" ON referrals
FOR SELECT USING (auth.uid() = referrer_id OR auth.uid() = referred_id);
```

```sql
CREATE POLICY "Users can create referrals" ON referrals
FOR INSERT WITH CHECK (auth.uid() = referrer_id);
```

### Redemptions Table Policies
```sql
CREATE POLICY "Users can view their own redemptions" ON redemptions
FOR SELECT USING (auth.uid() = user_id);
```

```sql
CREATE POLICY "Users can create redemptions" ON redemptions
FOR INSERT WITH CHECK (auth.uid() = user_id);
```

## Step 5: Test the Setup
```bash
python test_database_rls.py
```

## Production-Ready Security Features:
- **User Data Isolation**: Users can only access their own profiles, balances, transactions
- **Public Data Access**: Collectibles and price history are publicly readable
- **Authenticated Operations**: Only logged-in users can create/modify data  
- **Referral Security**: Users can only see referrals they're involved in
- **Transaction Privacy**: Users can only see their own transaction history

## Key Changes Made:
- Changed `set` to `set_name` (set is a reserved word in PostgreSQL)
- Removed all comments from SQL
- Separated each command into individual blocks
- Added production-ready RLS policies for data security
- Clean formatting without special characters
