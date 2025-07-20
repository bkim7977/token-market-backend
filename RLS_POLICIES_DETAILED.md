# Row Level Security Policies for Token Market Backend

Execute these policies in your Supabase SQL Editor after creating the tables.

## Basic RLS Policies

### 1. Collectibles - Public Read, Admin Write
```sql
CREATE POLICY "Anyone can view collectibles" ON collectibles
FOR SELECT USING (true);

CREATE POLICY "Only authenticated users can insert collectibles" ON collectibles
FOR INSERT WITH CHECK (auth.role() = 'authenticated');

CREATE POLICY "Only authenticated users can update collectibles" ON collectibles
FOR UPDATE USING (auth.role() = 'authenticated');
```

### 2. Users - Users can only see/edit their own data
```sql
CREATE POLICY "Users can view their own profile" ON users
FOR SELECT USING (auth.uid() = id);

CREATE POLICY "Users can insert their own profile" ON users
FOR INSERT WITH CHECK (auth.uid() = id);

CREATE POLICY "Users can update their own profile" ON users
FOR UPDATE USING (auth.uid() = id);
```

### 3. Token Balances - Users can only see their own balance
```sql
CREATE POLICY "Users can view their own balance" ON token_balances
FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own balance" ON token_balances
FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own balance" ON token_balances
FOR UPDATE USING (auth.uid() = user_id);
```

### 4. Transactions - Users can see their own transactions
```sql
CREATE POLICY "Users can view their own transactions" ON transactions
FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own transactions" ON transactions
FOR INSERT WITH CHECK (auth.uid() = user_id);
```

### 5. Price History - Public Read
```sql
CREATE POLICY "Anyone can view price history" ON price_history
FOR SELECT USING (true);

CREATE POLICY "Authenticated users can insert price history" ON price_history
FOR INSERT WITH CHECK (auth.role() = 'authenticated');
```

### 6. Referrals - Users can see referrals they're involved in
```sql
CREATE POLICY "Users can view referrals they're involved in" ON referrals
FOR SELECT USING (auth.uid() = referrer_id OR auth.uid() = referred_id);

CREATE POLICY "Users can create referrals" ON referrals
FOR INSERT WITH CHECK (auth.uid() = referrer_id);
```

### 7. Redemptions - Users can see their own redemptions
```sql
CREATE POLICY "Users can view their own redemptions" ON redemptions
FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can create redemptions" ON redemptions
FOR INSERT WITH CHECK (auth.uid() = user_id);
```

## Alternative: Simpler Development Policies

If you want to start simpler for development, use these instead:

### Allow all operations for authenticated users
```sql
CREATE POLICY "Allow all for authenticated users" ON users
FOR ALL USING (auth.role() = 'authenticated');

CREATE POLICY "Allow all for authenticated users" ON collectibles
FOR ALL USING (auth.role() = 'authenticated');

CREATE POLICY "Allow all for authenticated users" ON token_balances
FOR ALL USING (auth.role() = 'authenticated');

CREATE POLICY "Allow all for authenticated users" ON price_history
FOR ALL USING (auth.role() = 'authenticated');

CREATE POLICY "Allow all for authenticated users" ON transactions
FOR ALL USING (auth.role() = 'authenticated');

CREATE POLICY "Allow all for authenticated users" ON referrals
FOR ALL USING (auth.role() = 'authenticated');

CREATE POLICY "Allow all for authenticated users" ON redemptions
FOR ALL USING (auth.role() = 'authenticated');
```

### Allow public read access to collectibles and price history
```sql
CREATE POLICY "Public read access" ON collectibles
FOR SELECT USING (true);

CREATE POLICY "Public read access" ON price_history
FOR SELECT USING (true);
```
