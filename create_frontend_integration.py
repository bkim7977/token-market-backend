#!/usr/bin/env python3
"""
🌐 FRONTEND INTEGRATION DEMO
Creates a simple React app that connects to your Token Market Backend
"""

import os
import subprocess
import webbrowser
import time

def create_react_integration():
    """Create a simple React integration example."""
    
    print("🚀 FRONTEND INTEGRATION GUIDE")
    print("=" * 50)
    
    print("\n📋 INTEGRATION OPTIONS:")
    print("1. 🌐 HTML/JavaScript Demo (Ready to use)")
    print("2. ⚛️ React Integration")
    print("3. 🖖 Vue.js Integration")
    print("4. 📱 Mobile App Integration")
    print("5. 🔧 Custom Integration")
    
    print("\n🎯 IMMEDIATE DEMO:")
    print("✅ Open: file:///Users/brian/token_market_backend/frontend_demo.html")
    print("   → Complete working frontend demo")
    print("   → Test registration, login, balance, collectibles")
    print("   → Works immediately with your backend")
    
    print("\n🔧 BACKEND REQUIREMENTS:")
    print("✅ Your backend must be running:")
    print("   cd /Users/brian/token_market_backend")
    print("   python start.py serve")
    print("✅ Backend URL: http://localhost:8000")
    print("✅ API Docs: http://localhost:8000/docs")
    
    print("\n⚛️ REACT QUICK START:")
    print("1. Create React app:")
    print("   npx create-react-app my-token-app")
    print("   cd my-token-app")
    print("   npm install axios")
    
    print("2. Replace src/App.js with:")
    react_code = '''
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

const API_BASE = 'http://localhost:8000';

function App() {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('token'));
  const [balance, setBalance] = useState(null);
  const [collectibles, setCollectibles] = useState([]);
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    username: ''
  });

  useEffect(() => {
    if (token) {
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      fetchUserData();
    }
    fetchCollectibles();
  }, [token]);

  const fetchUserData = async () => {
    try {
      const response = await axios.get(`${API_BASE}/profile/balance`);
      setBalance(response.data);
    } catch (error) {
      console.error('Error:', error);
      logout();
    }
  };

  const fetchCollectibles = async () => {
    try {
      const response = await axios.get(`${API_BASE}/collectibles`);
      setCollectibles(response.data);
    } catch (error) {
      console.error('Error fetching collectibles:', error);
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

  return (
    <div className="App" style={{ padding: '20px', maxWidth: '800px', margin: '0 auto' }}>
      <h1>🪙 Token Market</h1>
      
      {user ? (
        <div style={{ background: '#e8f5e8', padding: '20px', borderRadius: '10px', marginBottom: '20px' }}>
          <h2>Welcome, {user.username}!</h2>
          <p>Email: {user.email}</p>
          {balance && <p>Balance: {balance.balance} tokens</p>}
          <button onClick={logout} style={{ background: '#dc3545', color: 'white', padding: '10px 20px', border: 'none', borderRadius: '5px' }}>
            Logout
          </button>
        </div>
      ) : (
        <div style={{ display: 'flex', gap: '40px', marginBottom: '20px' }}>
          <form onSubmit={register} style={{ flex: 1, background: '#f8f9fa', padding: '20px', borderRadius: '10px' }}>
            <h3>Register</h3>
            <input
              type="text"
              placeholder="Username"
              value={formData.username}
              onChange={(e) => setFormData({...formData, username: e.target.value})}
              style={{ width: '100%', padding: '10px', margin: '5px 0', border: '1px solid #ddd', borderRadius: '5px' }}
              required
            />
            <input
              type="email"
              placeholder="Email"
              value={formData.email}
              onChange={(e) => setFormData({...formData, email: e.target.value})}
              style={{ width: '100%', padding: '10px', margin: '5px 0', border: '1px solid #ddd', borderRadius: '5px' }}
              required
            />
            <input
              type="password"
              placeholder="Password"
              value={formData.password}
              onChange={(e) => setFormData({...formData, password: e.target.value})}
              style={{ width: '100%', padding: '10px', margin: '5px 0', border: '1px solid #ddd', borderRadius: '5px' }}
              required
            />
            <button type="submit" style={{ background: '#007bff', color: 'white', padding: '10px 20px', border: 'none', borderRadius: '5px', width: '100%' }}>
              Register
            </button>
          </form>

          <form onSubmit={login} style={{ flex: 1, background: '#f8f9fa', padding: '20px', borderRadius: '10px' }}>
            <h3>Login</h3>
            <input
              type="email"
              placeholder="Email"
              value={formData.email}
              onChange={(e) => setFormData({...formData, email: e.target.value})}
              style={{ width: '100%', padding: '10px', margin: '5px 0', border: '1px solid #ddd', borderRadius: '5px' }}
              required
            />
            <input
              type="password"
              placeholder="Password"
              value={formData.password}
              onChange={(e) => setFormData({...formData, password: e.target.value})}
              style={{ width: '100%', padding: '10px', margin: '5px 0', border: '1px solid #ddd', borderRadius: '5px' }}
              required
            />
            <button type="submit" style={{ background: '#28a745', color: 'white', padding: '10px 20px', border: 'none', borderRadius: '5px', width: '100%' }}>
              Login
            </button>
          </form>
        </div>
      )}

      <div>
        <h2>🏪 Marketplace ({collectibles.length} items)</h2>
        <div style={{ display: 'grid', gap: '15px' }}>
          {collectibles.map((item) => (
            <div key={item.id} style={{ border: '1px solid #ddd', padding: '15px', borderRadius: '8px', background: '#f8f9fa' }}>
              <h3>{item.name}</h3>
              <p>Set: {item.set_name}</p>
              <p>Rarity: {item.rarity}</p>
              <p>Price: ${item.current_price}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default App;
    '''
    
    print("3. Start the React app:")
    print("   npm start")
    print("   → Opens on http://localhost:3000")
    
    print("\n🖖 VUE.JS QUICK START:")
    print("1. Create Vue app:")
    print("   npm create vue@latest my-token-vue-app")
    print("   cd my-token-vue-app")
    print("   npm install axios")
    print("   npm run dev")
    
    print("\n📱 MOBILE APP INTEGRATION:")
    print("1. React Native:")
    print("   npx react-native init TokenMarketApp")
    print("   → Use fetch API for HTTP requests")
    
    print("2. Flutter:")
    print("   → Use http package for API calls")
    
    print("3. iOS (Swift):")
    print("   → Use URLSession for HTTP requests")
    
    print("4. Android (Kotlin/Java):")
    print("   → Use Retrofit or OkHttp for API calls")
    
    print("\n🔧 KEY INTEGRATION CONCEPTS:")
    print("✅ Base URL: http://localhost:8000")
    print("✅ Authentication: Bearer token in Authorization header")
    print("✅ CORS: Already configured in your backend")
    print("✅ Content-Type: application/json")
    
    print("\n📊 API ENDPOINTS TO USE:")
    print("• POST /auth/register - User registration")
    print("• POST /auth/login - User authentication")
    print("• GET /profile/balance - User balance (protected)")
    print("• GET /collectibles - Marketplace items (public)")
    
    print("\n🎯 TESTING YOUR INTEGRATION:")
    print("1. Start backend: python start.py serve")
    print("2. Open frontend_demo.html in browser")
    print("3. Test registration and login")
    print("4. Verify balance and collectibles load")
    
    print("\n📚 DOCUMENTATION:")
    print("• Complete guide: FRONTEND_INTEGRATION_GUIDE.md")
    print("• API docs: http://localhost:8000/docs")
    print("• Working demo: frontend_demo.html")
    
    print("\n🚀 YOUR BACKEND IS READY FOR ANY FRONTEND!")
    print("The JWT authentication, CORS setup, and RESTful design")
    print("make it compatible with any modern frontend technology.")

if __name__ == "__main__":
    create_react_integration()
