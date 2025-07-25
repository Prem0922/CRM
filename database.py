from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Get the absolute path for the database file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_FILE = "transit_card.db"
DATABASE_PATH = os.path.join(BASE_DIR, DATABASE_FILE)

# Create SQLite database URL with absolute path
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

# Create SQLAlchemy engine with proper settings
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=True  # Enable SQL logging for debugging
)

# Create sessionmaker
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,  # Changed to False to prevent automatic flushing
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