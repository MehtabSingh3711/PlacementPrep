from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db
from app.core import security, deps
from datetime import date

router = APIRouter()

@router.post("/onboarding", status_code=status.HTTP_201_CREATED)
def onboard_employee(
    workflow_data: schemas.OnboardingWorkflow,
    db: Session = Depends(get_db),
    current_user: models.EmployeeSystemAccess = Depends(deps.get_current_user)
) -> Any:
    """
    Onboard a new employee:
    1. Create Employee Record
    2. Create System Access (optional)
    3. Assign Initial Onboarding Tasks
    All in a single transaction.
    """
    # Check permissions (e.g. only Admin or HR)
    if current_user.role.role_name not in ["Admin", "HR"]:
        raise HTTPException(status_code=403, detail="Not authorized to onboard employees")

    try:
        # 0. Generate Employee Code (Simple auto-generation)
        # In real app, use a sequence or max ID query.
        import random
        import string
        suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        e_code = f"EMP-{date.today().strftime('%Y%m')}-{suffix}"

        # 1. Create Employee
        db_employee = models.Employee(
            employee_code=e_code,
            first_name=workflow_data.first_name,
            last_name=workflow_data.last_name,
            email=workflow_data.email,
            department_id=workflow_data.department_id,
            position_id=workflow_data.position_id,
            date_of_joining=workflow_data.date_of_joining,
            employment_type=workflow_data.employment_type,
            employment_status=workflow_data.employment_status,
            created_by=current_user.employee_id
        )
        db.add(db_employee)
        db.flush() # Flush to get employee_id for next steps

        # 2. Create System Access (Login)
        # Check if username exists
        if db.query(models.EmployeeSystemAccess).filter(models.EmployeeSystemAccess.username == workflow_data.username).first():
            raise HTTPException(status_code=400, detail="Username already taken")
        
        hashed_password = security.get_password_hash(workflow_data.password)
        db_access = models.EmployeeSystemAccess(
            employee_id=db_employee.employee_id,
            role_id=workflow_data.role_id,
            username=workflow_data.username,
            password_hash=hashed_password,
            is_active=True
        )
        db.add(db_access)

        # 3. Assign Initial Task (if provided)
        if workflow_data.task_name:
            db_task = models.OnboardingTask(
                employee_id=db_employee.employee_id,
                task_name=workflow_data.task_name,
                task_description=workflow_data.task_description,
                assigned_to=current_user.employee_id,
                due_date=workflow_data.task_due_date,
                status=models.TaskStatus.Pending
            )
            db.add(db_task)
        
        db.commit()
        db.refresh(db_employee)
        
        return {
            "message": "Onboarding workflow completed successfully",
            "employee_id": db_employee.employee_id,
            "employee_code": db_employee.employee_code,
            "employee_name": f"{db_employee.first_name} {db_employee.last_name}",
            "username": workflow_data.username
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
