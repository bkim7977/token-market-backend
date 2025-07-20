#!/bin/bash
# 🌐 BASH/CURL API Usage Examples
# Complete demonstration of HTTP API endpoints

echo "🚀 TOKEN MARKET API - BASH/CURL EXAMPLES"
echo "========================================"

# Make sure server is running
echo "📡 Testing server connection..."
if ! curl -s "http://localhost:8000/" > /dev/null; then
    echo "❌ Server not running! Start with: python start.py serve"
    exit 1
fi
echo "✅ Server is running!"

# Generate unique user
TIMESTAMP=$(date +%s)
USER_EMAIL="bash_user_${TIMESTAMP}@example.com"
USER_NAME="bash_user_${TIMESTAMP}"

echo -e "\n1️⃣  REGISTERING NEW USER"
echo "========================"
echo "📧 Email: $USER_EMAIL"

curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d "{
    \"email\": \"$USER_EMAIL\",
    \"password\": \"SecurePassword123!\",
    \"username\": \"$USER_NAME\"
  }" \
  -w "\nStatus Code: %{http_code}\n"

echo -e "\n\n2️⃣  USER LOGIN"
echo "==============="

# Login and extract token
LOGIN_RESPONSE=$(curl -s -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d "{
    \"email\": \"$USER_EMAIL\",
    \"password\": \"SecurePassword123!\"
  }")

echo "$LOGIN_RESPONSE" | jq '.' 2>/dev/null || echo "$LOGIN_RESPONSE"

# Extract access token (requires jq)
if command -v jq > /dev/null; then
    ACCESS_TOKEN=$(echo "$LOGIN_RESPONSE" | jq -r '.access_token // empty')
else
    echo "⚠️  Install 'jq' for automatic token extraction: brew install jq"
    echo "For now, copy the access_token from the response above"
    echo "Enter your access token:"
    read ACCESS_TOKEN
fi

if [ ! -z "$ACCESS_TOKEN" ] && [ "$ACCESS_TOKEN" != "null" ]; then
    echo "🔑 Access Token: ${ACCESS_TOKEN:0:50}..."
    
    echo -e "\n\n3️⃣  PROTECTED ENDPOINT ACCESS"
    echo "=============================="
    
    echo "👤 Getting user profile..."
    curl -X GET "http://localhost:8000/profile" \
      -H "Authorization: Bearer $ACCESS_TOKEN" \
      -w "\nStatus Code: %{http_code}\n"
    
    echo -e "\n💰 Getting user balance..."
    curl -X GET "http://localhost:8000/profile/balance" \
      -H "Authorization: Bearer $ACCESS_TOKEN" \
      -w "\nStatus Code: %{http_code}\n"
      
else
    echo "❌ Failed to get access token. Check login response above."
fi

echo -e "\n\n4️⃣  PUBLIC DATA ACCESS"
echo "======================"

echo "🏪 Getting all collectibles (public endpoint)..."
curl -X GET "http://localhost:8000/collectibles" \
  -w "\nStatus Code: %{http_code}\n"

echo -e "\n\n5️⃣  API DOCUMENTATION"
echo "====================="
echo "📚 Interactive API docs: http://localhost:8000/docs"
echo "📖 ReDoc documentation: http://localhost:8000/redoc"

echo -e "\n✅ BASH/CURL EXAMPLES COMPLETE!"
echo "🐍 Try Python examples: python api_usage_examples.py"
echo "📝 Full guide: python python_database_access_guide.py"
