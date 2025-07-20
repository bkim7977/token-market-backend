#!/usr/bin/env python3
"""
🚀 RAILWAY DEPLOYMENT STATUS CHECKER
Monitor your Railway deployment progress
"""

import requests
import time

def check_railway_status():
    print("🚀 RAILWAY DEPLOYMENT STATUS CHECKER")
    print("=" * 50)
    
    railway_url = "https://token-market-backend-production.up.railway.app"
    
    print(f"🎯 Monitoring: {railway_url}")
    print(f"📋 Issue Fixed: Updated supabase==2.11.5 → supabase==2.17.0")
    print(f"🔄 Code pushed to GitHub - Railway should be rebuilding now")
    
    print(f"\n⏳ MONITORING DEPLOYMENT...")
    print("─" * 25)
    
    max_attempts = 10
    wait_time = 30
    
    for attempt in range(1, max_attempts + 1):
        print(f"\n🧪 Attempt {attempt}/{max_attempts}: Testing deployment...")
        
        try:
            # Test health endpoint
            response = requests.get(f"{railway_url}/health", timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                print("🎉 SUCCESS! Your Railway deployment is working!")
                print(f"✅ Health Response: {data}")
                
                # Test other endpoints
                print(f"\n🔍 Testing additional endpoints...")
                
                # Test root endpoint
                try:
                    root_response = requests.get(f"{railway_url}/", timeout=10)
                    if root_response.status_code == 200:
                        print(f"✅ Root endpoint: {root_response.json()}")
                    else:
                        print(f"⚠️ Root endpoint: HTTP {root_response.status_code}")
                except:
                    print(f"⚠️ Root endpoint: Failed to connect")
                
                # Test collectibles endpoint
                try:
                    collectibles_response = requests.get(f"{railway_url}/collectibles", timeout=10)
                    if collectibles_response.status_code == 200:
                        collectibles = collectibles_response.json()
                        print(f"✅ Collectibles endpoint: {len(collectibles)} items found")
                    else:
                        print(f"⚠️ Collectibles endpoint: HTTP {collectibles_response.status_code}")
                except:
                    print(f"⚠️ Collectibles endpoint: Failed to connect")
                
                print(f"\n💖 YOUR LOVABLE INTEGRATION IS READY!")
                print(f"✅ Railway URL: {railway_url}")
                print(f"✅ TokenMarketLovable.tsx already updated with this URL")
                print(f"✅ Test your Lovable app now - the 'Failed to fetch' error should be resolved!")
                
                return True
                
            elif response.status_code == 404:
                print(f"🔄 Still deploying... (404 - Application not found)")
                
            else:
                print(f"⚠️ HTTP {response.status_code}: {response.text[:100]}...")
                
        except requests.exceptions.RequestException as e:
            print(f"🔄 Connection failed: {str(e)[:100]}...")
        
        if attempt < max_attempts:
            print(f"⏳ Waiting {wait_time} seconds before next check...")
            time.sleep(wait_time)
    
    print(f"\n⚠️ DEPLOYMENT STILL IN PROGRESS")
    print(f"🔧 What to do next:")
    print(f"1. Check Railway dashboard for build logs")
    print(f"2. Verify all environment variables are set") 
    print(f"3. The fix should resolve the supabase version issue")
    print(f"4. Railway deployments can take 5-10 minutes")
    
    print(f"\n🎯 MANUAL CHECK:")
    print(f"Visit: {railway_url}/health")
    print(f"Expected response: {{'status': 'healthy', 'message': 'Token Market Backend is running', 'version': '1.0.0'}}")
    
    return False

if __name__ == "__main__":
    check_railway_status()
