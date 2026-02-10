from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db
from app.core import deps

router = APIRouter()

@router.get("/postings", response_model=List[schemas.JobPosting])
def read_job_postings(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
) -> Any:
    # Public endpoint?
    postings = db.query(models.JobPosting).filter(models.JobPosting.status == "Open").offset(skip).limit(limit).all()
    return postings

@router.post("/postings", response_model=schemas.JobPosting)
def create_job_posting(
    *,
    db: Session = Depends(get_db),
    posting_in: schemas.JobPostingCreate,
    current_user: models.EmployeeSystemAccess = Depends(deps.get_current_active_superuser),
) -> Any:
    posting = models.JobPosting(**posting_in.model_dump())
    db.add(posting)
    db.commit()
    db.refresh(posting)
    return posting

@router.post("/apply", response_model=schemas.JobApplication)
def apply_for_job(
    *,
    db: Session = Depends(get_db),
    application_in: schemas.JobApplicationCreate,
) -> Any:
    # Public endpoint
    application = models.JobApplication(**application_in.model_dump())
    db.add(application)
    db.commit()
    db.refresh(application)
    return application
