"""
Railway-optimized database configuration
Handles missing environment variables gracefully
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from supabase import create_client, Client
import os
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Get database configuration with defaults for Railway
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")  # Fallback to SQLite
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://placeholder.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "placeholder-key")

# Initialize with error handling
engine = None
SessionLocal = None
Base = declarative_base()
supabase = None

def init_database():
    """Initialize database connections with error handling"""
    global engine, SessionLocal, supabase
    
    try:
        # SQLAlchemy setup
        if DATABASE_URL != "sqlite:///./test.db":
            logger.info("Initializing PostgreSQL connection...")
            engine = create_engine(DATABASE_URL)
            SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
        else:
            logger.info("Using SQLite fallback for testing...")
            engine = create_engine(DATABASE_URL)
            SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
        
        # Supabase client setup
        if SUPABASE_URL != "https://placeholder.supabase.co":
            logger.info("Initializing Supabase connection...")
            supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        else:
            logger.warning("Using placeholder Supabase configuration")
            # Create a mock client that won't fail
            supabase = None
            
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        # Don't fail completely - allow health checks to work
        supabase = None

# Initialize on import
init_database()
