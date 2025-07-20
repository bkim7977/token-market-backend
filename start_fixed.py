#!/usr/bin/env python3
"""
Token Market Backend Startup Script
"""

import sys
import subprocess
import os

def run_tests():
    """Run the production RLS tests"""
    print("🧪 Running Production Database Tests...")
    try:
        result = subprocess.run([
            sys.executable, "test_database_rls.py"
        ], capture_output=True, text=True)
        
        print(result.stdout)
        if result.stderr:
            print("Errors:", result.stderr)
            
        return result.returncode == 0
    except Exception as e:
        print(f"Error running tests: {e}")
        return False

def run_simple_tests():
    """Run simple database tests"""
    print("🧪 Running Simple Database Tests...")
    try:
        result = subprocess.run([
            sys.executable, "test_simple.py"
        ], capture_output=True, text=True)
        
        print(result.stdout)
        if result.stderr:
            print("Errors:", result.stderr)
            
        return result.returncode == 0
    except Exception as e:
        print(f"Error running tests: {e}")
        return False

def run_jwt_tests():
    """Run JWT authentication tests"""
    print("🧪 Running JWT Authentication Tests...")
    try:
        result = subprocess.run([
            sys.executable, "test_jwt_auth.py"
        ], capture_output=True, text=True)
        
        print(result.stdout)
        if result.stderr:
            print("Errors:", result.stderr)
            
        return result.returncode == 0
    except Exception as e:
        print(f"Error running tests: {e}")
        return False

def start_api():
    """Start the FastAPI server"""
    print("🚀 Starting FastAPI Server...")
    try:
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "app.api:app", 
            "--reload", 
            "--host", "0.0.0.0", 
            "--port", "8000"
        ])
    except KeyboardInterrupt:
        print("\n👋 Server stopped")
    except Exception as e:
        print(f"Error starting server: {e}")

def print_help():
    """Print help information"""
    print("Usage: python start.py [command]")
    print("\nCommands:")
    print("  test        - Run production database tests (with RLS)")
    print("  test-simple - Run basic database functionality tests")
    print("  test-jwt    - Run JWT authentication tests (requires running server)")
    print("  serve       - Start the FastAPI server")
    print("  dev         - Run simple tests then start server")
    print("\nExamples:")
    print("  python start.py test")
    print("  python start.py test-simple")
    print("  python start.py serve")
    print("  python start.py test-jwt  # Run in another terminal while server is running")
    print("  python start.py dev")

def main():
    """Main function"""
    print("🎮 Token Market Backend")
    print("=" * 30)
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "test":
            success = run_tests()
            sys.exit(0 if success else 1)
        elif command == "test-simple":
            success = run_simple_tests()
            sys.exit(0 if success else 1)
        elif command == "test-jwt":
            success = run_jwt_tests()
            sys.exit(0 if success else 1)
        elif command == "serve":
            start_api()
        elif command == "dev":
            print("🔧 Development Mode: Running tests first...")
            if run_simple_tests():
                print("\n✅ Tests passed! Starting server...")
                start_api()
            else:
                print("\n❌ Tests failed. Fix issues before starting server.")
                sys.exit(1)
        else:
            print(f"Unknown command: {command}")
            print_help()
    else:
        print_help()

if __name__ == "__main__":
    main()
