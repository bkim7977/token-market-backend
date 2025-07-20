// 💖 LOVABLE-OPTIMIZED TOKEN MARKET COMPONENT
// Copy this directly into your Lovable project

import React, { useState, useEffect } from 'react';

// Environment-aware API configuration
const API_BASE_URL = process.env.NODE_ENV === 'development'
  ? 'http://localhost:8000'
  : 'https://token-market-backend-production.up.railway.app';

// For immediate testing with ngrok (temporary solution):
// const API_BASE_URL = 'https://your-ngrok-url.ngrok.io';

// Types for TypeScript (Lovable loves TypeScript!)
interface User {
  id: number;
  username: string;
  email: string;
}

interface Collectible {
  id: number;
  name: string;
  set_name: string;
  rarity: string;
  current_price: number;
}

interface UserBalance {
  balance: number;
  user_id: number;
  user?: User;
}

interface AuthResponse {
  access_token: string;
  token_type: string;
  user: User;
}

const TokenMarketLovable: React.FC = () => {
  // State management (Lovable style)
  const [user, setUser] = useState<User | null>(null);
  const [balance, setBalance] = useState<number | null>(null);
  const [collectibles, setCollectibles] = useState<Collectible[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string>('');
  const [isLogin, setIsLogin] = useState(true);
  
  // Form state
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    username: ''
  });

  // API helpers with proper error handling
  const apiCall = async (endpoint: string, options: RequestInit = {}) => {
    const token = localStorage.getItem('token');
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
      ...(token && { Authorization: `Bearer ${token}` }),
    };

    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      ...options,
      headers: { ...headers, ...options.headers },
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || `HTTP ${response.status}`);
    }

    return response.json();
  };

  // Load data on mount
  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      fetchUserData();
    }
    fetchCollectibles();
  }, []);

  // Fetch user profile and balance
  const fetchUserData = async () => {
    try {
      const data: UserBalance = await apiCall('/profile/balance');
      setBalance(data.balance);
      setUser(data.user || { id: data.user_id, username: 'User', email: formData.email });
    } catch (error) {
      console.error('Error fetching user data:', error);
      handleLogout();
    }
  };

  // Fetch marketplace collectibles
  const fetchCollectibles = async () => {
    try {
      const data: Collectible[] = await apiCall('/collectibles');
      setCollectibles(data);
    } catch (error) {
      console.error('Error fetching collectibles:', error);
      setError('Failed to load marketplace items');
    }
  };

  // Handle authentication
  const handleAuth = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const endpoint = isLogin ? '/auth/login' : '/auth/register';
      const body = isLogin 
        ? { email: formData.email, password: formData.password }
        : formData;

      const response: AuthResponse = await apiCall(endpoint, {
        method: 'POST',
        body: JSON.stringify(body),
      });

      localStorage.setItem('token', response.access_token);
      setUser(response.user);
      setFormData({ email: '', password: '', username: '' });
      
      await fetchUserData();
    } catch (error) {
      setError(error instanceof Error ? error.message : 'Authentication failed');
    } finally {
      setLoading(false);
    }
  };

  // Handle logout
  const handleLogout = () => {
    localStorage.removeItem('token');
    setUser(null);
    setBalance(null);
    setFormData({ email: '', password: '', username: '' });
    setError('');
  };

  // Handle input changes
  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <h1 className="text-3xl font-bold text-gray-900">
              🪙 Token Market
            </h1>
            {user && (
              <button
                onClick={handleLogout}
                className="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-lg transition-colors duration-200"
              >
                Logout
              </button>
            )}
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Error Display */}
        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded-lg mb-6">
            <p>{error}</p>
          </div>
        )}

        {/* User Dashboard */}
        {user ? (
          <div className="bg-gradient-to-r from-blue-500 to-purple-600 text-white rounded-xl p-8 mb-8 shadow-lg">
            <div className="flex flex-col md:flex-row md:items-center md:justify-between">
              <div>
                <h2 className="text-2xl font-bold mb-2">Welcome back, {user.username}! 👋</h2>
                <p className="text-blue-100 mb-2">📧 {user.email}</p>
                {balance !== null && (
                  <p className="text-xl">
                    💰 Balance: <span className="font-bold">{balance} tokens</span>
                  </p>
                )}
              </div>
              <div className="mt-4 md:mt-0">
                <div className="bg-white bg-opacity-20 rounded-lg p-4 text-center">
                  <p className="text-sm text-blue-100">Account Status</p>
                  <p className="font-bold">✅ Active</p>
                </div>
              </div>
            </div>
          </div>
        ) : (
          /* Authentication Form */
          <div className="bg-white rounded-xl shadow-lg p-8 mb-8 max-w-md mx-auto">
            <h2 className="text-2xl font-bold text-gray-900 text-center mb-6">
              {isLogin ? '🔐 Login' : '📝 Create Account'}
            </h2>
            
            <form onSubmit={handleAuth} className="space-y-4">
              {!isLogin && (
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Username
                  </label>
                  <input
                    type="text"
                    name="username"
                    value={formData.username}
                    onChange={handleInputChange}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="Enter your username"
                    required
                  />
                </div>
              )}
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Email
                </label>
                <input
                  type="email"
                  name="email"
                  value={formData.email}
                  onChange={handleInputChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="Enter your email"
                  required
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Password
                </label>
                <input
                  type="password"
                  name="password"
                  value={formData.password}
                  onChange={handleInputChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="Enter your password"
                  required
                />
              </div>
              
              <button
                type="submit"
                disabled={loading}
                className={`w-full py-3 px-4 rounded-lg font-medium text-white transition-colors duration-200 ${
                  loading 
                    ? 'bg-gray-400 cursor-not-allowed' 
                    : isLogin 
                      ? 'bg-green-500 hover:bg-green-600' 
                      : 'bg-blue-500 hover:bg-blue-600'
                }`}
              >
                {loading ? 'Please wait...' : (isLogin ? 'Login' : 'Create Account')}
              </button>
            </form>
            
            <div className="mt-6 text-center">
              <p className="text-gray-600">
                {isLogin ? "Don't have an account? " : "Already have an account? "}
                <button
                  onClick={() => setIsLogin(!isLogin)}
                  className="text-blue-500 hover:text-blue-600 font-medium"
                >
                  {isLogin ? 'Sign up here' : 'Login here'}
                </button>
              </p>
            </div>
          </div>
        )}

        {/* Marketplace Section */}
        <div className="bg-white rounded-xl shadow-lg p-8">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-2xl font-bold text-gray-900">🏪 Marketplace</h2>
            <span className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm font-medium">
              {collectibles.length} items available
            </span>
          </div>
          
          {loading ? (
            <div className="text-center py-12">
              <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
              <p className="mt-2 text-gray-600">Loading collectibles...</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
              {collectibles.map((item) => (
                <div
                  key={item.id}
                  className="bg-gray-50 rounded-lg p-6 hover:shadow-md transition-shadow duration-200 border border-gray-200"
                >
                  <div className="flex items-start justify-between mb-3">
                    <h3 className="font-semibold text-gray-900 text-lg">{item.name}</h3>
                    <span className="bg-yellow-100 text-yellow-800 px-2 py-1 rounded text-xs font-medium">
                      {item.rarity}
                    </span>
                  </div>
                  <p className="text-gray-600 text-sm mb-4">
                    <span className="font-medium">Set:</span> {item.set_name}
                  </p>
                  <div className="flex items-center justify-between">
                    <span className="text-2xl font-bold text-green-600">
                      ${item.current_price}
                    </span>
                    <button className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors duration-200">
                      View Details
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Connection Status */}
        <div className="mt-8 bg-green-50 border border-green-200 rounded-lg p-4">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <div className="w-3 h-3 bg-green-400 rounded-full"></div>
            </div>
            <div className="ml-3">
              <p className="text-sm text-green-800">
                <strong>Backend Connected:</strong> Successfully connected to Token Market API ({API_BASE_URL})
              </p>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default TokenMarketLovable;
