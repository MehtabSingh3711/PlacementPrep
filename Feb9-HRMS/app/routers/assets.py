from typing import List, Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db
from app.core import deps

router = APIRouter()

@router.get("/", response_model=List[schemas.CompanyAsset])
def read_assets(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.EmployeeSystemAccess = Depends(deps.get_current_user),
) -> Any:
    assets = db.query(models.CompanyAsset).offset(skip).limit(limit).all()
    return assets

@router.post("/", response_model=schemas.CompanyAsset)
def create_asset(
    *,
    db: Session = Depends(get_db),
    asset_in: schemas.CompanyAssetCreate,
    current_user: models.EmployeeSystemAccess = Depends(deps.get_current_active_superuser),
) -> Any:
    asset = models.CompanyAsset(**asset_in.model_dump())
    db.add(asset)
    db.commit()
    db.refresh(asset)
    return asset
