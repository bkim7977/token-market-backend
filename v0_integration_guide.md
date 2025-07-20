# 🚀 V0 Frontend Integration Guide

Your Token Market backend is **100% compatible** with v0.dev frontends! Here's everything you need to know:

## ✅ Why It Works Perfectly

- **REST API**: v0 generates modern React/Next.js apps that work seamlessly with REST APIs
- **JWT Authentication**: Standard Bearer token authentication that v0 components handle naturally  
- **CORS Enabled**: Your backend already allows frontend connections
- **JSON Responses**: Clean, predictable API responses that v0 components expect

## 🎯 Integration Steps for v0

### 1. **Use These API Endpoints in v0**

```typescript
// Base configuration for v0 components
const API_BASE = 'http://localhost:8000';

// Authentication endpoints
POST /auth/register  // User registration
POST /auth/login     // User login

// Protected endpoints (require JWT token)
GET /profile/balance // User balance and profile

// Public endpoints  
GET /collectibles    // Marketplace items
```

### 2. **Authentication Pattern for v0**

```typescript
// Login function for v0 components
const login = async (email: string, password: string) => {
  const response = await fetch('http://localhost:8000/auth/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ email, password }),
  });
  
  const data = await response.json();
  localStorage.setItem('token', data.access_token);
  return data;
};

// Protected API calls in v0
const fetchUserBalance = async () => {
  const token = localStorage.getItem('token');
  const response = await fetch('http://localhost:8000/profile/balance', {
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
  });
  return response.json();
};
```

### 3. **v0 Prompt Examples**

When creating components in v0, use these prompts:

**Authentication Component:**
```
Create a modern login/register form component with:
- Email and password fields
- Toggle between login/register modes  
- JWT token storage in localStorage
- Error handling for failed requests
- API calls to http://localhost:8000/auth/login and /auth/register
- Store access_token from response in localStorage
```

**User Dashboard:**
```
Create a user dashboard component that:
- Shows user balance and profile info
- Fetches data from http://localhost:8000/profile/balance
- Uses Bearer token authentication from localStorage  
- Displays loading and error states
- Has a logout button that clears localStorage
```

**Marketplace Component:**
```
Create a collectibles marketplace component that:
- Fetches items from http://localhost:8000/collectibles
- Displays items in a responsive grid
- Shows name, set_name, rarity, and current_price for each item
- Includes search and filter functionality
- Modern card-based design
```

### 4. **Data Structures for v0**

Your backend returns these exact formats that v0 can use:

```typescript
// Login/Register Response
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "username": "john_doe", 
    "email": "john@example.com"
  }
}

// User Balance Response  
{
  "balance": 1000,
  "user_id": 1
}

// Collectibles Response
[
  {
    "id": 1,
    "name": "Charizard",
    "set_name": "Base Set",
    "rarity": "Rare",
    "current_price": 150.00
  }
]
```

### 5. **Environment Variables for v0**

Add to your v0 project's environment:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

Then use in components:
```typescript
const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
```

## 🎨 v0 Component Templates

### Complete v0-Ready Authentication Hook

```typescript
// Custom hook for v0 authentication
import { useState, useEffect } from 'react';

export const useAuth = () => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const storedToken = localStorage.getItem('token');
    if (storedToken) {
      setToken(storedToken);
      fetchUserProfile(storedToken);
    }
  }, []);

  const login = async (email: string, password: string) => {
    setLoading(true);
    try {
      const response = await fetch('http://localhost:8000/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      });
      
      const data = await response.json();
      if (response.ok) {
        localStorage.setItem('token', data.access_token);
        setToken(data.access_token);
        setUser(data.user);
        return { success: true, data };
      } else {
        return { success: false, error: data.detail };
      }
    } catch (error) {
      return { success: false, error: 'Network error' };
    } finally {
      setLoading(false);
    }
  };

  const logout = () => {
    localStorage.removeItem('token');
    setToken(null);
    setUser(null);
  };

  return { user, token, login, logout, loading };
};
```

## 🚀 v0 Integration Checklist

- ✅ **API Base URL**: `http://localhost:8000` 
- ✅ **Authentication**: Bearer token in Authorization header
- ✅ **Content-Type**: `application/json` for all requests
- ✅ **CORS**: Already configured in your backend
- ✅ **Error Handling**: Standard HTTP status codes and JSON error responses
- ✅ **Data Format**: Clean JSON responses ready for v0 components

## 🎯 Quick Start with v0

1. **Start your backend**: `python start.py serve`
2. **Create v0 components** using the patterns above
3. **Test authentication** with the login/register endpoints  
4. **Fetch data** from the collectibles and profile endpoints
5. **Deploy** both backend and v0 frontend when ready

## 📱 v0 Component Ideas

Perfect v0 prompts for your Token Market:

- **"Create a crypto wallet dashboard with balance display and transaction history"**
- **"Build a NFT marketplace with card grid, filters, and purchase buttons"** 
- **"Design a user profile page with avatar, stats, and account settings"**
- **"Make a trading interface with buy/sell orders and price charts"**

## 🔧 Production Deployment

When deploying your v0 frontend:

1. **Update API_BASE** to your production backend URL
2. **Configure CORS** in your backend for the frontend domain
3. **Use HTTPS** for both frontend and backend in production
4. **Environment variables** for API URLs in v0/Next.js

Your backend is **production-ready** and will work seamlessly with any v0-generated frontend! 🚀

---

**Need help with specific v0 components?** Just ask! I can provide exact prompts and code examples for any UI you want to build.
