from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db
from app.core import deps

router = APIRouter()

@router.post("/reviews", response_model=schemas.PerformanceReview)
def create_review(
    *,
    db: Session = Depends(get_db),
    review_in: schemas.PerformanceReviewCreate,
    current_user: models.EmployeeSystemAccess = Depends(deps.get_current_active_superuser),
) -> Any:
    # Reviewer must be current user or admin? 
    # Logic: Reviewer ID in payload must match current user, or be admin override.
    if current_user.role.role_name != "Admin" and review_in.reviewer_id != current_user.employee_id:
        raise HTTPException(status_code=400, detail="Reviewer mismatch")
        
    review = models.PerformanceReview(**review_in.model_dump())
    db.add(review)
    db.commit()
    db.refresh(review)
    return review

@router.get("/reviews/{employee_id}", response_model=List[schemas.PerformanceReview])
def read_employee_reviews(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: models.EmployeeSystemAccess = Depends(deps.get_current_user),
) -> Any:
    # Access control: Self or Manager/Admin
    if current_user.role.role_name != "Admin" and current_user.employee_id != employee_id:
         # Check if manager...
         pass
    
    reviews = db.query(models.PerformanceReview).filter(models.PerformanceReview.employee_id == employee_id).all()
    return reviews
