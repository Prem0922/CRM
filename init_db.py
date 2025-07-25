from database import engine
from models import Base

def init_db():
    print("Dropping all existing tables...")
    Base.metadata.drop_all(bind=engine)
    print("Creating new database tables...")
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
    print("Database tables recreated successfully!") 