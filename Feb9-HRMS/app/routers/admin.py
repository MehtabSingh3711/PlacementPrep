from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db
from app.core import deps

router = APIRouter()

# --- Departments ---

@router.get("/departments", response_model=List[schemas.Department])
def read_departments(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.EmployeeSystemAccess = Depends(deps.get_current_user),
) -> Any:
    deps = db.query(models.Department).offset(skip).limit(limit).all()
    return deps

@router.post("/departments", response_model=schemas.Department)
def create_department(
    *,
    db: Session = Depends(get_db),
    department_in: schemas.DepartmentCreate,
    current_user: models.EmployeeSystemAccess = Depends(deps.get_current_active_superuser),
) -> Any:
    data = department_in.model_dump()
    # Check parent dept if provided
    if data.get("parent_department_id"):
        parent = db.query(models.Department).filter(models.Department.department_id == data["parent_department_id"]).first()
        if not parent:
             raise HTTPException(status_code=404, detail="Parent Department not found")
            
    dept = models.Department(**data)
    db.add(dept)
    db.commit()
    db.refresh(dept)
    return dept

# --- Job Positions ---

@router.get("/job-positions", response_model=List[schemas.JobPosition])
def read_job_positions(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.EmployeeSystemAccess = Depends(deps.get_current_user),
) -> Any:
    positions = db.query(models.JobPosition).offset(skip).limit(limit).all()
    return positions

@router.post("/job-positions", response_model=schemas.JobPosition)
def create_job_position(
    *,
    db: Session = Depends(get_db),
    job_in: schemas.JobPositionCreate,
    current_user: models.EmployeeSystemAccess = Depends(deps.get_current_active_superuser),
) -> Any:
    # Check dept exists
    dept = db.query(models.Department).filter(models.Department.department_id == job_in.department_id).first()
    if not dept:
        raise HTTPException(status_code=404, detail="Department not found")

    job = models.JobPosition(**job_in.model_dump())
    db.add(job)
    db.commit()
    db.refresh(job)
    return job

# --- User Roles ---

@router.get("/roles", response_model=List[schemas.UserRole])
def read_roles(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    # Publicly accessible for signup form population perhaps, or restricted
    roles = db.query(models.UserRole).offset(skip).limit(limit).all()
    return roles

@router.post("/roles", response_model=schemas.UserRole)
def create_role(
    *,
    db: Session = Depends(get_db),
    role_in: schemas.UserRoleCreate,
    current_user: models.EmployeeSystemAccess = Depends(deps.get_current_active_superuser),
):
    role = models.UserRole(**role_in.model_dump())
    db.add(role)
    db.commit()
    db.refresh(role)
    return role
