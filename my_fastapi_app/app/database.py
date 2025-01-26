from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import OperationalError, ProgrammingError
import logging
from .config import settings
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Configure logging
logging.basicConfig(level=settings.log_level)
logger = logging.getLogger(__name__)

def create_database_if_not_exists():
    """Create database if it doesn't exist"""
    # Connection string to postgres default database
    default_db_url = f"postgresql://{settings.db_user}:{settings.db_password}@{settings.db_host}:{settings.db_port}/postgres"
    
    try:
        # Try connecting to the target database first
        conn = psycopg2.connect(
            dbname=settings.db_name,
            user=settings.db_user,
            password=settings.db_password,
            host=settings.db_host,
            port=settings.db_port
        )
        conn.close()
        logger.info(f"Database '{settings.db_name}' already exists")
        return True
    except psycopg2.OperationalError:
        logger.info(f"Database '{settings.db_name}' not found. Creating...")
        
        try:
            # Connect to default postgres database to create new db
            conn = psycopg2.connect(
                dbname="postgres",
                user=settings.db_user,
                password=settings.db_password,
                host=settings.db_host,
                port=settings.db_port
            )
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cur = conn.cursor()
            
            # Create database
            cur.execute(f"CREATE DATABASE {settings.db_name}")
            
            cur.close()
            conn.close()
            logger.info(f"Database '{settings.db_name}' created successfully")
            return True
        except Exception as e:
            logger.error(f"Error creating database: {e}")
            raise

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.db_user}:{settings.db_password}@{settings.db_host}:{settings.db_port}/{settings.db_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def check_table_exists(table_name: str) -> bool:
    """Check if a table exists in the database"""
    inspector = inspect(engine)
    return table_name in inspector.get_table_names()

def init_db():
    """Initialize database with proper error handling"""
    try:
        # First ensure database exists
        create_database_if_not_exists()
        
        # Check if tables exist
        if not check_table_exists("items"):
            logger.info("Creating database tables...")
            Base.metadata.create_all(bind=engine)
            logger.info("Database tables created successfully")
        else:
            logger.info("Database tables already exist")
            
        # Verify database connection
        db = SessionLocal()
        try:
            # Test query
            db.execute(text("SELECT 1"))
            logger.info("Database connection verified successfully")
        finally:
            db.close()
            
    except OperationalError as e:
        logger.error(f"Database connection error: {e}")
        raise
    except ProgrammingError as e:
        logger.error(f"Database schema error: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error during database initialization: {e}")
        raise