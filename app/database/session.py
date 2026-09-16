from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config.settings import settings
from app.utils.logger import logger

# 1. Create the Database Engine
# connect_args={"check_same_thread": False} is required for SQLite in multithreaded apps
engine = create_engine(
    settings.DATABASE_URL, 
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
)

# 2. Create a Session Local class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 3. Create a Base class for our future SQL ORM models
Base = declarative_base()

def get_db():
    """
    Dependency function to get a DB session. 
    Ensures the connection is closed after use.
    """
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Database error: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()