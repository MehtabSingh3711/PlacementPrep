from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import date
from app import models, schemas
from app.database import get_db
from app.core import deps

router = APIRouter()

@router.post("/check-in", response_model=schemas.Attendance)
def check_in(
    *,
    db: Session = Depends(get_db),
    current_user: models.EmployeeSystemAccess = Depends(deps.get_current_user),
    notes: str = None
) -> Any:
    # Check if already checked in today
    today = date.today()
    existing = db.query(models.Attendance).filter(
        models.Attendance.employee_id == current_user.employee_id,
        models.Attendance.attendance_date == today
    ).first()
    
    if existing:
         raise HTTPException(status_code=400, detail="Already checked in for today")
    
    # Needs a time object. In a real app, this comes from the request or server time.
    # Using server time via SQL default or python datetime.now().time()
    from datetime import datetime
    now = datetime.now()
    
    attendance = models.Attendance(
        employee_id=current_user.employee_id,
        attendance_date=today,
        check_in=now.time(),
        status="Present",
        notes=notes
    )
    db.add(attendance)
    db.commit()
    db.refresh(attendance)
    return attendance

@router.post("/check-out", response_model=schemas.Attendance)
def check_out(
    *,
    db: Session = Depends(get_db),
    current_user: models.EmployeeSystemAccess = Depends(deps.get_current_user),
    notes: str = None
) -> Any:
    today = date.today()
    attendance = db.query(models.Attendance).filter(
        models.Attendance.employee_id == current_user.employee_id,
        models.Attendance.attendance_date == today
    ).first()
    
    if not attendance:
        raise HTTPException(status_code=404, detail="No attendance record found for today. Please check in first.")
    
    from datetime import datetime
    now = datetime.now()
    attendance.check_out = now.time()
    
    # Calculate work hours (simplified)
    # in real world, handle cross-day shifts
    dummy_date = date(2000, 1, 1)
    start = datetime.combine(dummy_date, attendance.check_in)
    end = datetime.combine(dummy_date, attendance.check_out)
    duration = (end - start).total_seconds() / 3600
    
    attendance.work_hours = round(duration, 2)
    if notes:
        attendance.notes = (attendance.notes or "") + " | Checkout: " + notes
        
    db.add(attendance)
    db.commit()
    db.refresh(attendance)
    return attendance

@router.get("/history", response_model=List[schemas.Attendance])
def read_attendance_history(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.EmployeeSystemAccess = Depends(deps.get_current_user),
) -> Any:
    # Employees verify their own, Admin verifies all?
    # Logic: If admin, can see all (maybe with filter). If employee, only own.
    # For now, simplistic: return all for admin, own for employee.
    
    if current_user.role.role_name == "Admin":
        attendance = db.query(models.Attendance).offset(skip).limit(limit).all()
    else:
        attendance = db.query(models.Attendance).filter(
            models.Attendance.employee_id == current_user.employee_id
        ).offset(skip).limit(limit).all()
        
    return attendance
