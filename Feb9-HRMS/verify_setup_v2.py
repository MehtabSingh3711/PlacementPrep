import sys
import os
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
from app.core.config import settings

def create_database_if_not_exists():
    # Parse the URL to switch to 'postgres' db
    # Assumes standard postgres url format
    from sqlalchemy.engine.url import make_url
    url = make_url(settings.DATABASE_URL)
    db_name = url.database
    
    # Connect to default 'postgres' database to check/create target db
    admin_url = url.set(database="postgres")
    
    print(f"Connecting to admin DB: {admin_url}...")
    try:
        engine = create_engine(admin_url)
        # SQLAlchemy engine might need isolation_level="AUTOCOMMIT" for CREATE DATABASE
        conn = engine.connect()
        conn.execution_options(isolation_level="AUTOCOMMIT")
        
        # Check if DB exists
        result = conn.execute(text(f"SELECT 1 FROM pg_database WHERE datname = '{db_name}'"))
        if not result.fetchone():
            print(f"Database '{db_name}' does not exist. Creating...")
            # We need to close the transaction or use autocommit for CREATE DATABASE
            # But with engine.connect(), we are in a transaction block usually?
            # Let's try raw connection or ensure autocommit
            conn.close()
            
            # Re-create engine with isolation level
            engine = create_engine(admin_url, isolation_level="AUTOCOMMIT")
            with engine.connect() as conn:
                conn.execute(text(f"CREATE DATABASE {db_name}"))
            print(f"Database '{db_name}' created successfully.")
        else:
            print(f"Database '{db_name}' already exists.")
            
    except OperationalError as e:
        print(f"Admin Connection Failed: {e}")
        return False
    except Exception as e:
        print(f"Error checking/creating DB: {e}")
        return False
    return True

def verify():
    if not create_database_if_not_exists():
        print("Skipping table check due to DB connection failure.")
        return

    print(f"Connecting to {settings.DATABASE_URL}...")
    try:
        from app import models, database
        # Trigger create_all
        print("Initializing tables...")
        models.Base.metadata.create_all(bind=database.engine)
        print("Tables initialized.")
        
        # Verify
        from sqlalchemy import inspect
        inspector = inspect(database.engine)
        tables = inspector.get_table_names()
        print(f"Tables found: {len(tables)}")
        print(tables)
        
    except Exception as e:
        print(f"Table verification failed: {e}")

if __name__ == "__main__":
    sys.path.append(os.getcwd())
    verify()
