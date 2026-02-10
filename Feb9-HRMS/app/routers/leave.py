from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db
from app.core import deps

router = APIRouter()

# --- Leave Types ---
@router.get("/types", response_model=List[schemas.LeaveType])
def read_leave_types(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.EmployeeSystemAccess = Depends(deps.get_current_user),
) -> Any:
    types = db.query(models.LeaveType).offset(skip).limit(limit).all()
    return types

@router.post("/types", response_model=schemas.LeaveType)
def create_leave_type(
    *,
    db: Session = Depends(get_db),
    type_in: schemas.LeaveTypeBase,
    current_user: models.EmployeeSystemAccess = Depends(deps.get_current_active_superuser),
) -> Any:
    leave_type = models.LeaveType(**type_in.model_dump())
    db.add(leave_type)
    db.commit()
    db.refresh(leave_type)
    return leave_type

# --- Leave Applications ---
@router.post("/apply", response_model=schemas.LeaveApplication)
def apply_leave(
    *,
    db: Session = Depends(get_db),
    leave_in: schemas.LeaveApplicationCreate,
    current_user: models.EmployeeSystemAccess = Depends(deps.get_current_user),
) -> Any:
    # Verify employee ID matches current user unless admin/manager
    if current_user.role.role_name != "Admin" and leave_in.employee_id != current_user.employee_id:
         raise HTTPException(status_code=400, detail="Cannot apply leave for another employee")

    # Simple days calculation (inclusive)
    days = (leave_in.end_date - leave_in.start_date).days + 1
    if days <= 0:
        raise HTTPException(status_code=400, detail="End date must be after start date")

    application = models.LeaveApplication(
        **leave_in.model_dump(),
        total_days=days,
        status="Pending"
    )
    db.add(application)
    db.commit()
    db.refresh(application)
    return application

@router.get("/pending", response_model=List[schemas.LeaveApplication])
def get_pending_leaves(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.EmployeeSystemAccess = Depends(deps.get_current_active_superuser), # Managers only
) -> Any:
    leaves = db.query(models.LeaveApplication).filter(models.LeaveApplication.status == "Pending").offset(skip).limit(limit).all()
    return leaves

@router.put("/{leave_id}/status", response_model=schemas.LeaveApplication)
def update_leave_status(
    leave_id: int,
    status: str, # Approved, Rejected
    db: Session = Depends(get_db),
    current_user: models.EmployeeSystemAccess = Depends(deps.get_current_active_superuser),
) -> Any:
    leave = db.query(models.LeaveApplication).filter(models.LeaveApplication.leave_id == leave_id).first()
    if not leave:
        raise HTTPException(status_code=404, detail="Leave application not found")
    
    leave.status = status
    leave.approved_by = current_user.employee_id
    from datetime import datetime
    leave.approved_on = datetime.now()
    
    # If approved, deduct balance (logic omitted for brevity, but should be here)
    if status == "Approved":
        # Check balance, deduct...
        pass
        
    db.add(leave)
    db.commit()
    db.refresh(leave)
    return leave
