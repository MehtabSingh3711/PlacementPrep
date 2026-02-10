from typing import Generator, Optional
from fastapi import Depends, HTTPException, status, Query, Request
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.config import settings
from app.core import security
from app import models

# set auto_error=False to handle manually efficiently
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token", auto_error=False)

def get_current_user(
    request: Request,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
    token_query: str = Query(None, alias="token", description="Alternative: Pass token as query param")
) -> models.EmployeeSystemAccess:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    effective_token = None
    if token:
        effective_token = token
    elif token_query:
        effective_token = token_query
    elif request.cookies.get("access_token"):
        # Handle "Bearer <token>" format in cookie if present, or just token
        cookie_token = request.cookies.get("access_token")
        if cookie_token.startswith("Bearer "):
            effective_token = cookie_token.split(" ")[1]
        else:
            effective_token = cookie_token
            
    if not effective_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        payload = jwt.decode(
            effective_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(models.EmployeeSystemAccess).filter(models.EmployeeSystemAccess.username == username).first()
    if user is None:
        raise credentials_exception
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user

def get_current_active_superuser(
    current_user: models.EmployeeSystemAccess = Depends(get_current_user),
) -> models.EmployeeSystemAccess:
    # In a real app we'd check role permissions here.
    # For now, assuming anyone with a specific role ID or name is admin.
    # Let's assume role_name 'Admin' is checked via the relationship.
    if current_user.role.role_name != "Admin":
         raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user
