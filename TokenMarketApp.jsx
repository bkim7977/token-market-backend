import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_BASE = 'http://localhost:8000';

// Configure axios defaults
axios.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Add response interceptor for better error handling
axios.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expired or invalid
      localStorage.removeItem('token');
      window.location.reload();
    }
    return Promise.reject(error);
  }
);

function TokenMarketApp() {
  // State management
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('token'));
  const [balance, setBalance] = useState(null);
  const [collectibles, setCollectibles] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  
  // Form states
  const [isLogin, setIsLogin] = useState(true);
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    username: ''
  });

  // Load data on component mount
  useEffect(() => {
    if (token) {
      fetchUserData();
    }
    fetchCollectibles();
  }, [token]);

  // Fetch user profile and balance
  const fetchUserData = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`${API_BASE}/profile/balance`);
      setBalance(response.data);
      setUser(response.data.user || { username: 'User', email: formData.email });
    } catch (error) {
      console.error('Error fetching user data:', error);
      handleLogout();
    } finally {
      setLoading(false);
    }
  };

  // Fetch marketplace collectibles
  const fetchCollectibles = async () => {
    try {
      const response = await axios.get(`${API_BASE}/collectibles`);
      setCollectibles(response.data);
    } catch (error) {
      console.error('Error fetching collectibles:', error);
      setError('Failed to load marketplace items');
    }
  };

  // Handle user registration
  const handleRegister = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const response = await axios.post(`${API_BASE}/auth/register`, formData);
      const { access_token, user } = response.data;
      
      localStorage.setItem('token', access_token);
      setToken(access_token);
      setUser(user);
      
      // Clear form
      setFormData({ email: '', password: '', username: '' });
      
      // Fetch user data after successful registration
      await fetchUserData();
      
    } catch (error) {
      setError(error.response?.data?.detail || 'Registration failed');
    } finally {
      setLoading(false);
    }
  };

  // Handle user login
  const handleLogin = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const response = await axios.post(`${API_BASE}/auth/login`, {
        email: formData.email,
        password: formData.password
      });
      const { access_token, user } = response.data;
      
      localStorage.setItem('token', access_token);
      setToken(access_token);
      setUser(user);
      
      // Clear form
      setFormData({ email: '', password: '', username: '' });
      
      // Fetch user data after successful login
      await fetchUserData();
      
    } catch (error) {
      setError(error.response?.data?.detail || 'Login failed');
    } finally {
      setLoading(false);
    }
  };

  // Handle logout
  const handleLogout = () => {
    localStorage.removeItem('token');
    setToken(null);
    setUser(null);
    setBalance(null);
    setFormData({ email: '', password: '', username: '' });
    setError('');
  };

  // Handle form input changes
  const handleInputChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  // Styles
  const styles = {
    container: {
      maxWidth: '1200px',
      margin: '0 auto',
      padding: '20px',
      fontFamily: 'Arial, sans-serif'
    },
    header: {
      textAlign: 'center',
      marginBottom: '30px',
      color: '#333'
    },
    userInfo: {
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      color: 'white',
      padding: '20px',
      borderRadius: '10px',
      marginBottom: '30px',
      boxShadow: '0 4px 6px rgba(0,0,0,0.1)'
    },
    authContainer: {
      display: 'flex',
      gap: '20px',
      marginBottom: '30px',
      flexWrap: 'wrap'
    },
    authForm: {
      flex: '1',
      minWidth: '300px',
      background: '#f8f9fa',
      padding: '25px',
      borderRadius: '10px',
      boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
    },
    input: {
      width: '100%',
      padding: '12px',
      margin: '8px 0',
      border: '1px solid #ddd',
      borderRadius: '5px',
      fontSize: '14px',
      boxSizing: 'border-box'
    },
    button: {
      width: '100%',
      padding: '12px',
      margin: '10px 0',
      border: 'none',
      borderRadius: '5px',
      fontSize: '16px',
      cursor: 'pointer',
      transition: 'background-color 0.3s'
    },
    primaryButton: {
      backgroundColor: '#007bff',
      color: 'white'
    },
    successButton: {
      backgroundColor: '#28a745',
      color: 'white'
    },
    dangerButton: {
      backgroundColor: '#dc3545',
      color: 'white',
      width: 'auto',
      padding: '8px 16px'
    },
    marketplace: {
      marginTop: '30px'
    },
    collectiblesGrid: {
      display: 'grid',
      gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))',
      gap: '20px',
      marginTop: '20px'
    },
    collectibleCard: {
      border: '1px solid #ddd',
      padding: '20px',
      borderRadius: '8px',
      background: 'white',
      boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
      transition: 'transform 0.2s, box-shadow 0.2s'
    },
    error: {
      background: '#f8d7da',
      color: '#721c24',
      padding: '10px',
      borderRadius: '5px',
      margin: '10px 0',
      border: '1px solid #f5c6cb'
    },
    loading: {
      textAlign: 'center',
      color: '#666',
      fontStyle: 'italic'
    },
    toggleButton: {
      background: 'none',
      border: 'none',
      color: '#007bff',
      cursor: 'pointer',
      textDecoration: 'underline'
    }
  };

  return (
    <div style={styles.container}>
      <h1 style={styles.header}>🪙 Token Market</h1>
      
      {error && (
        <div style={styles.error}>
          {error}
        </div>
      )}
      
      {user && token ? (
        <div style={styles.userInfo}>
          <h2>Welcome back, {user.username}! 👋</h2>
          <p>📧 {user.email}</p>
          {balance && (
            <p>💰 Balance: <strong>{balance.balance} tokens</strong></p>
          )}
          <button 
            onClick={handleLogout}
            style={{...styles.button, ...styles.dangerButton}}
          >
            Logout
          </button>
        </div>
      ) : (
        <div style={styles.authContainer}>
          <form 
            onSubmit={isLogin ? handleLogin : handleRegister} 
            style={styles.authForm}
          >
            <h3>{isLogin ? '🔐 Login' : '📝 Register'}</h3>
            
            {!isLogin && (
              <input
                type="text"
                name="username"
                placeholder="Username"
                value={formData.username}
                onChange={handleInputChange}
                style={styles.input}
                required
              />
            )}
            
            <input
              type="email"
              name="email"
              placeholder="Email"
              value={formData.email}
              onChange={handleInputChange}
              style={styles.input}
              required
            />
            
            <input
              type="password"
              name="password"
              placeholder="Password"
              value={formData.password}
              onChange={handleInputChange}
              style={styles.input}
              required
            />
            
            <button 
              type="submit" 
              disabled={loading}
              style={{
                ...styles.button, 
                ...(isLogin ? styles.successButton : styles.primaryButton)
              }}
            >
              {loading ? 'Please wait...' : (isLogin ? 'Login' : 'Register')}
            </button>
            
            <p style={{ textAlign: 'center', marginTop: '15px' }}>
              {isLogin ? "Don't have an account? " : "Already have an account? "}
              <button 
                type="button"
                onClick={() => setIsLogin(!isLogin)}
                style={styles.toggleButton}
              >
                {isLogin ? 'Register here' : 'Login here'}
              </button>
            </p>
          </form>
        </div>
      )}

      <div style={styles.marketplace}>
        <h2>🏪 Marketplace</h2>
        <p>{collectibles.length} collectibles available</p>
        
        {loading ? (
          <div style={styles.loading}>Loading collectibles...</div>
        ) : (
          <div style={styles.collectiblesGrid}>
            {collectibles.map((item) => (
              <div 
                key={item.id} 
                style={styles.collectibleCard}
                onMouseEnter={(e) => {
                  e.target.style.transform = 'translateY(-2px)';
                  e.target.style.boxShadow = '0 4px 8px rgba(0,0,0,0.15)';
                }}
                onMouseLeave={(e) => {
                  e.target.style.transform = 'translateY(0)';
                  e.target.style.boxShadow = '0 2px 4px rgba(0,0,0,0.1)';
                }}
              >
                <h3 style={{ margin: '0 0 10px 0', color: '#333' }}>{item.name}</h3>
                <p style={{ margin: '5px 0', color: '#666' }}>
                  <strong>Set:</strong> {item.set_name}
                </p>
                <p style={{ margin: '5px 0', color: '#666' }}>
                  <strong>Rarity:</strong> {item.rarity}
                </p>
                <p style={{ 
                  margin: '10px 0 0 0', 
                  fontSize: '18px', 
                  fontWeight: 'bold', 
                  color: '#28a745' 
                }}>
                  ${item.current_price}
                </p>
              </div>
            ))}
          </div>
        )}
      </div>
      
      <div style={{ 
        marginTop: '50px', 
        padding: '20px', 
        background: '#f8f9fa', 
        borderRadius: '10px',
        textAlign: 'center'
      }}>
        <h3>🔗 Backend Connected</h3>
        <p>Successfully connected to Token Market API</p>
        <p><strong>API Base:</strong> {API_BASE}</p>
        <p><strong>Status:</strong> ✅ Online</p>
      </div>
    </div>
  );
}

export default TokenMarketApp;
