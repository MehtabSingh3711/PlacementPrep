from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db
from app.core import deps

router = APIRouter()

@router.get("/", response_model=List[schemas.Employee])
def read_employees(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.EmployeeSystemAccess = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve employees.
    """
    employees = db.query(models.Employee).offset(skip).limit(limit).all()
    return employees

@router.post("/", response_model=schemas.Employee)
def create_employee(
    *,
    db: Session = Depends(get_db),
    employee_in: schemas.EmployeeCreate,
    current_user: models.EmployeeSystemAccess = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new employee. (Admin only)
    """
    employee = db.query(models.Employee).filter(models.Employee.email == employee_in.email).first()
    if employee:
        raise HTTPException(
            status_code=400,
            detail="The employee with this email already exists in the system.",
        )
    
    employee = models.Employee(**employee_in.model_dump())
    db.add(employee)
    db.commit()
    db.refresh(employee)
    return employee

@router.get("/{employee_id}", response_model=schemas.Employee)
def read_employee(
    *,
    db: Session = Depends(get_db),
    employee_id: int,
    current_user: models.EmployeeSystemAccess = Depends(deps.get_current_user),
) -> Any:
    """
    Get employee by ID.
    """
    employee = db.query(models.Employee).filter(models.Employee.employee_id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    # Add permission check here: Admins or the employee themselves
    if current_user.role.role_name != "Admin" and current_user.employee_id != employee_id:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return employee

@router.put("/{employee_id}", response_model=schemas.Employee)
def update_employee(
    *,
    db: Session = Depends(get_db),
    employee_id: int,
    employee_in: schemas.EmployeeUpdate,
    current_user: models.EmployeeSystemAccess = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update an employee. (Admin only)
    """
    employee = db.query(models.Employee).filter(models.Employee.employee_id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    update_data = employee_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(employee, field, value)
    
    db.add(employee)
    db.commit()
    db.refresh(employee)
    return employee
