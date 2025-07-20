#!/usr/bin/env python3
"""
Simple Railway deployment monitor
"""

import requests
import time
import json

def check_railway_status():
    url = "https://token-market-backend-production.up.railway.app"
    endpoints = ["/health", "/status", "/"]
    
    print("🚀 Checking Railway Deployment Status...")
    print(f"URL: {url}")
    print("-" * 50)
    
    for endpoint in endpoints:
        full_url = f"{url}{endpoint}"
        try:
            response = requests.get(full_url, timeout=10)
            print(f"✅ {endpoint}: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                if endpoint == "/health":
                    print(f"   Status: {data.get('status')}")
                    print(f"   Database: {data.get('database_available')}")
                elif endpoint == "/status":
                    print(f"   Service: {data.get('service')}")
                    print(f"   Environment: {data.get('environment')}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ {endpoint}: {str(e)}")
    
    print("-" * 50)
    print("✨ Railway deployment check complete!")

if __name__ == "__main__":
    check_railway_status()
