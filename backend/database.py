"""Database connection and session managements"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager
from typing import Generator

from shared.config import get_settings
from backend.models import Base

settings = get_settings()

# Create engine
engine = create_engine(
    settings.database_url,
    echo=False,  # Set to true for SQL query logging
    pool_pre_ping=True, # Verify connections before using
    pool_recycle=3600, # Recycle connections after 1 hour
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Initialize database by creating all tables"""
    Base.metadata.create_all(bind=engine)

def get_db() -> Generator[Session, None, None]:
    """
    Dependency function for FastAPI to get database

    Yields:
        Session: SQLAlchemy database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@contextmanager
def get_db_contect() -> Generator[Session, None, None]:
    """
    Context manager for database session (for use outside FastAPI)

    Usage:
        with get_db_context() as db:
            # use db session
    """
    db = SessionLocal()

    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()