# Additional RLS Policies for Testing

Add these policies to your Supabase SQL Editor to allow basic operations:

## Allow all operations for authenticated users (temporary for testing)

```sql
CREATE POLICY "Enable all operations for authenticated users" ON users
FOR ALL USING (true) WITH CHECK (true);
```

```sql
CREATE POLICY "Enable all operations for authenticated users" ON collectibles
FOR ALL USING (true) WITH CHECK (true);
```

```sql
CREATE POLICY "Enable all operations for authenticated users" ON token_balances
FOR ALL USING (true) WITH CHECK (true);
```

```sql
CREATE POLICY "Enable all operations for authenticated users" ON price_history
FOR ALL USING (true) WITH CHECK (true);
```

```sql
CREATE POLICY "Enable all operations for authenticated users" ON transactions
FOR ALL USING (true) WITH CHECK (true);
```

```sql
CREATE POLICY "Enable all operations for authenticated users" ON referrals
FOR ALL USING (true) WITH CHECK (true);
```

```sql
CREATE POLICY "Enable all operations for authenticated users" ON redemptions
FOR ALL USING (true) WITH CHECK (true);
```

## OR disable RLS temporarily for testing:

```sql
ALTER TABLE users DISABLE ROW LEVEL SECURITY;
ALTER TABLE collectibles DISABLE ROW LEVEL SECURITY;
ALTER TABLE token_balances DISABLE ROW LEVEL SECURITY;
ALTER TABLE price_history DISABLE ROW LEVEL SECURITY;
ALTER TABLE transactions DISABLE ROW LEVEL SECURITY;
ALTER TABLE referrals DISABLE ROW LEVEL SECURITY;
ALTER TABLE redemptions DISABLE ROW LEVEL SECURITY;
```

You can re-enable RLS later when you implement proper authentication.
