from typing import List, Optional, Any
from pydantic import BaseModel, EmailStr
from datetime import date, datetime, time
from decimal import Decimal
from enum import Enum

# Use strings for Enums in Pydantic to match SQLAlchemy Enums easily
# Or redefine them here. Re-using keys as strings is easiest.

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# --- Department Schemas ---
class DepartmentBase(BaseModel):
    department_name: str
    department_code: str
    parent_department_id: Optional[int] = None
    manager_id: Optional[int] = None
    budget: Optional[Decimal] = None
    location: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = True

class DepartmentCreate(DepartmentBase):
    pass

class DepartmentUpdate(DepartmentBase):
    pass

class Department(DepartmentBase):
    department_id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

# --- Job Position Schemas ---
class JobPositionBase(BaseModel):
    position_title: str
    position_code: str
    department_id: int
    job_level: Optional[str] = None
    min_salary: Optional[Decimal] = None
    max_salary: Optional[Decimal] = None
    job_description: Optional[str] = None
    requirements: Optional[str] = None
    is_active: Optional[bool] = True

class JobPositionCreate(JobPositionBase):
    pass

class JobPosition(JobPositionBase):
    position_id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True

# --- Employee Schemas ---
class EmployeeBase(BaseModel):
    employee_code: str
    first_name: str
    last_name: str
    middle_name: Optional[str] = None
    email: EmailStr
    phone: Optional[str] = None
    mobile: Optional[str] = None
    date_of_birth: Optional[date] = None
    gender: Optional[str] = None # Enum
    marital_status: Optional[str] = None # Enum
    nationality: Optional[str] = None
    national_id: Optional[str] = None
    passport_number: Optional[str] = None
    department_id: int
    position_id: int
    manager_id: Optional[int] = None
    employment_type: Optional[str] = None # Enum
    employment_status: Optional[str] = None # Enum
    date_of_joining: date
    date_of_leaving: Optional[date] = None
    probation_end_date: Optional[date] = None
    current_address: Optional[str] = None
    permanent_address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_relationship: Optional[str] = None
    emergency_contact_phone: Optional[str] = None
    profile_picture: Optional[str] = None
    is_active: Optional[bool] = True

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeUpdate(EmployeeBase):
    pass

class Employee(EmployeeBase):
    employee_id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True

# --- User/Auth Schemas ---
class UserRoleBase(BaseModel):
    role_name: str
    description: Optional[str] = None
    permissions: Optional[dict] = None
    is_active: Optional[bool] = True

class UserRoleCreate(UserRoleBase):
    pass

class UserRole(UserRoleBase):
    role_id: int
    
    class Config:
        from_attributes = True

class SystemAccessBase(BaseModel):
    username: str
    role_id: int
    employee_id: int
    is_active: Optional[bool] = True

class SystemAccessCreate(SystemAccessBase):
    password: str

class SystemAccess(SystemAccessBase):
    access_id: int
    last_login: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class Login(BaseModel):
    username: str
    password: str

class SignUp(BaseModel):
    # Combined for registering a new employee + user logic
    # Simplified for demo: verify checks first
    employee: EmployeeCreate
    user_access: SystemAccessCreate

# --- Attendance Schemas ---
class AttendanceBase(BaseModel):
    employee_id: int
    attendance_date: date
    check_in: Optional[time] = None
    check_out: Optional[time] = None
    status: Optional[str] = "Present"
    location: Optional[str] = None
    notes: Optional[str] = None

class AttendanceCreate(AttendanceBase):
    pass

class Attendance(AttendanceBase):
    attendance_id: int
    work_hours: Optional[Decimal] = None
    overtime_hours: Optional[Decimal] = None
    
    class Config:
        from_attributes = True

# --- Leave Schemas ---
class LeaveTypeBase(BaseModel):
    leave_name: str
    leave_code: str
    days_per_year: Optional[int] = None
    is_paid: Optional[bool] = True
    carry_forward_allowed: Optional[bool] = False
    
class LeaveType(LeaveTypeBase):
    leave_type_id: int
    class Config:
        from_attributes = True

class LeaveApplicationBase(BaseModel):
    employee_id: int
    leave_type_id: int
    start_date: date
    end_date: date
    reason: str

class LeaveApplicationCreate(LeaveApplicationBase):
    pass

class LeaveApplication(LeaveApplicationBase):
    leave_id: int
    total_days: Decimal
    status: str
    applied_on: datetime
    
    class Config:
        from_attributes = True

# --- Recruitment Schemas ---
class JobPostingBase(BaseModel):
    position_id: int
    job_title: str
    department_id: int
    vacancies: int = 1
    job_description: str
    requirements: Optional[str] = None

class JobPostingCreate(JobPostingBase):
    pass

class JobPosting(JobPostingBase):
    posting_id: int
    status: str
    posted_date: date
    
    class Config:
        from_attributes = True

class JobApplicationBase(BaseModel):
    posting_id: int
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    resume_path: Optional[str] = None

class JobApplicationCreate(JobApplicationBase):
    pass

class JobApplication(JobApplicationBase):
    application_id: int
    status: str
    applied_date: datetime
    
    class Config:
        from_attributes = True

# --- Payroll Schemas ---
class SalaryStructureBase(BaseModel):
    employee_id: int
    effective_from: date
    basic_salary: Decimal
    house_rent_allowance: Optional[Decimal] = 0
    gross_salary: Decimal
    net_salary: Decimal

class SalaryStructureCreate(SalaryStructureBase):
    pass

class SalaryStructure(SalaryStructureBase):
    structure_id: int
    created_at: Optional[datetime]
    class Config:
        from_attributes = True

class PayrollBase(BaseModel):
    employee_id: int
    pay_period_start: date
    pay_period_end: date
    basic_salary: Decimal
    gross_pay: Decimal
    net_pay: Decimal
    status: Optional[str] = "Draft"

class PayrollCreate(PayrollBase):
    pass

class Payroll(PayrollBase):
    payroll_id: int
    created_at: Optional[datetime]
    class Config:
        from_attributes = True

# --- Performance Schemas ---
class PerformanceReviewBase(BaseModel):
    employee_id: int
    reviewer_id: int
    cycle_id: int
    review_date: date
    overall_rating: Optional[Decimal] = None
    status: Optional[str] = "Draft"

class PerformanceReviewCreate(PerformanceReviewBase):
    pass

class PerformanceReview(PerformanceReviewBase):
    review_id: int
    created_at: Optional[datetime]
    class Config:
        from_attributes = True

# --- Training Schemas ---
class TrainingProgramBase(BaseModel):
    program_name: str
    program_code: str
    status: Optional[str] = "Scheduled"

class TrainingProgramCreate(TrainingProgramBase):
    pass

class TrainingProgram(TrainingProgramBase):
    program_id: int
    class Config:
        from_attributes = True

# --- Asset Schemas ---
class CompanyAssetBase(BaseModel):
    asset_name: str
    asset_code: str
    asset_type: str
    status: Optional[str] = "Available"

class CompanyAssetCreate(CompanyAssetBase):
    pass

class CompanyAsset(CompanyAssetBase):
    asset_id: int
    class Config:
        from_attributes = True

class OnboardingTaskCreate(BaseModel):
    task_name: str
    task_description: Optional[str] = None
    due_date: Optional[date] = None

class SystemAccessOnboarding(BaseModel):
    username: str
    password: str
    role_id: int
    is_active: Optional[bool] = True

class OnboardingWorkflow(BaseModel):
    # Employee Fields
    first_name: str
    last_name: str
    email: EmailStr
    department_id: int
    position_id: int
    date_of_joining: date
    employment_type: str = "Full-time"
    employment_status: str = "Active"
    
    # System Access Fields
    username: str
    password: str
    role_id: int
    
    # Initial Task Fields (Simplified to one task for flat UI)
    task_name: Optional[str] = "Complete Profile"
    task_description: Optional[str] = "Please complete your employee profile"
    task_due_date: Optional[date] = None
