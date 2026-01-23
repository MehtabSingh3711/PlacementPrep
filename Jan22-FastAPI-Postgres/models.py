from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func  # <--- Import func for automatic dates
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    
    # Login Information
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False) # <--- New
    password = Column(String, nullable=False)
    
    # Profile Information
    first_name = Column(String, nullable=True) # <--- New
    last_name = Column(String, nullable=True)  # <--- New
    phone_number = Column(String, nullable=True) # <--- New
    
    # System Status
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now()) # <--- New