from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db
from app.core import deps

router = APIRouter()

# --- Salary Structure ---
@router.post("/salary-structure", response_model=schemas.SalaryStructure)
def create_salary_structure(
    *,
    db: Session = Depends(get_db),
    structure_in: schemas.SalaryStructureCreate,
    current_user: models.EmployeeSystemAccess = Depends(deps.get_current_active_superuser),
) -> Any:
    # Check if active structure exists and update end_date?
    # Simplified: just create new
    structure = models.SalaryStructure(**structure_in.model_dump())
    db.add(structure)
    db.commit()
    db.refresh(structure)
    return structure

@router.get("/salary-structure/{employee_id}", response_model=List[schemas.SalaryStructure])
def read_salary_structure(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: models.EmployeeSystemAccess = Depends(deps.get_current_active_superuser), 
) -> Any:
    structures = db.query(models.SalaryStructure).filter(models.SalaryStructure.employee_id == employee_id).all()
    return structures

# --- Payroll Processing ---
@router.post("/process", response_model=schemas.Payroll)
def process_payroll(
    *,
    db: Session = Depends(get_db),
    payroll_in: schemas.PayrollCreate, # In real app, might just take period and employee_id, and calc rest
    current_user: models.EmployeeSystemAccess = Depends(deps.get_current_active_superuser),
) -> Any:
    payroll = models.Payroll(**payroll_in.model_dump())
    db.add(payroll)
    db.commit()
    db.refresh(payroll)
    return payroll
