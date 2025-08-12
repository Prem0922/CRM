from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from api import router
from database import Base, engine
from routers import auth
import models

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for now
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables
Base.metadata.create_all(bind=engine)

# Include the API router
app.include_router(router)

# Include auth router
app.include_router(auth.router, prefix="/auth", tags=["auth"])

# --- Admin endpoints for DB management ---
@app.get("/admin/db-info")
def get_db_info():
    try:
        from database import engine
        db_url = str(engine.url)
        return {
            "status": "success",
            "database_type": "PostgreSQL" if "postgresql" in db_url else "SQLite",
            "connection_string": db_url.split("@")[0] + "@***" if "@" in db_url else db_url
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/admin/db-test")
def test_db_connection():
    try:
        from database import engine
        from sqlalchemy import text
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version()"))
            version = result.fetchone()[0]
            return {
                "status": "success",
                "database_type": "PostgreSQL",
                "version": version
            }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/admin/schema-info")
def get_schema_info():
    try:
        from database import engine
        from sqlalchemy import text
        with engine.connect() as conn:
            # Get customers table schema
            customers_result = conn.execute(text("""
                SELECT column_name, data_type, is_nullable 
                FROM information_schema.columns 
                WHERE table_name = 'customers' 
                ORDER BY ordinal_position
            """))
            customers_schema = [{"column": row[0], "type": row[1], "nullable": row[2]} for row in customers_result]
            
            # Get cards table schema
            cards_result = conn.execute(text("""
                SELECT column_name, data_type, is_nullable 
                FROM information_schema.columns 
                WHERE table_name = 'cards' 
                ORDER BY ordinal_position
            """))
            cards_schema = [{"column": row[0], "type": row[1], "nullable": row[2]} for row in cards_result]
            
            return {
                "status": "success",
                "customers_schema": customers_schema,
                "cards_schema": cards_schema
            }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/admin/fix-cards-schema")
def fix_cards_schema():
    """Fix the cards table schema by adding missing product column"""
    try:
        from database import engine
        from sqlalchemy import text
        
        with engine.connect() as conn:
            # Check if product column already exists
            result = conn.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'cards' AND column_name = 'product'
            """))
            
            if result.fetchone():
                return {
                    "status": "success",
                    "message": "Product column already exists in cards table"
                }
            
            # Add the missing product column
            conn.execute(text("""
                ALTER TABLE cards 
                ADD COLUMN product VARCHAR
            """))
            
            # Commit the transaction
            conn.commit()
            
            return {
                "status": "success",
                "message": "Successfully added 'product' column to cards table"
            }
            
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error fixing cards schema: {str(e)}"
        }

@app.post("/admin/fix-all-schema")
def fix_all_schema():
    """Fix all schema mismatches between models and database tables"""
    try:
        from database import engine
        from sqlalchemy import text
        
        with engine.connect() as conn:
            print("Checking and fixing database schema...")
            
            # Fix cards table
            print("\n1. Checking cards table...")
            
            # Check if product column exists
            result = conn.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'cards' AND column_name = 'product'
            """))
            
            if not result.fetchone():
                print("  - Adding missing 'product' column to cards table...")
                conn.execute(text("""
                    ALTER TABLE cards 
                    ADD COLUMN product VARCHAR
                """))
                print("  - Successfully added 'product' column!")
            else:
                print("  - 'product' column already exists")
            
            # Check if notifications column exists in customers table
            print("\n2. Checking customers table...")
            result = conn.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'customers' AND column_name = 'notifications'
            """))
            
            if not result.fetchone():
                print("  - Adding missing 'notifications' column to customers table...")
                conn.execute(text("""
                    ALTER TABLE customers 
                    ADD COLUMN notifications VARCHAR DEFAULT 'SMS Enabled'
                """))
                print("  - Successfully added 'notifications' column!")
            else:
                print("  - 'notifications' column already exists")
            
            # Check if case_status, priority, category, assigned_agent, notes columns exist in cases table
            print("\n3. Checking cases table...")
            case_columns = [
                ('case_status', 'VARCHAR'),
                ('priority', 'VARCHAR'),
                ('category', 'VARCHAR'),
                ('assigned_agent', 'VARCHAR'),
                ('notes', 'TEXT')
            ]
            
            for col_name, col_type in case_columns:
                result = conn.execute(text(f"""
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_name = 'cases' AND column_name = '{col_name}'
                """))
                
                if not result.fetchone():
                    print(f"  - Adding missing '{col_name}' column to cases table...")
                    conn.execute(text(f"""
                        ALTER TABLE cases 
                        ADD COLUMN {col_name} {col_type}
                    """))
                    print(f"  - Successfully added '{col_name}' column!")
                else:
                    print(f"  - '{col_name}' column already exists")
            
            # Check if all required columns exist in trips table
            print("\n4. Checking trips table...")
            trip_columns = [
                ('start_time', 'TIMESTAMP'),
                ('end_time', 'TIMESTAMP'),
                ('entry_location', 'VARCHAR'),
                ('exit_location', 'VARCHAR'),
                ('fare', 'FLOAT'),
                ('route', 'VARCHAR'),
                ('operator', 'VARCHAR'),
                ('transit_mode', 'VARCHAR'),
                ('adjustable', 'VARCHAR')
            ]
            
            for col_name, col_type in trip_columns:
                result = conn.execute(text(f"""
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_name = 'trips' AND column_name = '{col_name}'
                """))
                
                if not result.fetchone():
                    print(f"  - Adding missing '{col_name}' column to trips table...")
                    conn.execute(text(f"""
                        ALTER TABLE trips 
                        ADD COLUMN {col_name} {col_type}
                    """))
                    print(f"  - Successfully added '{col_name}' column!")
                else:
                    print(f"  - '{col_name}' column already exists")
            
            # Commit all changes
            conn.commit()
            
            return {
                "status": "success",
                "message": "All schema fixes completed successfully!"
            }
            
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error fixing schema: {str(e)}"
        }

@app.post("/admin/generate-data")
def generate_data():
    try:
        from generate_data import main as generate_main
        generate_main()
        return {"status": "success", "message": "Data generated"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/admin/reset-db")
def reset_database():
    try:
        from database import Base, engine
        print("Resetting database schema...")
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
        return {"status": "success", "message": "Database schema reset successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/admin/delete-db")
def delete_db():
    try:
        from delete_db import delete_database
        delete_database()
        return {"status": "success", "message": "Database deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Do NOT run uvicorn here; Render will do it for you 