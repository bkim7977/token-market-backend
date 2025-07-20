#!/usr/bin/env python3
"""
Railway-optimized startup script for Token Market Backend
Handles missing environment variables gracefully
"""

import os
import sys
import logging
from pathlib import Path

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_environment():
    """Check and set default environment variables for Railway deployment"""
    
    # Required environment variables with safe defaults for Railway
    env_vars = {
        'DATABASE_URL': 'postgresql://localhost/tokenmarket',  # Default - will be overridden in Railway
        'SUPABASE_URL': 'https://placeholder.supabase.co',      # Default - will be overridden in Railway
        'SUPABASE_KEY': 'placeholder-key',                       # Default - will be overridden in Railway
        'JWT_SECRET_KEY': 'railway-default-secret-key',          # Default - should be overridden in Railway
        'DEBUG': 'false',
        'ENVIRONMENT': 'production',
        'PORT': '8000'
    }
    
    # Set defaults if not already set
    for key, default_value in env_vars.items():
        if not os.getenv(key):
            os.environ[key] = default_value
            logger.info(f"Set default {key}")
        else:
            logger.info(f"Using existing {key}")

def main():
    """Main startup function"""
    logger.info("Starting Token Market Backend on Railway...")
    
    # Set environment defaults
    check_environment()
    
    # Import and start the application
    try:
        import uvicorn
        # Use minimal test first to verify Railway deployment works
        from minimal_test import app
        
        port = int(os.getenv('PORT', 8000))
        logger.info(f"Starting minimal test server on port {port}")
        
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=port,
            log_level="info",
            access_log=True
        )
        
    except Exception as e:
        logger.error(f"Failed to start application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
