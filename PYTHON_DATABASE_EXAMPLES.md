# 🐍 PYTHON DATABASE ACCESS - COMPLETE EXAMPLES

## 📋 **Overview**
Your Token Market backend supports **4 different ways** to access data in Python, each optimized for different use cases.

---

## 🌐 **Method 1: HTTP API Client (Recommended)**

### **Use Cases:** 
- Web applications (React, Vue, Angular)
- Mobile apps (iOS, Android)
- Microservices
- Third-party integrations

### **Python Example:**
```python
import requests

class TokenMarketClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.access_token = None
    
    def login(self, email, password):
        response = requests.post(f"{self.base_url}/auth/login", 
                               json={"email": email, "password": password})
        if response.status_code == 200:
            data = response.json()
            self.access_token = data["access_token"]
            return data
        return None
    
    def get_balance(self):
        headers = {"Authorization": f"Bearer {self.access_token}"}
        response = requests.get(f"{self.base_url}/profile/balance", headers=headers)
        return response.json()

# Usage
client = TokenMarketClient()
client.login("user@example.com", "password123")
balance = client.get_balance()
```

### **Available Scripts:**
- `python api_usage_examples.py` - Complete HTTP examples
- `python database_usage_demo.py` - Advanced usage patterns

---

## 🔧 **Method 2: Database Service Layer**

### **Use Cases:**
- Backend services within your application
- Internal microservices
- Data processing scripts
- Admin tools

### **Python Example:**
```python
from app.db_service import DatabaseService
import asyncio

async def main():
    db = DatabaseService()
    
    # Create user
    user = await db.create_user_with_jwt("user@example.com", "password123", "username")
    
    # Authenticate
    auth = await db.authenticate_user_jwt("user@example.com", "password123")
    
    # Get balance
    user_id = auth['user']['user_id']
    balance = await db.get_user_balance(user_id)
    
    return balance

balance = asyncio.run(main())
```

---

## 🗄️ **Method 3: Direct Supabase Access**

### **Use Cases:**
- Database migrations
- Bulk data operations
- Analytics queries
- Administrative tasks

### **Python Example:**
```python
from app.database import supabase
from app.auth import hash_password
import uuid

# Create user directly
user_id = str(uuid.uuid4())
password_hash = hash_password("password123")

result = supabase.table("users").insert({
    "user_id": user_id,
    "email": "direct@example.com",
    "username": "direct_user",
    "password_hash": password_hash
}).execute()

# Query data
users = supabase.table("users").select("*").eq("email", "direct@example.com").execute()
collectibles = supabase.table("collectibles").select("*").limit(10).execute()
```

---

## 📡 **Method 4: Raw HTTP Requests**

### **Use Cases:**
- Universal approach for any language
- Debugging and testing
- Simple scripts without dependencies
- Integration with non-Python systems

### **Python Example:**
```python
import urllib.request
import json

# Login
login_data = {"email": "user@example.com", "password": "password123"}
req = urllib.request.Request(
    "http://localhost:8000/auth/login",
    data=json.dumps(login_data).encode('utf-8'),
    headers={'Content-Type': 'application/json'}
)

with urllib.request.urlopen(req) as response:
    result = json.loads(response.read().decode('utf-8'))
    access_token = result["access_token"]

# Protected request
req = urllib.request.Request(
    "http://localhost:8000/profile/balance",
    headers={'Authorization': f'Bearer {access_token}'}
)

with urllib.request.urlopen(req) as response:
    balance = json.loads(response.read().decode('utf-8'))
```

### **Bash/cURL Alternative:**
```bash
# Also works with cURL for any language
./api_usage_examples.sh
```

---

## 🚀 **Running the Examples**

### **1. Start the Server:**
```bash
python start.py serve
```

### **2. Run Python Examples:**
```bash
# Method 1: HTTP API Client
python api_usage_examples.py

# All 4 methods demonstration
python python_database_access_guide.py

# Advanced usage demo
python database_usage_demo.py

# Direct database examples
python direct_database_demo.py
```

### **3. Run Bash Examples:**
```bash
# HTTP API with cURL
./api_usage_examples.sh
```

---

## 📊 **Method Comparison**

| Method | Speed | Security | Complexity | Best For |
|--------|-------|----------|------------|----------|
| HTTP API Client | ⚡⚡⚡ | 🔐🔐🔐 | 🟢 Simple | Web/Mobile Apps |
| Service Layer | ⚡⚡⚡⚡ | 🔐🔐🔐🔐 | 🟡 Medium | Backend Services |
| Direct Supabase | ⚡⚡⚡⚡⚡ | 🔐🔐🔐🔐🔐 | 🔴 Advanced | Admin/Analytics |
| Raw HTTP | ⚡⚡ | 🔐🔐🔐 | 🟢 Simple | Universal Use |

---

## 🔐 **Authentication Examples**

### **JWT Token Flow:**
```python
# 1. Register/Login
response = requests.post('http://localhost:8000/auth/login', 
                        json={'email': 'user@example.com', 'password': 'password123'})
token = response.json()['access_token']

# 2. Use token in headers
headers = {'Authorization': f'Bearer {token}'}

# 3. Access protected endpoints
balance = requests.get('http://localhost:8000/profile/balance', headers=headers)
profile = requests.get('http://localhost:8000/profile', headers=headers)
```

### **Password Hashing:**
```python
from app.auth import hash_password, verify_password

# Hash password for storage
hashed = hash_password("user_password")

# Verify password
is_valid = verify_password("user_password", hashed)
```

---

## 🎯 **Production Ready Examples**

### **Error Handling:**
```python
import requests

def safe_api_call(url, headers=None):
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raises exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"API Error: {e}")
        return None
    except ValueError as e:
        print(f"JSON Error: {e}")
        return None
```

### **Token Refresh Logic:**
```python
class TokenManager:
    def __init__(self):
        self.token = None
        self.expires_at = None
    
    def is_token_valid(self):
        return self.token and self.expires_at > datetime.now()
    
    def refresh_token_if_needed(self):
        if not self.is_token_valid():
            self.login()
    
    def api_call(self, url, data=None):
        self.refresh_token_if_needed()
        headers = {'Authorization': f'Bearer {self.token}'}
        return requests.get(url, headers=headers, json=data)
```

---

## 📚 **Next Steps**

1. **Choose Your Method** based on your use case
2. **Test with Examples** - Run the provided scripts
3. **Integrate into Your App** - Use the patterns shown
4. **Add Error Handling** - Implement proper exception handling
5. **Scale as Needed** - Add caching, retry logic, etc.

### **Documentation:**
- **Interactive API Docs:** `http://localhost:8000/docs`
- **Complete Guide:** `DATABASE_USAGE.md`
- **Live Examples:** All Python scripts in the project

**Your database is ready for any Python application!** 🚀
