#!/usr/bin/env python3
"""
🔗 RAILWAY URL TESTER
Test your deployed Railway backend URL
"""

import requests
import sys

def test_railway_url(base_url):
    """Test the deployed Railway backend"""
    print(f"🧪 TESTING RAILWAY DEPLOYMENT: {base_url}")
    print("=" * 60)
    
    endpoints_to_test = [
        {"path": "/", "name": "Root endpoint"},
        {"path": "/health", "name": "Health check"},
        {"path": "/collectibles", "name": "Collectibles (public)"}
    ]
    
    all_working = True
    
    for endpoint in endpoints_to_test:
        url = f"{base_url}{endpoint['path']}"
        try:
            print(f"\n🔍 Testing {endpoint['name']}: {url}")
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                print(f"✅ {endpoint['name']}: Working!")
                if endpoint['path'] == '/health':
                    print(f"   Response: {response.json()}")
            else:
                print(f"❌ {endpoint['name']}: HTTP {response.status_code}")
                all_working = False
                
        except requests.exceptions.RequestException as e:
            print(f"❌ {endpoint['name']}: Connection failed - {e}")
            all_working = False
    
    print(f"\n{'='*60}")
    if all_working:
        print("🎉 YOUR RAILWAY DEPLOYMENT IS WORKING!")
        print("✅ Ready to use in your Lovable frontend!")
        print(f"✅ API Base URL: {base_url}")
    else:
        print("⚠️  Some endpoints failed. Check Railway logs.")
    
    return all_working

def main():
    print("🚀 RAILWAY URL TESTER")
    print("After deploying to Railway, use this script to test your backend")
    
    # Example URLs - replace with your actual Railway URL
    print("\n📋 Example Railway URLs:")
    print("• https://token-market-backend-production.railway.app")
    print("• https://web-production-abc123.railway.app") 
    print("• https://your-app-name.up.railway.app")
    
    url = input("\n🔗 Enter your Railway URL (without trailing slash): ").strip()
    
    if not url:
        print("❌ Please provide a URL")
        return
    
    if not url.startswith('http'):
        url = 'https://' + url
    
    # Remove trailing slash if present
    url = url.rstrip('/')
    
    test_railway_url(url)
    
    print(f"\n💖 UPDATE YOUR LOVABLE COMPONENT:")
    print("Replace this line in TokenMarketLovable.tsx:")
    print(f"const API_BASE_URL = '{url}';")

if __name__ == "__main__":
    main()
