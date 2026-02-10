from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app import models, database
from app.routers import (
    auth, employees, admin, attendance, leave, 
    payroll, recruitment, performance, training, benefits, assets
)
from app.core.config import settings


models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    openapi_url="/api/v1/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
)
# CORS
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(admin.router, prefix="/admin", tags=["Admin"])
app.include_router(employees.router, prefix="/employees", tags=["Employees"])
app.include_router(attendance.router, prefix="/attendance", tags=["Attendance"])
app.include_router(leave.router, prefix="/leave", tags=["Leave"])
app.include_router(payroll.router, prefix="/payroll", tags=["Payroll"])
app.include_router(recruitment.router, prefix="/recruitment", tags=["Recruitment"])
app.include_router(performance.router, prefix="/performance", tags=["Performance"])
app.include_router(training.router, prefix="/training", tags=["Training"])
app.include_router(benefits.router, prefix="/benefits", tags=["Benefits"])
app.include_router(assets.router, prefix="/assets", tags=["Assets"])

from app.routers import workflows
app.include_router(workflows.router, prefix="/workflows", tags=["Workflows"])

@app.get("/")
def root():
    return {"message": "Welcome to HRMS API"}
