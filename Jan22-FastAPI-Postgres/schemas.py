from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Base schema (Shared properties)
class UserBase(BaseModel):
    email: str
    username: str             # <--- New (Required)
    first_name: Optional[str] = None # <--- New (Optional)
    last_name: Optional[str] = None  # <--- New (Optional)
    phone_number: Optional[str] = None # <--- New (Optional)

# Schema for CREATING a user (Input)
class UserCreate(UserBase):
    password: str

# Schema for READING a user (Output)
class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime      # <--- New (Returns the creation time)

    class Config:
        from_attributes = True