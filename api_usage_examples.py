#!/usr/bin/env python3
"""
🐍 Python API Usage Examples
Demonstrates HTTP API usage with the requests library
"""

import requests
import json
import sys

# Base URL for the API
BASE_URL = "http://localhost:8000"

def print_response(response, description):
    """Pretty print API response."""
    print(f"\n{'='*50}")
    print(f"📡 {description}")
    print(f"{'='*50}")
    print(f"Status Code: {response.status_code}")
    
    try:
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2)}")
        return data
    except:
        print(f"Raw Response: {response.text}")
        return None

def main():
    print("🚀 PYTHON API USAGE EXAMPLES")
    print("Make sure the server is running: python start.py serve")
    
    # 1. Register a new user
    print("\n1️⃣  REGISTERING NEW USER")
    register_data = {
        "email": "python_user@example.com",
        "password": "SecurePassword123!",
        "username": "pythonuser"
    }
    
    try:
        register_response = requests.post(
            f"{BASE_URL}/auth/register",
            json=register_data,
            headers={"Content-Type": "application/json"}
        )
        register_result = print_response(register_response, "User Registration")
        
        # 2. Login user
        print("\n2️⃣  USER LOGIN")
        login_data = {
            "email": "python_user@example.com",
            "password": "SecurePassword123!"
        }
        
        login_response = requests.post(
            f"{BASE_URL}/auth/login",
            json=login_data,
            headers={"Content-Type": "application/json"}
        )
        login_result = print_response(login_response, "User Login")
        
        # Extract access token
        if login_result and "access_token" in login_result:
            access_token = login_result["access_token"]
            print(f"\n🔑 Access Token: {access_token[:50]}...")
            
            # 3. Access protected endpoint
            print("\n3️⃣  PROTECTED ENDPOINT ACCESS")
            headers = {"Authorization": f"Bearer {access_token}"}
            
            # Get user profile
            profile_response = requests.get(f"{BASE_URL}/profile", headers=headers)
            print_response(profile_response, "User Profile")
            
            # Get user balance
            balance_response = requests.get(f"{BASE_URL}/profile/balance", headers=headers)
            print_response(balance_response, "User Balance")
            
        else:
            print("❌ Failed to get access token")
    
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Make sure the server is running!")
        print("Run: python start.py serve")
        return
    
    # 4. Get public data (no authentication needed)
    print("\n4️⃣  PUBLIC DATA ACCESS")
    try:
        # Get all collectibles
        collectibles_response = requests.get(f"{BASE_URL}/collectibles")
        collectibles_data = print_response(collectibles_response, "Public Collectibles")
        
        # Get specific collectible if any exist
        if collectibles_data and isinstance(collectibles_data, list) and len(collectibles_data) > 0:
            first_collectible_id = collectibles_data[0].get("collectible_id")
            if first_collectible_id:
                item_response = requests.get(f"{BASE_URL}/collectibles/{first_collectible_id}")
                print_response(item_response, f"Collectible Details")
    
    except Exception as e:
        print(f"❌ Error accessing public data: {e}")
    
    print("\n✅ API USAGE EXAMPLES COMPLETE!")
    print("\n📚 Next Steps:")
    print("- Check the interactive docs: http://localhost:8000/docs")
    print("- Try the database_usage_demo.py for more advanced examples")
    print("- See DATABASE_USAGE.md for comprehensive usage guide")

if __name__ == "__main__":
    main()
