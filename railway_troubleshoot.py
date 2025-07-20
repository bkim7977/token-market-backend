#!/usr/bin/env python3
"""
🔧 RAILWAY DEPLOYMENT TROUBLESHOOTING
Debug your Railway deployment issues
"""

import requests
import time

def check_railway_deployment():
    print("🔧 RAILWAY DEPLOYMENT TROUBLESHOOTING")
    print("=" * 50)
    
    railway_url = "https://token-market-backend-production.up.railway.app"
    
    print(f"🎯 Testing URL: {railway_url}")
    print("\n📋 Common Railway Deployment Issues:")
    print("─" * 35)
    
    issues_and_solutions = [
        {
            "issue": "🔴 Application not found (404)",
            "causes": [
                "• Deployment still building/starting up",
                "• Build failed during deployment",
                "• Environment variables missing",
                "• start.py not executing properly"
            ],
            "solutions": [
                "1. Check Railway dashboard → Deployments → View logs",
                "2. Verify all environment variables are set",
                "3. Ensure start.py has the correct serve command",
                "4. Wait 2-3 minutes for initial deployment"
            ]
        },
        {
            "issue": "🟡 Build Issues",
            "causes": [
                "• Missing dependencies in requirements.txt",
                "• Python version compatibility",
                "• Import errors in code"
            ],
            "solutions": [
                "1. Check build logs in Railway dashboard",
                "2. Verify requirements.txt is complete",
                "3. Test locally with: python start.py serve"
            ]
        },
        {
            "issue": "🟢 App Running but API Errors", 
            "causes": [
                "• Environment variables not set correctly",
                "• Database connection issues",
                "• JWT secret key problems"
            ],
            "solutions": [
                "1. Add all required environment variables",
                "2. Test database connection",
                "3. Verify Supabase credentials"
            ]
        }
    ]
    
    for item in issues_and_solutions:
        print(f"\n{item['issue']}")
        print("Possible causes:")
        for cause in item['causes']:
            print(f"  {cause}")
        print("Solutions:")
        for solution in item['solutions']:
            print(f"  {solution}")
    
    print(f"\n🚀 REQUIRED ENVIRONMENT VARIABLES FOR RAILWAY:")
    print("─" * 45)
    env_vars = {
        "SUPABASE_URL": "https://rrhdrkmomngxcjsatcpy.supabase.co",
        "SUPABASE_KEY": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJyaGRya21vbW5neGNqc2F0Y3B5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzU0MDQwODUsImV4cCI6MjA1MDk4MDA4NX0.yLnx5vQyZ49vwLlT1mKS_DGx1-MfLCXVZ4lJtWMIPlA",
        "JWT_SECRET_KEY": "token-market-super-secret-jwt-key-2025-production-ready",
        "ENVIRONMENT": "production",
        "PORT": "8000"
    }
    
    for key, value in env_vars.items():
        print(f"{key} = {value}")
    
    print(f"\n🔍 DEBUGGING CHECKLIST:")
    print("─" * 20)
    checklist = [
        "[ ] Repository pushed to GitHub successfully",
        "[ ] Railway connected to correct repository",
        "[ ] All environment variables added to Railway", 
        "[ ] Build completed successfully (check logs)",
        "[ ] Service started (check Railway dashboard)",
        "[ ] Health endpoint accessible",
        "[ ] No errors in Railway application logs"
    ]
    
    for item in checklist:
        print(f"  {item}")
    
    print(f"\n⚡ QUICK FIXES TO TRY:")
    print("─" * 20)
    quick_fixes = [
        "1. 🔄 Redeploy: Railway dashboard → Redeploy",
        "2. ⏰ Wait: Initial deployments can take 5-10 minutes",
        "3. 📋 Check logs: Railway dashboard → View logs", 
        "4. 🔧 Verify start command: Should use 'python start.py serve'",
        "5. 🌐 Test locally first: python start.py serve"
    ]
    
    for fix in quick_fixes:
        print(f"  {fix}")
    
    print(f"\n💡 ALTERNATIVE: TEST WITH NGROK")
    print("─" * 30)
    print("If Railway deployment is taking time, test with ngrok:")
    print("1. Terminal 1: python start.py serve")
    print("2. Terminal 2: ngrok http 8000") 
    print("3. Use the ngrok https URL in your Lovable component")
    print("4. This gives you immediate testing while Railway deploys")
    
    # Test the URL periodically
    print(f"\n🧪 TESTING YOUR RAILWAY URL...")
    for attempt in range(3):
        try:
            print(f"\nAttempt {attempt + 1}/3: Testing {railway_url}")
            response = requests.get(f"{railway_url}/health", timeout=10)
            
            if response.status_code == 200:
                print("✅ SUCCESS! Your Railway deployment is working!")
                print(f"Response: {response.json()}")
                print(f"\n🎉 UPDATE YOUR LOVABLE COMPONENT:")
                print("Your TokenMarketLovable.tsx is already updated with the Railway URL!")
                return True
            else:
                print(f"❌ Status: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Connection failed: {e}")
        
        if attempt < 2:  # Don't wait after the last attempt
            print("⏳ Waiting 30 seconds before next attempt...")
            time.sleep(30)
    
    print(f"\n⚠️  DEPLOYMENT NOT READY YET")
    print("Check Railway dashboard for build/deployment status")
    print("Your Lovable component is updated and ready once deployment succeeds!")
    
    return False

if __name__ == "__main__":
    check_railway_deployment()
