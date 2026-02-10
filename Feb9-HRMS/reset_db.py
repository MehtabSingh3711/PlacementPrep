import sys
import os
from sqlalchemy import create_engine, text
from app.core.config import settings
from app import models

def reset_database():
    print(f"Connecting to {settings.DATABASE_URL}...")
    engine = create_engine(settings.DATABASE_URL)
    
    try:
        with engine.connect() as conn:
            print("Dropping schema public cascade...")
            # Committing transaction for schema operations
            conn.execution_options(isolation_level="AUTOCOMMIT")
            conn.execute(text("DROP SCHEMA public CASCADE"))
            conn.execute(text("CREATE SCHEMA public"))
            conn.execute(text("GRANT ALL ON SCHEMA public TO public"))
            conn.commit()
            print("Schema reset.")
    except Exception as e:
        print(f"Error dropping/recreating schema: {e}")
        # If schema drop fails (e.g. permissions), fall back to drop_all but it might fail
        pass

    # Recreate all tables
    print("Recreating all tables...")
    models.Base.metadata.create_all(bind=engine)
    
    print("Database reset complete.")

if __name__ == "__main__":
    sys.path.append(os.getcwd())
    reset_database()
