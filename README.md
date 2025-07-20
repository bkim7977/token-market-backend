# 🪙 Token Market Backend

**Production-ready backend for token trading marketplace with JWT authentication, database security, and comprehensive API.**

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Latest-green.svg)](https://fastapi.tiangolo.com/)
[![Supabase](https://img.shields.io/badge/Supabase-Database-orange.svg)](https://supabase.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)

---

## 🚀 **Quick Start**

```bash
# Clone and setup
git clone <your-repo>
cd token_market_backend

# Configure environment
cp .env.example .env
# Edit .env with your Supabase credentials

# Install dependencies
pip install -r requirements-minimal.txt

# Development mode (runs tests + starts server)
python start.py dev
```

**API Documentation:** `http://localhost:8000/docs`

---

## ✨ **Features**

### **🔐 Authentication & Security**
- **JWT Authentication** with secure token generation
- **Password Hashing** using bcrypt
- **Row Level Security (RLS)** for data protection  
- **Protected Routes** with automatic user identification

### **💾 Database Architecture**
- **7 Production Tables** (users, transactions, collectibles, etc.)
- **Cloud PostgreSQL** via Supabase
- **Automatic Migrations** and schema management
- **Real-time Capabilities** (Supabase features)

### **🌐 API Features** 
- **RESTful Endpoints** with FastAPI
- **Interactive Documentation** at `/docs`
- **CORS Support** for frontend integration
- **Error Handling** and validation

### **🧪 Testing & Quality**
- **Comprehensive Test Suite** (JWT, RLS, API tests)
- **100% Authentication Coverage**
- **Production-Ready Code Quality**

### **🐳 Deployment Ready**
- **Docker Configuration** with compose
- **Environment Management** with .env
- **Production Optimization** settings
- **Cloud Platform Compatible**

---

## 📋 **API Endpoints**

### **🔓 Public Endpoints**
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Health check |
| `POST` | `/auth/register` | Create new account |
| `POST` | `/auth/login` | Authenticate user |
| `GET` | `/collectibles` | Browse marketplace |
| `GET` | `/collectibles/{id}` | Item details |

### **🔐 Protected Endpoints** (Requires JWT)
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/profile` | User profile |
| `GET` | `/profile/balance` | Token balance |
| `GET` | `/profile/transactions` | Transaction history |
| `POST` | `/profile/purchase` | Buy collectible |

---

## 🗄️ **Database Schema**

```sql
users              # User accounts with JWT support
├── user_id        # UUID primary key  
├── email          # Unique login credential
├── username       # Display name
├── password_hash  # Bcrypt secured
└── created_at     # Registration timestamp

token_balances     # User token holdings
├── balance_id     # UUID primary key
├── user_id        # Foreign key to users
├── amount         # Current token balance
└── last_updated   # Balance update timestamp

collectibles       # Marketplace items  
├── collectible_id # UUID primary key
├── name           # Item name
├── description    # Item description
├── current_price  # Current market price
└── created_at     # Listing timestamp

transactions       # Purchase/sale records
├── transaction_id # UUID primary key
├── user_id        # Foreign key to users
├── collectible_id # Foreign key to collectibles
├── amount         # Transaction amount
├── type           # purchase/sale/transfer
└── created_at     # Transaction timestamp

# Additional tables: price_history, referrals, redemptions
```

---

## 🛠️ **Development**

### **Available Commands**
```bash
# Development workflow
python start.py dev         # Tests + server (recommended)
python start.py test        # Run all tests
python start.py test-jwt    # JWT authentication tests only  
python start.py serve       # Start API server only

# Testing & validation
python start.py simple-test      # Basic database connectivity
python start.py test-rls         # Row Level Security validation
python database_usage_demo.py    # API usage demonstration
python direct_database_demo.py   # Direct database examples
```

---

## ⚙️ **Configuration**

### **Environment Variables** (.env)
```bash
# Supabase Configuration
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key

# JWT Configuration  
JWT_SECRET_KEY=your-super-secret-jwt-key
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=30

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
```

---

## 🧪 **Testing**

### **Run All Tests**
```bash
python start.py test
```

### **Test Categories**
- **JWT Authentication** - Registration, login, protected routes
- **Database Connectivity** - Supabase connection and basic operations  
- **Row Level Security** - Data access permissions
- **API Integration** - Complete HTTP request/response cycle

### **Test Results Example**
```
✅ JWT Registration: SUCCESS
✅ JWT Login: SUCCESS  
✅ Protected Access: SUCCESS
✅ Public Access: SUCCESS
✅ Database Connection: SUCCESS
✅ User Creation: SUCCESS
✅ Token Balance: SUCCESS

ALL TESTS PASSED - System Ready! 🎯
```

---

## 🐳 **Deployment**

### **Docker (Recommended)**
```bash
# Build and run
docker-compose up --build
```

### **Cloud Platforms**
- **Railway** - `railway up` (auto-detection)
- **Render** - Connect GitHub repo  
- **Vercel** - Serverless functions
- **Heroku** - `git push heroku main`

---

## 🔧 **Usage Examples**

### **Frontend Integration (JavaScript)**
```javascript
// Authentication flow
const auth = await fetch('/auth/login', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({email: 'user@example.com', password: 'password123'})
});
const {access_token} = await auth.json();

// Authenticated requests  
const balance = await fetch('/profile/balance', {
  headers: {'Authorization': `Bearer ${access_token}`}
});
```

---

## 🎯 **Production Checklist**

- ✅ **JWT Authentication** - Secure token-based auth
- ✅ **Database Security** - Row Level Security implemented  
- ✅ **API Documentation** - Interactive docs at /docs
- ✅ **Comprehensive Testing** - All authentication flows tested
- ✅ **Docker Support** - Container-ready deployment  
- ✅ **Environment Configuration** - Secure credential management
- ✅ **CORS Support** - Frontend integration ready

**Your backend is production-ready!** 🚀

## Development Notes

- Uses Supabase REST API for reliable cloud database access
- RLS policies automatically enforce data isolation
- FastAPI provides automatic API documentation at `/docs`
- All endpoints use proper HTTP status codes and error handling

## API Documentation

When the server is running, visit:
- Interactive docs: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
