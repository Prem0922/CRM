from database import engine
from sqlalchemy import text

def fix_cards_schema():
    """Add missing product column to cards table"""
    try:
        with engine.connect() as conn:
            # Check if product column already exists
            result = conn.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'cards' AND column_name = 'product'
            """))
            
            if result.fetchone():
                print("Product column already exists in cards table")
                return
            
            # Add the missing product column
            print("Adding missing 'product' column to cards table...")
            conn.execute(text("""
                ALTER TABLE cards 
                ADD COLUMN product VARCHAR
            """))
            
            # Commit the transaction
            conn.commit()
            print("Successfully added 'product' column to cards table!")
            
    except Exception as e:
        print(f"Error fixing cards schema: {e}")
        # Try to rollback if possible
        try:
            conn.rollback()
        except:
            pass
        raise e

if __name__ == "__main__":
    print("Starting database schema fix...")
    fix_cards_schema()
    print("Database schema fix completed!")
