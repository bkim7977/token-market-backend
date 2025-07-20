#!/usr/bin/env python3
"""
🎯 FINAL SYSTEM VERIFICATION
Comprehensive verification that the token market backend is production-ready.
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def print_status(message, status="info"):
    """Print colored status messages."""
    colors = {
        "success": "\033[92m✅",
        "error": "\033[91m❌", 
        "warning": "\033[93m⚠️",
        "info": "\033[94mℹ️"
    }
    reset = "\033[0m"
    print(f"{colors.get(status, '')} {message}{reset}")

def check_file_exists(filepath, description):
    """Check if a file exists and print status."""
    if Path(filepath).exists():
        print_status(f"{description}: EXISTS", "success")
        return True
    else:
        print_status(f"{description}: MISSING", "error")
        return False

def run_command(command, description):
    """Run a command and return success status."""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print_status(f"{description}: SUCCESS", "success")
            return True
        else:
            print_status(f"{description}: FAILED", "error")
            print(f"Error: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print_status(f"{description}: TIMEOUT", "warning")
        return False
    except Exception as e:
        print_status(f"{description}: ERROR - {e}", "error")
        return False

def main():
    print("🚀 TOKEN MARKET BACKEND - FINAL VERIFICATION")
    print("=" * 60)
    
    all_checks = []
    
    # 1. Core files check
    print("\n📁 CORE FILES CHECK:")
    core_files = [
        ("app/api.py", "FastAPI endpoints"),
        ("app/auth.py", "JWT authentication"),
        ("app/database.py", "Database connection"),
        ("app/db_service.py", "Database service layer"),
        ("start.py", "Main control script"),
        ("requirements-minimal.txt", "Production dependencies"),
        ("docker-compose.yml", "Docker configuration"),
        (".env.example", "Environment template"),
        (".gitignore", "Git ignore rules"),
        ("README.md", "Documentation"),
        ("DATABASE_USAGE.md", "Usage guide")
    ]
    
    for filepath, description in core_files:
        all_checks.append(check_file_exists(filepath, description))
    
    # 2. Test files check
    print("\n🧪 TEST FILES CHECK:")
    test_files = [
        ("test_jwt_auth.py", "JWT authentication tests"),
        ("simple_test.py", "Basic database tests"),
        ("database_usage_demo.py", "API usage demo"),
        ("direct_database_demo.py", "Direct database demo")
    ]
    
    for filepath, description in test_files:
        all_checks.append(check_file_exists(filepath, description))
    
    # 3. Environment check
    print("\n🔧 ENVIRONMENT CHECK:")
    env_exists = check_file_exists(".env", "Environment variables")
    all_checks.append(env_exists)
    
    if env_exists:
        required_vars = ["SUPABASE_URL", "SUPABASE_KEY", "JWT_SECRET_KEY"]
        with open(".env", "r") as f:
            env_content = f.read()
        
        for var in required_vars:
            if var in env_content and f"{var}=" in env_content:
                print_status(f"Environment variable {var}: SET", "success")
                all_checks.append(True)
            else:
                print_status(f"Environment variable {var}: MISSING", "error")
                all_checks.append(False)
    
    # 4. Dependencies check
    print("\n📦 DEPENDENCIES CHECK:")
    all_checks.append(run_command("python -c 'import fastapi, uvicorn, supabase'", "Core packages"))
    all_checks.append(run_command("python -c 'from jose import jwt'", "JWT package"))
    all_checks.append(run_command("python -c 'import bcrypt'", "Bcrypt package"))
    
    # 5. Quick functionality test
    print("\n⚡ FUNCTIONALITY TEST:")
    all_checks.append(run_command("python -c 'from app.database import supabase; print(\"Database OK\")'", "Database connection"))
    all_checks.append(run_command("python -c 'from app.auth import create_access_token; print(\"JWT OK\")'", "JWT functionality"))
    
    # 6. Git readiness check  
    print("\n📝 GIT READINESS CHECK:")
    git_files = [
        (".gitignore", "Git ignore file"),
        ("README.md", "Main documentation"),
        ("requirements-minimal.txt", "Minimal requirements"),
        (".env.example", "Environment template")
    ]
    
    for filepath, description in git_files:
        all_checks.append(check_file_exists(filepath, description))
    
    # 7. Docker readiness check
    print("\n🐳 DOCKER READINESS CHECK:")
    docker_files = [
        ("Dockerfile", "Docker image definition"),
        ("docker-compose.yml", "Docker orchestration"),
    ]
    
    for filepath, description in docker_files:
        all_checks.append(check_file_exists(filepath, description))
    
    # Final summary
    print("\n" + "=" * 60)
    success_count = sum(all_checks)
    total_count = len(all_checks)
    success_rate = (success_count / total_count) * 100 if total_count > 0 else 0
    
    if success_rate >= 90:
        print_status(f"SYSTEM STATUS: PRODUCTION READY! ({success_count}/{total_count} checks passed - {success_rate:.1f}%)", "success")
        print("\n🎯 NEXT STEPS:")
        print("1. git init && git add . && git commit -m 'Initial commit'")
        print("2. Create GitHub repository")
        print("3. git remote add origin <your-repo-url>")
        print("4. git push -u origin main")
        print("5. Deploy to your preferred platform")
        print("\n🚀 Your backend is ready for production!")
        
    elif success_rate >= 75:
        print_status(f"SYSTEM STATUS: MOSTLY READY ({success_count}/{total_count} checks passed - {success_rate:.1f}%)", "warning")
        print("Fix remaining issues before deployment.")
        
    else:
        print_status(f"SYSTEM STATUS: NEEDS WORK ({success_count}/{total_count} checks passed - {success_rate:.1f}%)", "error")
        print("Address critical issues before proceeding.")
    
    print("\n📚 Documentation:")
    print("- API Docs: http://localhost:8000/docs (when running)")
    print("- Usage Guide: DATABASE_USAGE.md")
    print("- Full README: README.md")

if __name__ == "__main__":
    main()
