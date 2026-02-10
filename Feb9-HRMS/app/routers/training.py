from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db
from app.core import deps

router = APIRouter()

@router.get("/programs", response_model=List[schemas.TrainingProgram])
def read_programs(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.EmployeeSystemAccess = Depends(deps.get_current_user),
) -> Any:
    programs = db.query(models.TrainingProgram).offset(skip).limit(limit).all()
    return programs

@router.post("/programs", response_model=schemas.TrainingProgram)
def create_program(
    *,
    db: Session = Depends(get_db),
    program_in: schemas.TrainingProgramCreate,
    current_user: models.EmployeeSystemAccess = Depends(deps.get_current_active_superuser),
) -> Any:
    program = models.TrainingProgram(**program_in.model_dump())
    db.add(program)
    db.commit()
    db.refresh(program)
    return program
