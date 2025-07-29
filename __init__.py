# This file makes the backend directory a Python package from database import engine
from models import Base

def init_db():
    print("Creating database tables if they don't exist...")
    Base.metadata.create_all(bind=engine)
    print("Database tables ready!")

if __name__ == "__main__":
    init_db()
    print("Database initialization complete!") 
