#!/usr/bin/env python3
"""
🚀 GITHUB SETUP & DEPLOYMENT GUIDE
Step-by-step guide to get your repository online for Railway deployment
"""

def show_github_setup():
    print("🚀 GITHUB REPOSITORY SETUP")
    print("=" * 50)
    
    print("\n✅ Good news! Your code is committed locally.")
    print("Now you need to push it to GitHub so Railway can see it.")
    
    print("\n📋 STEP-BY-STEP GITHUB SETUP:")
    print("─" * 35)
    
    print("\n1️⃣ CREATE GITHUB REPOSITORY:")
    print("   • Go to https://github.com")
    print("   • Click the green 'New' button (or '+' → New repository)")
    print("   • Repository name: token-market-backend")
    print("   • Description: Production-ready Token Market Backend with JWT auth")
    print("   • Make it PUBLIC (so Railway can access it)")
    print("   • DON'T initialize with README (you already have one)")
    print("   • Click 'Create repository'")
    
    print("\n2️⃣ CONNECT LOCAL REPOSITORY TO GITHUB:")
    print("   Copy and run these commands in your terminal:")
    print("   ─" * 50)
    print("   git remote add origin https://github.com/YOUR-USERNAME/token-market-backend.git")
    print("   git branch -M main")
    print("   git push -u origin main")
    print("   ─" * 50)
    print("   📝 Replace YOUR-USERNAME with your actual GitHub username")
    
    print("\n3️⃣ VERIFY UPLOAD:")
    print("   • Refresh your GitHub repository page")
    print("   • You should see all your files uploaded")
    print("   • Look for: requirements.txt, start.py, Dockerfile, app/ folder")
    
    print("\n4️⃣ NOW DEPLOY TO RAILWAY:")
    print("   • Go to https://railway.app")
    print("   • Sign up/login with your GitHub account")
    print("   • Click 'Deploy from GitHub repo'")
    print("   • Select 'token-market-backend' from the list")
    print("   • Railway will automatically detect it's a Python app")
    
    print("\n5️⃣ ADD ENVIRONMENT VARIABLES IN RAILWAY:")
    print("   Click on your deployed project → Variables tab → Add these:")
    
    env_vars = {
        "SUPABASE_URL": "https://rrhdrkmomngxcjsatcpy.supabase.co",
        "SUPABASE_KEY": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJyaGRya21vbW5neGNqc2F0Y3B5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzU0MDQwODUsImV4cCI6MjA1MDk4MDA4NX0.yLnx5vQyZ49vwLlT1mKS_DGx1-MfLCXVZ4lJtWMIPlA",
        "JWT_SECRET_KEY": "token-market-super-secret-jwt-key-2025-production-ready",
        "ENVIRONMENT": "production",
        "PORT": "8000"
    }
    
    for key, value in env_vars.items():
        print(f"   {key} = {value}")
    
    print("\n6️⃣ DEPLOYMENT WILL START AUTOMATICALLY:")
    print("   • Railway reads your railway.toml config")
    print("   • Builds using: pip install -r requirements.txt")
    print("   • Starts with: python start.py serve")
    print("   • Health check: /health endpoint")
    print("   • You'll get a URL like: https://your-app.railway.app")
    
    print("\n7️⃣ UPDATE YOUR LOVABLE COMPONENT:")
    print("   Replace this line in TokenMarketLovable.tsx:")
    print("   const API_BASE_URL = 'https://your-backend-url.railway.app';")
    print("   With your actual Railway URL")
    
    print("\n🎯 ALTERNATIVE: QUICK TEST WITH NGROK")
    print("─" * 40)
    print("If you want to test immediately without GitHub:")
    print("1. Install ngrok: brew install ngrok")
    print("2. Start backend: python start.py serve")
    print("3. In another terminal: ngrok http 8000")
    print("4. Copy the https://...ngrok.io URL")
    print("5. Use that URL in your Lovable component")
    print("⚠️  ngrok URLs are temporary - use Railway for permanent solution")
    
    print("\n💡 TROUBLESHOOTING:")
    print("─" * 16)
    print("• Repository not showing up? Make sure it's PUBLIC on GitHub")
    print("• Build failing? Check that requirements.txt has all dependencies")
    print("• App not starting? Verify start.py has the serve command")
    print("• CORS errors? Your backend already allows all origins (*)")
    print("• Still issues? Check Railway logs in the deployment dashboard")
    
    print("\n✅ CHECKLIST:")
    print("─" * 10)
    checklist = [
        "[ ] GitHub repository created and PUBLIC",
        "[ ] Code pushed to GitHub (git push origin main)",
        "[ ] Railway connected to GitHub repository", 
        "[ ] Environment variables added in Railway",
        "[ ] Deployment successful (check Railway dashboard)",
        "[ ] Health check working (visit your-url.railway.app/health)",
        "[ ] Lovable component updated with new API_BASE_URL",
        "[ ] Test authentication and data loading in Lovable"
    ]
    
    for item in checklist:
        print(f"  {item}")
    
    print("\n🚀 ONCE DEPLOYED:")
    print("Your Lovable app will be able to connect to your backend!")
    print("The 'Failed to fetch' error will be resolved.")
    print("You'll have a fully working Token Market application! 🎉")

if __name__ == "__main__":
    show_github_setup()
