from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app import models, schemas
from app.core import deps # Wait, I named it app.core.deps
from app.core import security
from app.database import get_db

router = APIRouter()

from fastapi import Response

@router.post("/login", response_model=schemas.Token)
def login_access_token_json(
    response: Response,
    login_data: schemas.Login,
    db: Session = Depends(get_db), 
) -> Any:
    """
    Login using JSON body (Preferred for FastView/API clients)
    """
    user = db.query(models.EmployeeSystemAccess).filter(models.EmployeeSystemAccess.username == login_data.username).first()
    if not user or not security.verify_password(login_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    
    access_token_expires = timedelta(minutes=security.settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        subject=user.username, expires_delta=access_token_expires
    )
    
    # Set cookie for auto-auth in browser/FastView
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        max_age=security.settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        expires=security.settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/token", response_model=schemas.Token)
def login_access_token_multipart(
    db: Session = Depends(get_db), 
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = db.query(models.EmployeeSystemAccess).filter(models.EmployeeSystemAccess.username == form_data.username).first()
    if not user or not security.verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    
    access_token_expires = timedelta(minutes=security.settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        subject=user.username, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/signup", response_model=schemas.Employee)
def signup(
    employee_in: schemas.EmployeeCreate,
    user_in: schemas.SystemAccessCreate,
    db: Session = Depends(get_db)
) -> Any:
    """
    Register a new employee and their system access.
    In a real system, this might be split or admin-only, but for this task/demo it allows self-registration or admin creation.
    """
    # check if user exists
    user = db.query(models.EmployeeSystemAccess).filter(models.EmployeeSystemAccess.username == user_in.username).first()
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    
    # check if employee email exists
    employee = db.query(models.Employee).filter(models.Employee.email == employee_in.email).first()
    if employee:
         raise HTTPException(
            status_code=400,
            detail="The employee with this email already exists in the system.",
        )

    # Validate foreign keys existence (Department, Position)
    dept = db.query(models.Department).filter(models.Department.department_id == employee_in.department_id).first()
    if not dept:
        raise HTTPException(status_code=404, detail="Department not found")
    
    pos = db.query(models.JobPosition).filter(models.JobPosition.position_id == employee_in.position_id).first()
    if not pos:
        raise HTTPException(status_code=404, detail="Job Position not found")

    # Create Employee
    db_employee = models.Employee(**employee_in.model_dump())
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)

    # Create System Access
    hashed_password = security.get_password_hash(user_in.password)
    db_user = models.EmployeeSystemAccess(
        employee_id=db_employee.employee_id,
        role_id=user_in.role_id,
        username=user_in.username,
        password_hash=hashed_password,
        is_active=user_in.is_active
    )
    db.add(db_user)
    db.commit()
    
    return db_employee
