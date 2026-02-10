import sys
import os
from sqlalchemy import create_engine, inspect
from app.core.config import settings
from app import models

def verify():
    print(f"Connecting to {settings.DATABASE_URL}...")
    try:
        engine = create_engine(settings.DATABASE_URL)
        connection = engine.connect()
        print("Connection successful!")
        
        # Check tables
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        print(f"Found {len(tables)} tables.")
        
        expected_tables = [
            "departments", "job_positions", "employees", 
            "employee_system_access", "user_roles",
            "attendance", "leave_applications",
            "payroll", "salary_structure",
            "job_postings", "job_applications"
        ]
        
        missing = []
        for t in expected_tables:
            if t not in tables:
                missing.append(t)
        
        if missing:
            print(f"ERROR: Missing tables: {missing}")
            # Identify if we need to run init (main.py imports models which triggers drop_all/create_all only if run? No, main.py has code at top level)
            # If we import app.main, it will run the create_all code.
            print("Attempting to initialize tables via importing app.main...")
            from app import main
            # Re-check
            tables = inspector.get_table_names()
            print(f"Found {len(tables)} tables after init.")
        else:
            print("All core tables found.")

        connection.close()
        print("Verification complete.")
        
    except Exception as e:
        print(f"Verification FAILED: {e}")

if __name__ == "__main__":
    # Add project root to sys.path
    sys.path.append(os.getcwd())
    verify()
