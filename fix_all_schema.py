from database import engine
from sqlalchemy import text

def fix_all_schema():
    """Fix all schema mismatches between models and database tables"""
    try:
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
            print("\n✅ All schema fixes completed successfully!")
            
    except Exception as e:
        print(f"❌ Error fixing schema: {e}")
        # Try to rollback if possible
        try:
            conn.rollback()
        except:
            pass
        raise e

if __name__ == "__main__":
    print("Starting comprehensive database schema fix...")
    fix_all_schema()
    print("Database schema fix completed!")
