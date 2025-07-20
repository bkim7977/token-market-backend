# 💖 Lovable Frontend Integration Guide

Your Token Market backend is **100% compatible** with Lovable-generated frontends! Here's the complete integration guide:

## ✅ Why It Works Perfectly with Lovable

- **React/TypeScript**: Lovable generates modern React apps that work seamlessly with REST APIs
- **JWT Authentication**: Standard Bearer token pattern that Lovable components handle naturally
- **Clean API Design**: RESTful endpoints that integrate smoothly with Lovable's fetch patterns
- **TypeScript Ready**: Your API responses are predictable and type-safe
- **Modern Architecture**: Follows patterns that Lovable generates code for

## 🚀 Quick Integration Steps

### 1. **Replace Lovable's API Configuration**

In your Lovable project, find the API configuration file (usually `src/lib/api.ts` or similar):

```typescript
// Replace with your Token Market backend
const API_BASE_URL = 'http://localhost:8000';

// Authentication helper
const getAuthHeaders = () => {
  const token = localStorage.getItem('token');
  return token ? { Authorization: `Bearer ${token}` } : {};
};

// API client configuration
export const api = {
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
    ...getAuthHeaders(),
  },
};
```

### 2. **Update Authentication Functions**

Replace Lovable's auth functions with these Token Market compatible ones:

```typescript
// src/lib/auth.ts
export interface User {
  id: number;
  username: string;
  email: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
  user: User;
}

export const authAPI = {
  async login(email: string, password: string): Promise<LoginResponse> {
    const response = await fetch(`${API_BASE_URL}/auth/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email, password }),
    });
    
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Login failed');
    }
    
    const data = await response.json();
    localStorage.setItem('token', data.access_token);
    return data;
  },

  async register(username: string, email: string, password: string): Promise<LoginResponse> {
    const response = await fetch(`${API_BASE_URL}/auth/register`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ username, email, password }),
    });
    
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Registration failed');
    }
    
    const data = await response.json();
    localStorage.setItem('token', data.access_token);
    return data;
  },

  logout() {
    localStorage.removeItem('token');
  },

  async getUserBalance() {
    const token = localStorage.getItem('token');
    if (!token) throw new Error('No token found');
    
    const response = await fetch(`${API_BASE_URL}/profile/balance`, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
    });
    
    if (!response.ok) {
      if (response.status === 401) {
        localStorage.removeItem('token');
        throw new Error('Session expired');
      }
      throw new Error('Failed to fetch balance');
    }
    
    return response.json();
  },
};
```

### 3. **Update Data Fetching Functions**

Replace Lovable's data fetching with Token Market endpoints:

```typescript
// src/lib/collectibles.ts
export interface Collectible {
  id: number;
  name: string;
  set_name: string;
  rarity: string;
  current_price: number;
}

export const collectiblesAPI = {
  async getAll(): Promise<Collectible[]> {
    const response = await fetch(`${API_BASE_URL}/collectibles`);
    
    if (!response.ok) {
      throw new Error('Failed to fetch collectibles');
    }
    
    return response.json();
  },
};
```

### 4. **Replace React Hook/Context**

If your Lovable app uses React Context for state management, update it:

```typescript
// src/contexts/AuthContext.tsx
import React, { createContext, useContext, useEffect, useState } from 'react';
import { authAPI, User } from '../lib/auth';

interface AuthContextType {
  user: User | null;
  balance: number | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (username: string, email: string, password: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | null>(null);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [balance, setBalance] = useState<number | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      fetchUserData();
    } else {
      setLoading(false);
    }
  }, []);

  const fetchUserData = async () => {
    try {
      const data = await authAPI.getUserBalance();
      setBalance(data.balance);
      // You might need to fetch user info separately or include it in balance response
      setUser(data.user || { username: 'User', email: '', id: data.user_id });
    } catch (error) {
      console.error('Error fetching user data:', error);
      localStorage.removeItem('token');
    } finally {
      setLoading(false);
    }
  };

  const login = async (email: string, password: string) => {
    const response = await authAPI.login(email, password);
    setUser(response.user);
    await fetchUserData();
  };

  const register = async (username: string, email: string, password: string) => {
    const response = await authAPI.register(username, email, password);
    setUser(response.user);
    await fetchUserData();
  };

  const logout = () => {
    authAPI.logout();
    setUser(null);
    setBalance(null);
  };

  return (
    <AuthContext.Provider value={{ user, balance, loading, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
```

### 5. **Update Your Lovable Components**

Replace the component logic in your Lovable-generated files with Token Market integration:

```typescript
// In your main component (e.g., Dashboard.tsx, App.tsx)
import React, { useEffect, useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { collectiblesAPI, Collectible } from '../lib/collectibles';

export const Dashboard: React.FC = () => {
  const { user, balance, logout } = useAuth();
  const [collectibles, setCollectibles] = useState<Collectible[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchCollectibles();
  }, []);

  const fetchCollectibles = async () => {
    setLoading(true);
    try {
      const data = await collectiblesAPI.getAll();
      setCollectibles(data);
    } catch (error) {
      console.error('Error fetching collectibles:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mx-auto p-6">
      {user && (
        <div className="bg-gradient-to-r from-blue-500 to-purple-600 text-white p-6 rounded-lg mb-6">
          <h2 className="text-2xl font-bold">Welcome, {user.username}! 👋</h2>
          <p>📧 {user.email}</p>
          {balance !== null && (
            <p>💰 Balance: <strong>{balance} tokens</strong></p>
          )}
          <button 
            onClick={logout}
            className="mt-4 bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded"
          >
            Logout
          </button>
        </div>
      )}

      <div className="mb-6">
        <h2 className="text-2xl font-bold mb-4">🏪 Marketplace</h2>
        <p className="text-gray-600">{collectibles.length} collectibles available</p>
      </div>

      {loading ? (
        <div className="text-center">Loading collectibles...</div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {collectibles.map((item) => (
            <div 
              key={item.id} 
              className="bg-white border rounded-lg p-6 shadow-md hover:shadow-lg transition-shadow"
            >
              <h3 className="text-xl font-semibold mb-2">{item.name}</h3>
              <p className="text-gray-600 mb-1">
                <strong>Set:</strong> {item.set_name}
              </p>
              <p className="text-gray-600 mb-3">
                <strong>Rarity:</strong> {item.rarity}
              </p>
              <p className="text-2xl font-bold text-green-600">
                ${item.current_price}
              </p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
```

## 🎯 Lovable-Specific Integration Tips

### **Environment Variables**
Add to your `.env.local` file in your Lovable project:
```env
REACT_APP_API_URL=http://localhost:8000
```

Then use it in your code:
```typescript
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
```

### **TypeScript Types**
Create a `types.ts` file for better TypeScript support:
```typescript
// src/types/index.ts
export interface User {
  id: number;
  username: string;
  email: string;
}

export interface Collectible {
  id: number;
  name: string;
  set_name: string;
  rarity: string;
  current_price: number;
}

export interface UserBalance {
  balance: number;
  user_id: number;
  user?: User;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: User;
}
```

### **Error Handling**
Add proper error handling for Lovable's UI patterns:
```typescript
const [error, setError] = useState<string | null>(null);

// In your API calls
try {
  // API call
} catch (err) {
  setError(err instanceof Error ? err.message : 'An error occurred');
}

// In your JSX
{error && (
  <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
    {error}
  </div>
)}
```

## 🚀 Quick Start Checklist

- [ ] Start your backend: `python start.py serve`
- [ ] Update API_BASE_URL to `http://localhost:8000`
- [ ] Replace auth functions with Token Market endpoints
- [ ] Update data fetching to use `/collectibles` and `/profile/balance`
- [ ] Add JWT token to Authorization headers
- [ ] Test login, registration, and data fetching
- [ ] Update TypeScript types to match your API responses

## 📱 Production Deployment

When deploying your Lovable app:
1. Update API_BASE_URL to your production backend URL
2. Ensure your backend CORS settings include your Lovable app's domain
3. Use HTTPS for both frontend and backend
4. Set environment variables in your Lovable deployment settings

Your Token Market backend is **perfectly compatible** with Lovable's modern React architecture! 🎨✨
