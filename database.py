from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Check for DATABASE_URL environment variable (for production)
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    # Use PostgreSQL in production (Render)
    SQLALCHEMY_DATABASE_URL = DATABASE_URL
    connect_args = {}
else:
    # Use SQLite for local development
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATABASE_FILE = "transit_card.db"
    DATABASE_PATH = os.path.join(BASE_DIR, DATABASE_FILE)
    SQLALCHEMY_DATABASE_URL = f"sqlite:///{DATABASE_PATH}"
    connect_args = {"check_same_thread": False}

# Create SQLAlchemy engine with proper settings
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args=connect_args,
    echo=True  # Enable SQL logging for debugging
)

# Create sessionmaker
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=True,  # Changed to True to ensure proper flushing
    bind=engine,
    expire_on_commit=False  # Added to prevent expired objects after commit
)

# Create Base class
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 