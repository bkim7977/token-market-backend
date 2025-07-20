#!/usr/bin/env python3
"""
🚀 DEPLOYMENT HELPER
Automate backend deployment for Lovable integration
"""

import os
import subprocess
import sys

def run_command(command, description):
    """Run a command and print the result"""
    print(f"\n🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} successful")
            if result.stdout:
                print(result.stdout)
        else:
            print(f"❌ {description} failed")
            print(result.stderr)
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def check_git_status():
    """Check if we're in a git repository"""
    return os.path.exists('.git')

def deploy_to_railway():
    """Deploy to Railway"""
    print("\n🚂 RAILWAY DEPLOYMENT")
    print("=" * 40)
    
    if not check_git_status():
        print("❌ Not a git repository. Initializing...")
        run_command("git init", "Initialize git repository")
        run_command("git add .", "Add all files")
        run_command('git commit -m "Initial commit for deployment"', "Initial commit")
    
    print("\n📋 Railway Deployment Steps:")
    print("1. Go to https://railway.app")
    print("2. Sign up/in with GitHub")
    print("3. Click 'Deploy from GitHub repo'")
    print("4. Select this repository")
    print("5. Add these environment variables:")
    
    env_vars = {
        "SUPABASE_URL": "https://rrhdrkmomngxcjsatcpy.supabase.co",
        "SUPABASE_KEY": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJyaGRya21vbW5neGNqc2F0Y3B5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzU0MDQwODUsImV4cCI6MjA1MDk4MDA4NX0.yLnx5vQyZ49vwLlT1mKS_DGx1-MfLCXVZ4lJtWMIPlA",
        "JWT_SECRET_KEY": "your-super-secret-jwt-key-make-it-long-and-random-123456789",
        "ENVIRONMENT": "production",
        "PORT": "8000"
    }
    
    for key, value in env_vars.items():
        print(f"   {key}={value}")
    
    print("\n6. Railway will automatically deploy using:")
    print("   - Build: pip install -r requirements.txt")
    print("   - Start: python start.py serve")
    print("   - Health check: /health endpoint")

def deploy_with_ngrok():
    """Quick testing with ngrok"""
    print("\n🌐 NGROK QUICK TEST")
    print("=" * 30)
    
    print("For immediate testing without full deployment:")
    print("\n1. Install ngrok:")
    print("   Mac: brew install ngrok")
    print("   Windows: Download from ngrok.com")
    
    print("\n2. Start your backend locally:")
    print("   python start.py serve")
    
    print("\n3. In another terminal, run:")
    print("   ngrok http 8000")
    
    print("\n4. Copy the https URL (e.g., https://abc123.ngrok.io)")
    print("5. Update your Lovable component's API_BASE_URL")
    
    print("\n⚠️  Note: ngrok URLs are temporary and change each time!")

def update_lovable_component():
    """Show how to update the Lovable component"""
    print("\n💖 UPDATE LOVABLE COMPONENT")
    print("=" * 35)
    
    print("After deploying your backend, update TokenMarketLovable.tsx:")
    print("\n// Replace this line:")
    print("const API_BASE_URL = 'https://your-backend-url.railway.app';")
    print("\n// With your actual deployed URL, for example:")
    print("const API_BASE_URL = 'https://token-market-backend-production.railway.app';")
    
    print("\nOr for environment-aware configuration:")
    print("""
const API_BASE_URL = process.env.NODE_ENV === 'development'
  ? 'http://localhost:8000'
  : 'https://your-actual-deployed-url.railway.app';
    """)

def check_deployment_readiness():
    """Check if the project is ready for deployment"""
    print("\n✅ DEPLOYMENT READINESS CHECK")
    print("=" * 40)
    
    required_files = [
        'requirements.txt',
        'start.py', 
        'Dockerfile',
        'railway.toml'
    ]
    
    all_ready = True
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file} - Found")
        else:
            print(f"❌ {file} - Missing")
            all_ready = False
    
    # Check if start.py has serve command
    if os.path.exists('start.py'):
        with open('start.py', 'r') as f:
            content = f.read()
            if 'serve' in content and 'uvicorn' in content:
                print("✅ start.py - Has serve command")
            else:
                print("❌ start.py - Missing serve command")
                all_ready = False
    
    if all_ready:
        print("\n🚀 Your project is DEPLOYMENT READY!")
    else:
        print("\n⚠️  Some files are missing. Run the setup again.")

def main():
    print("🚀 LOVABLE DEPLOYMENT HELPER")
    print("=" * 50)
    
    print("\nYour Lovable app needs your backend deployed online!")
    print("Current issue: Lovable (hosted) → localhost:8000 (local) = ❌ Failed to fetch")
    print("Solution: Deploy backend online so Lovable can reach it ✅")
    
    print("\n📋 DEPLOYMENT OPTIONS:")
    print("1. 🚂 Railway (Recommended - Free & Easy)")
    print("2. 🌐 Ngrok (Quick testing - Temporary)")
    print("3. 🔧 Other platforms (Render, Heroku)")
    
    choice = input("\nSelect option (1, 2, 3) or 'check' to verify readiness: ").strip()
    
    if choice == 'check':
        check_deployment_readiness()
    elif choice == '1':
        check_deployment_readiness()
        deploy_to_railway()
        update_lovable_component()
    elif choice == '2':
        deploy_with_ngrok()
        update_lovable_component()
    elif choice == '3':
        print("\n🔧 OTHER DEPLOYMENT OPTIONS:")
        print("• Render.com - Free tier available")
        print("• Heroku - Has free tier limitations")  
        print("• Google Cloud Run - Pay per use")
        print("• AWS Lambda - Serverless option")
        print("\nAll require similar environment variables and configuration.")
        update_lovable_component()
    else:
        print("Invalid choice. Run the script again.")
    
    print("\n✨ NEXT STEPS:")
    print("1. Deploy your backend using your chosen method")
    print("2. Get the deployed URL")
    print("3. Update API_BASE_URL in your Lovable component") 
    print("4. Test authentication and data loading in Lovable")
    print("5. Your Token Market is live! 🎉")

if __name__ == "__main__":
    main()
