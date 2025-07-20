# 🗄️ Database Usage Guide

## 🎯 **How to Use Your Token Market Database**

Your database is **production-ready** and supports multiple access methods:

---

## 🚀 **Method 1: FastAPI Endpoints (Recommended for Apps)**

### **Interactive Documentation**
Visit: `http://localhost:8000/docs` for a complete interactive API interface!

### **Basic Usage Flow:**
```javascript
// 1. Register/Login to get JWT token
const loginResponse = await fetch('http://localhost:8000/auth/login', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    email: 'user@example.com',
    password: 'password123'
  })
});
const {access_token} = await loginResponse.json();

// 2. Use token for protected endpoints
const balanceResponse = await fetch('http://localhost:8000/profile/balance', {
  headers: {'Authorization': `Bearer ${access_token}`}
});
const balance = await balanceResponse.json();
```

---

## 🐍 **Method 2: Python Client (Your Demo Script)**

Run: `python database_usage_demo.py`

**Features:**
- ✅ User registration with JWT
- ✅ Secure authentication  
- ✅ Protected data access
- ✅ Public data browsing

---

## 🔧 **Method 3: Direct Database Access**

```python
from app.database import supabase
from app.db_service import DatabaseService

# Using the service layer (recommended)
db_service = DatabaseService()
user_result = await db_service.create_user_with_jwt(email, password, username)

# Direct Supabase queries
users = supabase.table("users").select("*").execute()
collectibles = supabase.table("collectibles").select("*").execute()
```

---

## 📊 **Database Schema - 7 Tables**

| Table | Purpose | Access Level |
|-------|---------|--------------|
| `users` | User accounts | Protected (RLS) |
| `token_balances` | User token holdings | Protected (RLS) |
| `transactions` | Purchase/sale records | Protected (RLS) |
| `collectibles` | Marketplace items | Public |
| `price_history` | Historical pricing | Public |
| `referrals` | Referral tracking | Protected (RLS) |
| `redemptions` | Token redemptions | Protected (RLS) |

---

## 🔐 **Authentication & Security**

### **JWT Token Flow:**
1. **Register/Login** → Get JWT token
2. **Add to headers** → `Authorization: Bearer <token>`
3. **Access protected data** → Automatic user identification

### **Row Level Security (RLS):**
- Users can **only see their own** transactions, balances, referrals
- **Public data** (collectibles, price history) accessible to all
- **Database-level security** - impossible to bypass

---

## 🎮 **Common Use Cases**

### **Frontend Integration:**
```javascript
// React/Vue/Angular example
const api = axios.create({
  baseURL: 'http://localhost:8000',
  headers: {
    'Authorization': `Bearer ${localStorage.getItem('jwt_token')}`
  }
});

// Get user balance
const balance = await api.get('/profile/balance');

// Browse collectibles
const items = await api.get('/collectibles');
```

### **Mobile App Integration:**
```swift
// iOS Swift example
let headers = ["Authorization": "Bearer \(jwtToken)"]
let request = URLRequest(url: URL(string: "http://localhost:8000/profile/balance")!)
request.allHTTPHeaderFields = headers
```

### **Backend-to-Backend:**
```python
# Another service calling your API
import requests

response = requests.post('http://localhost:8000/auth/login', json={
    'email': 'service@example.com',
    'password': 'service_password'
})
token = response.json()['access_token']

# Use token for subsequent requests
headers = {'Authorization': f'Bearer {token}'}
user_data = requests.get('http://localhost:8000/profile/balance', headers=headers)
```

---

## 🚀 **Deployment Ready**

### **Local Development:**
```bash
python start.py dev    # Tests + server
```

### **Docker Deployment:**
```bash
docker-compose up --build
```

### **Production Deployment:**
Your database works with:
- ✅ Vercel/Netlify Functions
- ✅ Railway/Render
- ✅ AWS/GCP/Azure
- ✅ Kubernetes
- ✅ Traditional servers

---

## 📈 **Next Steps**

1. **Frontend Integration** - Connect your UI to the API endpoints
2. **Add More Endpoints** - Extend `app/api.py` for new features  
3. **Business Logic** - Add custom functions to `app/db_service.py`
4. **Testing** - Expand test coverage in test files
5. **Monitoring** - Add logging and metrics
6. **Caching** - Add Redis for performance

**Your database is ready for production use!** 🎯
