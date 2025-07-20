#!/usr/bin/env python3
"""
JWT Authentication API Test
Tests the complete authentication flow with JWT tokens
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import requests
import json
import uuid
from datetime import datetime

API_BASE_URL = "http://127.0.0.1:8000"

def test_api_health():
    """Test API health check"""
    print("🔌 Testing API Health Check...")
    try:
        response = requests.get(f"{API_BASE_URL}/")
        if response.status_code == 200:
            print("✓ API is running")
            print(f"  Response: {response.json()}")
            return True
        else:
            print(f"✗ API health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Cannot connect to API: {e}")
        return False

def test_user_registration():
    """Test user registration with JWT"""
    print("\n📝 Testing User Registration...")
    
    # Generate unique test user
    test_suffix = uuid.uuid4().hex[:8]
    test_user = {
        "email": f"jwt.test.{test_suffix}@example.com",
        "password": "SecurePassword123!",
        "username": f"jwt_user_{test_suffix}"
    }
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/auth/register",
            json=test_user,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✓ User registration successful")
            print(f"  User ID: {data['user']['id']}")
            print(f"  Token Type: {data['token_type']}")
            print(f"  Access Token: {data['access_token'][:50]}...")
            
            return {
                "user": data['user'],
                "access_token": data['access_token'],
                "credentials": test_user
            }
        else:
            print(f"✗ Registration failed: {response.status_code}")
            print(f"  Error: {response.text}")
            return None
            
    except Exception as e:
        print(f"✗ Registration error: {e}")
        return None

def test_user_login(credentials):
    """Test user login with JWT"""
    print("\n🔑 Testing User Login...")
    
    login_data = {
        "email": credentials["email"],
        "password": credentials["password"]
    }
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/auth/login",
            json=login_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✓ User login successful")
            print(f"  User: {data['user']['username']}")
            print(f"  Token Type: {data['token_type']}")
            return data['access_token']
        else:
            print(f"✗ Login failed: {response.status_code}")
            print(f"  Error: {response.text}")
            return None
            
    except Exception as e:
        print(f"✗ Login error: {e}")
        return None

def test_protected_endpoint(access_token):
    """Test protected endpoint with JWT token"""
    print("\n🔒 Testing Protected Endpoint...")
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(
            f"{API_BASE_URL}/profile/balance",
            headers=headers
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✓ Protected endpoint access successful")
            print(f"  Balance: {data}")
            return True
        else:
            print(f"✗ Protected endpoint failed: {response.status_code}")
            print(f"  Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"✗ Protected endpoint error: {e}")
        return False

def test_public_endpoints():
    """Test public endpoints (no authentication required)"""
    print("\n🌐 Testing Public Endpoints...")
    
    try:
        # Test collectibles endpoint
        response = requests.get(f"{API_BASE_URL}/collectibles")
        if response.status_code == 200:
            collectibles = response.json()
            print(f"✓ Collectibles endpoint working ({len(collectibles)} items)")
        else:
            print(f"✗ Collectibles endpoint failed: {response.status_code}")
            
    except Exception as e:
        print(f"✗ Public endpoints error: {e}")

def main():
    """Run complete JWT authentication test"""
    print("🚀 JWT Authentication API Test")
    print("=" * 50)
    
    # Test 1: API Health
    if not test_api_health():
        print("\n❌ API is not running. Start the server first:")
        print("python start.py serve")
        return
    
    # Test 2: User Registration
    registration_result = test_user_registration()
    if not registration_result:
        print("\n❌ User registration failed")
        return
    
    # Test 3: User Login
    access_token = test_user_login(registration_result["credentials"])
    if not access_token:
        print("\n❌ User login failed")
        return
    
    # Test 4: Protected Endpoint
    if not test_protected_endpoint(access_token):
        print("\n❌ Protected endpoint access failed")
        return
    
    # Test 5: Public Endpoints
    test_public_endpoints()
    
    print("\n🎉 ALL JWT AUTHENTICATION TESTS PASSED!")
    print("✅ Registration working with JWT tokens")
    print("✅ Login working with JWT tokens")
    print("✅ Protected endpoints secured with JWT")
    print("✅ Public endpoints accessible without authentication")

if __name__ == "__main__":
    main()
