from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from urllib.parse import quote_plus  # <--- IMPORT THIS

# 1. Define your credentials
DB_USER = "postgres"
DB_PASSWORD = "Garry@123" 
DB_HOST = "localhost"
DB_NAME = "lms"

# 2. URL Encode the password (and user, just to be safe)
# This converts '@' to '%40', preventing syntax errors
encoded_user = quote_plus(DB_USER)
encoded_password = quote_plus(DB_PASSWORD)

# 3. Construct the connection string using the encoded values
SQLALCHEMY_DATABASE_URL = f"postgresql://{encoded_user}:{encoded_password}@{DB_HOST}/{DB_NAME}"

# Create the engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a SessionLocal class for database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for our ORM models
Base = declarative_base()

# Dependency to get the DB session per request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()