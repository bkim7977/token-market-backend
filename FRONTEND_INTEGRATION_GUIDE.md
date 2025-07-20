# 🌐 FRONTEND INTEGRATION GUIDE

## 🎯 **How to Connect Your Token Market Backend to Any Frontend**

Your backend is **frontend-agnostic** and works with any technology stack. Here's how to integrate it:

---

## 🚀 **QUICK START INTEGRATION**

### **1. Start Your Backend Server**
```bash
cd /Users/brian/token_market_backend
python start.py serve
```
**Your API is now available at:** `http://localhost:8000`

### **2. Test the Connection**
Visit: `http://localhost:8000/docs` for interactive testing

---

## ⚛️ **REACT INTEGRATION**

### **Frontend Setup**
```bash
npx create-react-app my-token-market-app
cd my-token-market-app
npm install axios  # or use fetch API
npm start
```

### **React Authentication Component**
```jsx
// src/components/Auth.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_BASE = 'http://localhost:8000';

function Auth() {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('token'));
  const [balance, setBalance] = useState(null);
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    username: ''
  });

  // Set up axios defaults with token
  useEffect(() => {
    if (token) {
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      fetchUserData();
    }
  }, [token]);

  const fetchUserData = async () => {
    try {
      const balanceResponse = await axios.get(`${API_BASE}/profile/balance`);
      setBalance(balanceResponse.data);
    } catch (error) {
      console.error('Error fetching user data:', error);
      // Token might be expired
      logout();
    }
  };

  const register = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post(`${API_BASE}/auth/register`, formData);
      const { access_token, user } = response.data;
      
      setToken(access_token);
      setUser(user);
      localStorage.setItem('token', access_token);
      
      alert('Registration successful!');
    } catch (error) {
      alert('Registration failed: ' + error.response?.data?.detail);
    }
  };

  const login = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post(`${API_BASE}/auth/login`, {
        email: formData.email,
        password: formData.password
      });
      const { access_token, user } = response.data;
      
      setToken(access_token);
      setUser(user);
      localStorage.setItem('token', access_token);
      
      alert('Login successful!');
    } catch (error) {
      alert('Login failed: ' + error.response?.data?.detail);
    }
  };

  const logout = () => {
    setToken(null);
    setUser(null);
    setBalance(null);
    localStorage.removeItem('token');
    delete axios.defaults.headers.common['Authorization'];
  };

  const handleInputChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  if (user) {
    return (
      <div>
        <h2>Welcome, {user.username}!</h2>
        <p>Email: {user.email}</p>
        {balance && <p>Balance: {balance.balance} tokens</p>}
        <button onClick={logout}>Logout</button>
      </div>
    );
  }

  return (
    <div>
      <h2>Token Market Authentication</h2>
      
      {/* Registration Form */}
      <form onSubmit={register}>
        <h3>Register</h3>
        <input
          type="text"
          name="username"
          placeholder="Username"
          value={formData.username}
          onChange={handleInputChange}
          required
        />
        <input
          type="email"
          name="email"
          placeholder="Email"
          value={formData.email}
          onChange={handleInputChange}
          required
        />
        <input
          type="password"
          name="password"
          placeholder="Password"
          value={formData.password}
          onChange={handleInputChange}
          required
        />
        <button type="submit">Register</button>
      </form>

      {/* Login Form */}
      <form onSubmit={login}>
        <h3>Login</h3>
        <input
          type="email"
          name="email"
          placeholder="Email"
          value={formData.email}
          onChange={handleInputChange}
          required
        />
        <input
          type="password"
          name="password"
          placeholder="Password"
          value={formData.password}
          onChange={handleInputChange}
          required
        />
        <button type="submit">Login</button>
      </form>
    </div>
  );
}

export default Auth;
```

### **Collectibles Component**
```jsx
// src/components/Collectibles.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_BASE = 'http://localhost:8000';

function Collectibles() {
  const [collectibles, setCollectibles] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchCollectibles();
  }, []);

  const fetchCollectibles = async () => {
    try {
      // Public endpoint - no authentication required
      const response = await axios.get(`${API_BASE}/collectibles`);
      setCollectibles(response.data);
    } catch (error) {
      console.error('Error fetching collectibles:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div>Loading collectibles...</div>;

  return (
    <div>
      <h2>Marketplace ({collectibles.length} items)</h2>
      <div className="collectibles-grid">
        {collectibles.map((item) => (
          <div key={item.id} className="collectible-card">
            <h3>{item.name}</h3>
            <p>Set: {item.set_name}</p>
            <p>Rarity: {item.rarity}</p>
            <p>Price: ${item.current_price}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Collectibles;
```

---

## 🖖 **VUE.JS INTEGRATION**

### **Vue Authentication Component**
```vue
<!-- src/components/Auth.vue -->
<template>
  <div>
    <div v-if="user">
      <h2>Welcome, {{ user.username }}!</h2>
      <p>Email: {{ user.email }}</p>
      <p v-if="balance">Balance: {{ balance.balance }} tokens</p>
      <button @click="logout">Logout</button>
    </div>
    
    <div v-else>
      <h2>Token Market Authentication</h2>
      
      <!-- Registration -->
      <form @submit.prevent="register">
        <h3>Register</h3>
        <input v-model="formData.username" type="text" placeholder="Username" required>
        <input v-model="formData.email" type="email" placeholder="Email" required>
        <input v-model="formData.password" type="password" placeholder="Password" required>
        <button type="submit">Register</button>
      </form>

      <!-- Login -->
      <form @submit.prevent="login">
        <h3>Login</h3>
        <input v-model="formData.email" type="email" placeholder="Email" required>
        <input v-model="formData.password" type="password" placeholder="Password" required>
        <button type="submit">Login</button>
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

const API_BASE = 'http://localhost:8000';

export default {
  name: 'Auth',
  data() {
    return {
      user: null,
      balance: null,
      formData: {
        email: '',
        password: '',
        username: ''
      }
    };
  },
  async created() {
    const token = localStorage.getItem('token');
    if (token) {
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      await this.fetchUserData();
    }
  },
  methods: {
    async fetchUserData() {
      try {
        const response = await axios.get(`${API_BASE}/profile/balance`);
        this.balance = response.data;
      } catch (error) {
        console.error('Error fetching user data:', error);
        this.logout();
      }
    },
    
    async register() {
      try {
        const response = await axios.post(`${API_BASE}/auth/register`, this.formData);
        const { access_token, user } = response.data;
        
        localStorage.setItem('token', access_token);
        axios.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;
        this.user = user;
        
        alert('Registration successful!');
        await this.fetchUserData();
      } catch (error) {
        alert('Registration failed: ' + error.response?.data?.detail);
      }
    },
    
    async login() {
      try {
        const response = await axios.post(`${API_BASE}/auth/login`, {
          email: this.formData.email,
          password: this.formData.password
        });
        const { access_token, user } = response.data;
        
        localStorage.setItem('token', access_token);
        axios.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;
        this.user = user;
        
        alert('Login successful!');
        await this.fetchUserData();
      } catch (error) {
        alert('Login failed: ' + error.response?.data?.detail);
      }
    },
    
    logout() {
      this.user = null;
      this.balance = null;
      localStorage.removeItem('token');
      delete axios.defaults.headers.common['Authorization'];
    }
  }
};
</script>
```

---

## 📱 **VANILLA JAVASCRIPT (Works Anywhere)**

### **Complete HTML + JS Example**
```html
<!DOCTYPE html>
<html>
<head>
    <title>Token Market Frontend</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
        .form-group { margin: 10px 0; }
        input { padding: 8px; margin: 5px; width: 200px; }
        button { padding: 10px 15px; margin: 5px; cursor: pointer; }
        .user-info { background: #f0f0f0; padding: 15px; border-radius: 5px; }
        .collectible { border: 1px solid #ddd; padding: 10px; margin: 10px; border-radius: 5px; }
    </style>
</head>
<body>
    <h1>Token Market</h1>
    
    <div id="auth-section">
        <h2>Authentication</h2>
        
        <div id="login-forms">
            <h3>Register</h3>
            <div class="form-group">
                <input type="text" id="reg-username" placeholder="Username">
                <input type="email" id="reg-email" placeholder="Email">
                <input type="password" id="reg-password" placeholder="Password">
                <button onclick="register()">Register</button>
            </div>
            
            <h3>Login</h3>
            <div class="form-group">
                <input type="email" id="login-email" placeholder="Email">
                <input type="password" id="login-password" placeholder="Password">
                <button onclick="login()">Login</button>
            </div>
        </div>
        
        <div id="user-info" style="display: none;">
            <div class="user-info">
                <h3>Welcome!</h3>
                <p id="user-details"></p>
                <p id="user-balance"></p>
                <button onclick="logout()">Logout</button>
            </div>
        </div>
    </div>
    
    <div id="collectibles-section">
        <h2>Marketplace</h2>
        <div id="collectibles-list"></div>
        <button onclick="loadCollectibles()">Load Collectibles</button>
    </div>

    <script>
        const API_BASE = 'http://localhost:8000';
        let currentToken = localStorage.getItem('token');
        
        // Initialize page
        if (currentToken) {
            showUserInfo();
            loadUserData();
        }
        
        async function register() {
            const username = document.getElementById('reg-username').value;
            const email = document.getElementById('reg-email').value;
            const password = document.getElementById('reg-password').value;
            
            try {
                const response = await fetch(`${API_BASE}/auth/register`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ username, email, password })
                });
                
                const data = await response.json();
                
                if (response.ok) {
                    currentToken = data.access_token;
                    localStorage.setItem('token', currentToken);
                    showUserInfo();
                    loadUserData();
                    alert('Registration successful!');
                } else {
                    alert('Registration failed: ' + data.detail);
                }
            } catch (error) {
                alert('Error: ' + error.message);
            }
        }
        
        async function login() {
            const email = document.getElementById('login-email').value;
            const password = document.getElementById('login-password').value;
            
            try {
                const response = await fetch(`${API_BASE}/auth/login`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email, password })
                });
                
                const data = await response.json();
                
                if (response.ok) {
                    currentToken = data.access_token;
                    localStorage.setItem('token', currentToken);
                    showUserInfo();
                    loadUserData();
                    alert('Login successful!');
                } else {
                    alert('Login failed: ' + data.detail);
                }
            } catch (error) {
                alert('Error: ' + error.message);
            }
        }
        
        async function loadUserData() {
            if (!currentToken) return;
            
            try {
                const response = await fetch(`${API_BASE}/profile/balance`, {
                    headers: { 'Authorization': `Bearer ${currentToken}` }
                });
                
                if (response.ok) {
                    const balance = await response.json();
                    document.getElementById('user-balance').textContent = 
                        `Balance: ${balance.balance} tokens`;
                } else {
                    logout(); // Token might be expired
                }
            } catch (error) {
                console.error('Error loading user data:', error);
            }
        }
        
        async function loadCollectibles() {
            try {
                const response = await fetch(`${API_BASE}/collectibles`);
                const collectibles = await response.json();
                
                const container = document.getElementById('collectibles-list');
                container.innerHTML = collectibles.map(item => `
                    <div class="collectible">
                        <h4>${item.name}</h4>
                        <p>Set: ${item.set_name}</p>
                        <p>Rarity: ${item.rarity || 'Unknown'}</p>
                        <p>Price: $${item.current_price || 'N/A'}</p>
                    </div>
                `).join('');
            } catch (error) {
                alert('Error loading collectibles: ' + error.message);
            }
        }
        
        function showUserInfo() {
            document.getElementById('login-forms').style.display = 'none';
            document.getElementById('user-info').style.display = 'block';
        }
        
        function logout() {
            currentToken = null;
            localStorage.removeItem('token');
            document.getElementById('login-forms').style.display = 'block';
            document.getElementById('user-info').style.display = 'none';
            document.getElementById('user-details').textContent = '';
            document.getElementById('user-balance').textContent = '';
        }
        
        // Load collectibles on page load
        loadCollectibles();
    </script>
</body>
</html>
```

---

## 📱 **MOBILE APP INTEGRATION**

### **React Native Example**
```jsx
import React, { useState } from 'react';
import { View, Text, TextInput, Button, Alert } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';

const API_BASE = 'http://localhost:8000';

export default function TokenMarketApp() {
  const [user, setUser] = useState(null);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [username, setUsername] = useState('');

  const register = async () => {
    try {
      const response = await fetch(`${API_BASE}/auth/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, email, password })
      });
      
      const data = await response.json();
      
      if (response.ok) {
        await AsyncStorage.setItem('token', data.access_token);
        setUser(data.user);
        Alert.alert('Success', 'Registration successful!');
      } else {
        Alert.alert('Error', data.detail);
      }
    } catch (error) {
      Alert.alert('Error', error.message);
    }
  };

  const login = async () => {
    try {
      const response = await fetch(`${API_BASE}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
      });
      
      const data = await response.json();
      
      if (response.ok) {
        await AsyncStorage.setItem('token', data.access_token);
        setUser(data.user);
        Alert.alert('Success', 'Login successful!');
      } else {
        Alert.alert('Error', data.detail);
      }
    } catch (error) {
      Alert.alert('Error', error.message);
    }
  };

  return (
    <View style={{ padding: 20 }}>
      <Text style={{ fontSize: 24, marginBottom: 20 }}>Token Market</Text>
      
      {user ? (
        <View>
          <Text>Welcome, {user.username}!</Text>
          <Text>Email: {user.email}</Text>
          <Button title="Logout" onPress={() => setUser(null)} />
        </View>
      ) : (
        <View>
          <TextInput
            placeholder="Username"
            value={username}
            onChangeText={setUsername}
            style={{ borderWidth: 1, padding: 10, marginBottom: 10 }}
          />
          <TextInput
            placeholder="Email"
            value={email}
            onChangeText={setEmail}
            style={{ borderWidth: 1, padding: 10, marginBottom: 10 }}
          />
          <TextInput
            placeholder="Password"
            value={password}
            onChangeText={setPassword}
            secureTextEntry
            style={{ borderWidth: 1, padding: 10, marginBottom: 10 }}
          />
          <Button title="Register" onPress={register} />
          <Button title="Login" onPress={login} />
        </View>
      )}
    </View>
  );
}
```

---

## 🔧 **BACKEND CONFIGURATION FOR FRONTEND**

### **Enable CORS (Already Configured)**
Your backend already includes CORS support in `app/api.py`:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### **Production CORS Setup**
For production, update CORS settings:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://yourdomain.com",
        "https://www.yourdomain.com",
        "http://localhost:3000",  # React dev server
        "http://localhost:8080",  # Vue dev server
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
```

---

## 🌐 **DEPLOYMENT CONSIDERATIONS**

### **Frontend Deployment Options**
- **Netlify/Vercel** - Static site hosting with CI/CD
- **AWS S3 + CloudFront** - Scalable static hosting
- **Firebase Hosting** - Google's hosting platform
- **GitHub Pages** - Free static hosting

### **Environment Variables for Frontend**
```javascript
// In React (.env file)
REACT_APP_API_URL=https://your-backend-domain.com

// In Vue (.env file)
VUE_APP_API_URL=https://your-backend-domain.com

// Usage in code
const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:8000';
```

---

## 📊 **API ENDPOINTS REFERENCE**

### **Authentication Endpoints**
```javascript
POST /auth/register
{
  "email": "user@example.com",
  "password": "password123",
  "username": "username"
}

POST /auth/login
{
  "email": "user@example.com", 
  "password": "password123"
}
```

### **Protected Endpoints** (Require Bearer Token)
```javascript
GET /profile/balance
Headers: { "Authorization": "Bearer <token>" }

// Add more protected endpoints as needed
```

### **Public Endpoints**
```javascript
GET /collectibles  // No authentication required
GET /             // Health check
```

---

## 🎯 **NEXT STEPS**

1. **Choose Your Frontend Framework** (React, Vue, vanilla JS, mobile)
2. **Copy the Appropriate Example** from this guide
3. **Start Your Backend** (`python start.py serve`)
4. **Test the Integration** using the examples
5. **Customize** the UI and add your features
6. **Deploy** both frontend and backend

**Your Token Market Backend is ready to power any frontend application!** 🚀

The JWT authentication system, CORS configuration, and RESTful API design make it compatible with any modern frontend technology.
