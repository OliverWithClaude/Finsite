"""
Migration script for v1.1 - Add price_history table
"""
from app.database import Base, engine
from sqlalchemy import text

def migrate():
    """Run migration to add price_history table."""
    print("Starting migration for v1.1 - Chart feature...")
    
    # Create price_history table
    Base.metadata.create_all(engine)
    print("✓ price_history table created")
    
    print("\nMigration completed successfully!")
    print("You can now use the chart feature for closed positions.")

if __name__ == "__main__":
    migrate()
