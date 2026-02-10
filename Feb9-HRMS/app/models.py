from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date, DateTime, Time, Text, Numeric, Enum, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from .database import Base

# Enums
class Gender(str, enum.Enum):
    Maloe = "Male"
    Female = "Female"
    Other = "Other"
    PreferNotToSay = "Prefer not to say"

class MaritalStatus(str, enum.Enum):
    Single = "Single"
    Married = "Married"
    Divorced = "Divorced"
    Widowed = "Widowed"

class EmploymentType(str, enum.Enum):
    FullTime = "Full-time"
    PartTime = "Part-time"
    Contract = "Contract"
    Intern = "Intern"
    Temporary = "Temporary"

class EmploymentStatus(str, enum.Enum):
    Active = "Active"
    OnLeave = "On Leave"
    Suspended = "Suspended"
    Terminated = "Terminated"
    Resigned = "Resigned"

class AttendanceStatus(str, enum.Enum):
    Present = "Present"
    Absent = "Absent"
    Late = "Late"
    HalfDay = "Half-day"
    OnLeave = "On Leave"
    Holiday = "Holiday"
    Weekend = "Weekend"

class LeaveApplicationStatus(str, enum.Enum):
    Pending = "Pending"
    Approved = "Approved"
    Rejected = "Rejected"
    Cancelled = "Cancelled"

class PayrollStatus(str, enum.Enum):
    Draft = "Draft"
    Processed = "Processed"
    Paid = "Paid"
    OnHold = "On Hold"

class PaymentMethod(str, enum.Enum):
    BankTransfer = "Bank Transfer"
    Check = "Check"
    Cash = "Cash"
    Other = "Other"

class BonusStatus(str, enum.Enum):
    Pending = "Pending"
    Approved = "Approved"
    Paid = "Paid"
    Rejected = "Rejected"

class JobPostingStatus(str, enum.Enum):
    Open = "Open"
    Closed = "Closed"
    OnHold = "On Hold"

class ApplicationStatus(str, enum.Enum):
    Applied = "Applied"
    Screening = "Screening"
    Interview = "Interview"
    Offered = "Offered"
    Rejected = "Rejected"
    Hired = "Hired"
    Withdrawn = "Withdrawn"

class InterviewType(str, enum.Enum):
    Phone = "Phone"
    Video = "Video"
    InPerson = "In-person"
    Technical = "Technical"
    HR = "HR"

class InterviewStatus(str, enum.Enum):
    Scheduled = "Scheduled"
    Completed = "Completed"
    Cancelled = "Cancelled"
    Rescheduled = "Rescheduled"

class InterviewResult(str, enum.Enum):
    Selected = "Selected"
    Rejected = "Rejected"
    OnHold = "On Hold"

class TaskStatus(str, enum.Enum):
    Pending = "Pending"
    InProgress = "In Progress"
    Completed = "Completed"

class CycleStatus(str, enum.Enum):
    Active = "Active"
    Completed = "Completed"
    Cancelled = "Cancelled"

class ReviewStatus(str, enum.Enum):
    Draft = "Draft"
    Submitted = "Submitted"
    Acknowledged = "Acknowledged"
    Completed = "Completed"

class GoalStatus(str, enum.Enum):
    NotStarted = "Not Started"
    InProgress = "In Progress"
    Completed = "Completed"
    Cancelled = "Cancelled"
    OnHold = "On Hold"

class Priority(str, enum.Enum):
    Low = "Low"
    Medium = "Medium"
    High = "High"
    Critical = "Critical"

class TrainingType(str, enum.Enum):
    Internal = "Internal"
    External = "External"
    Online = "Online"
    Workshop = "Workshop"
    Certification = "Certification"

class TrainingStatus(str, enum.Enum):
    Scheduled = "Scheduled"
    Ongoing = "Ongoing"
    Completed = "Completed"
    Cancelled = "Cancelled"

class EnrollmentStatus(str, enum.Enum):
    Enrolled = "Enrolled"
    Completed = "Completed"
    Cancelled = "Cancelled"
    InProgress = "In Progress"

class BenefitStatus(str, enum.Enum):
    Active = "Active"
    Inactive = "Inactive"
    Pending = "Pending"
    Cancelled = "Cancelled"

class AssetStatus(str, enum.Enum):
    Available = "Available"
    Assigned = "Assigned"
    UnderRepair = "Under Repair"
    Retired = "Retired"

class AssetCondition(str, enum.Enum):
    New = "New"
    Good = "Good"
    Fair = "Fair"
    Poor = "Poor"

class Severity(str, enum.Enum):
    VerbalWarning = "Verbal Warning"
    WrittenWarning = "Written Warning"
    Suspension = "Suspension"
    Termination = "Termination"

class PaymentFrequency(str, enum.Enum):
    Monthly = "Monthly"
    BiWeekly = "Bi-weekly"
    Weekly = "Weekly"

# Models

class Department(Base):
    __tablename__ = "departments"

    department_id = Column(Integer, primary_key=True, index=True)
    department_name = Column(String(100), nullable=False)
    department_code = Column(String(20), unique=True, nullable=False)
    parent_department_id = Column(Integer, ForeignKey("departments.department_id"), nullable=True)
    manager_id = Column(Integer, nullable=True) # Recursive relationship handle carefully
    budget = Column(Numeric(15, 2))
    location = Column(String(100))
    description = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    parent_department = relationship("Department", remote_side=[department_id], backref="sub_departments")
    employees = relationship("Employee", back_populates="department", foreign_keys="Employee.department_id")
    job_positions = relationship("JobPosition", back_populates="department")


class JobPosition(Base):
    __tablename__ = "job_positions"

    position_id = Column(Integer, primary_key=True, index=True)
    position_title = Column(String(100), nullable=False)
    position_code = Column(String(20), unique=True, nullable=False)
    department_id = Column(Integer, ForeignKey("departments.department_id"), nullable=False)
    job_level = Column(String(50))
    min_salary = Column(Numeric(12, 2))
    max_salary = Column(Numeric(12, 2))
    job_description = Column(Text)
    requirements = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    department = relationship("Department", back_populates="job_positions")
    employees = relationship("Employee", back_populates="position")


class Employee(Base):
    __tablename__ = "employees"

    employee_id = Column(Integer, primary_key=True, index=True)
    employee_code = Column(String(20), unique=True, nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    middle_name = Column(String(50))
    email = Column(String(100), unique=True, nullable=False, index=True)
    phone = Column(String(20))
    mobile = Column(String(20))
    date_of_birth = Column(Date)
    gender = Column(Enum(Gender))
    marital_status = Column(Enum(MaritalStatus))
    nationality = Column(String(50))
    national_id = Column(String(50))
    passport_number = Column(String(50))

    department_id = Column(Integer, ForeignKey("departments.department_id"), nullable=False)
    position_id = Column(Integer, ForeignKey("job_positions.position_id"), nullable=False)
    manager_id = Column(Integer, ForeignKey("employees.employee_id"), nullable=True)
    employment_type = Column(Enum(EmploymentType))
    employment_status = Column(Enum(EmploymentStatus))
    date_of_joining = Column(Date, nullable=False)
    date_of_leaving = Column(Date)
    probation_end_date = Column(Date)

    current_address = Column(Text)
    permanent_address = Column(Text)
    city = Column(String(100))
    state = Column(String(100))
    country = Column(String(100))
    postal_code = Column(String(20))

    emergency_contact_name = Column(String(100))
    emergency_contact_relationship = Column(String(50))
    emergency_contact_phone = Column(String(20))

    profile_picture = Column(String(255))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    created_by = Column(Integer)

    # Relationships
    department = relationship("Department", back_populates="employees", foreign_keys=[department_id])
    position = relationship("JobPosition", back_populates="employees")
    manager = relationship("Employee", remote_side=[employee_id], backref="direct_reports")
    
    education = relationship("EmployeeEducation", back_populates="employee")
    experience = relationship("EmployeeExperience", back_populates="employee")
    documents = relationship("EmployeeDocuments", back_populates="employee")
    attendances = relationship("Attendance", back_populates="employee")
    leave_applications = relationship("LeaveApplication", back_populates="employee", foreign_keys="LeaveApplication.employee_id")
    leave_balances = relationship("EmployeeLeaveBalance", back_populates="employee")
    
    system_access = relationship("EmployeeSystemAccess", back_populates="employee", uselist=False)


class EmployeeEducation(Base):
    __tablename__ = "employee_education"
    education_id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.employee_id"), nullable=False)
    degree = Column(String(100), nullable=False)
    institution = Column(String(200), nullable=False)
    field_of_study = Column(String(100))
    start_date = Column(Date)
    end_date = Column(Date)
    grade_gpa = Column(String(20))
    country = Column(String(100))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    employee = relationship("Employee", back_populates="education")


class EmployeeExperience(Base):
    __tablename__ = "employee_experience"
    experience_id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.employee_id"), nullable=False)
    company_name = Column(String(200), nullable=False)
    job_title = Column(String(100), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date)
    responsibilities = Column(Text)
    country = Column(String(100))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    employee = relationship("Employee", back_populates="experience")


class EmployeeDocuments(Base):
    __tablename__ = "employee_documents"
    document_id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.employee_id"), nullable=False)
    document_type = Column(String(50), nullable=False)
    document_name = Column(String(200), nullable=False)
    file_path = Column(String(255), nullable=False)
    file_size = Column(Integer)
    uploaded_by = Column(Integer)
    upload_date = Column(DateTime(timezone=True), server_default=func.now())
    expiry_date = Column(Date)
    notes = Column(Text)

    employee = relationship("Employee", back_populates="documents")


class WorkSchedule(Base):
    __tablename__ = "work_schedules"
    schedule_id = Column(Integer, primary_key=True, index=True)
    schedule_name = Column(String(100), nullable=False)
    monday_start = Column(Time)
    monday_end = Column(Time)
    tuesday_start = Column(Time)
    tuesday_end = Column(Time)
    wednesday_start = Column(Time)
    wednesday_end = Column(Time)
    thursday_start = Column(Time)
    thursday_end = Column(Time)
    friday_start = Column(Time)
    friday_end = Column(Time)
    saturday_start = Column(Time)
    saturday_end = Column(Time)
    sunday_start = Column(Time)
    sunday_end = Column(Time)
    total_hours_per_week = Column(Numeric(4, 2))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class EmployeeSchedule(Base):
    __tablename__ = "employee_schedules"
    assignment_id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.employee_id"), nullable=False)
    schedule_id = Column(Integer, ForeignKey("work_schedules.schedule_id"), nullable=False)
    effective_from = Column(Date, nullable=False)
    effective_to = Column(Date)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Attendance(Base):
    __tablename__ = "attendance"
    attendance_id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.employee_id"), nullable=False)
    attendance_date = Column(Date, nullable=False)
    check_in = Column(Time)
    check_out = Column(Time)
    work_hours = Column(Numeric(4, 2))
    overtime_hours = Column(Numeric(4, 2), default=0)
    status = Column(Enum(AttendanceStatus), default=AttendanceStatus.Present)
    location = Column(String(100))
    notes = Column(Text)
    approved_by = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    employee = relationship("Employee", back_populates="attendances")


class LeaveType(Base):
    __tablename__ = "leave_types"
    leave_type_id = Column(Integer, primary_key=True, index=True)
    leave_name = Column(String(100), nullable=False)
    leave_code = Column(String(20), unique=True, nullable=False)
    days_per_year = Column(Integer)
    is_paid = Column(Boolean, default=True)
    carry_forward_allowed = Column(Boolean, default=False)
    max_carry_forward_days = Column(Integer)
    requires_approval = Column(Boolean, default=True)
    description = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class EmployeeLeaveBalance(Base):
    __tablename__ = "employee_leave_balance"
    balance_id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.employee_id"), nullable=False)
    leave_type_id = Column(Integer, ForeignKey("leave_types.leave_type_id"), nullable=False)
    year = Column(Integer, nullable=False)
    total_days = Column(Numeric(5, 2), nullable=False)
    used_days = Column(Numeric(5, 2), default=0)
    remaining_days = Column(Numeric(5, 2), nullable=False)
    carried_forward = Column(Numeric(5, 2), default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    employee = relationship("Employee", back_populates="leave_balances")
    leave_type = relationship("LeaveType")


class LeaveApplication(Base):
    __tablename__ = "leave_applications"
    leave_id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.employee_id"), nullable=False)
    leave_type_id = Column(Integer, ForeignKey("leave_types.leave_type_id"), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    total_days = Column(Numeric(5, 2), nullable=False)
    reason = Column(Text, nullable=False)
    status = Column(Enum(LeaveApplicationStatus), default=LeaveApplicationStatus.Pending)
    applied_on = Column(DateTime(timezone=True), server_default=func.now())
    approved_by = Column(Integer, ForeignKey("employees.employee_id"))
    approved_on = Column(DateTime(timezone=True))
    rejection_reason = Column(Text)
    comments = Column(Text)

    employee = relationship("Employee", foreign_keys=[employee_id], back_populates="leave_applications")
    approver = relationship("Employee", foreign_keys=[approved_by])
    leave_type = relationship("LeaveType")


class SalaryStructure(Base):
    __tablename__ = "salary_structure"
    structure_id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.employee_id"), nullable=False)
    effective_from = Column(Date, nullable=False)
    effective_to = Column(Date)
    basic_salary = Column(Numeric(12, 2), nullable=False)
    house_rent_allowance = Column(Numeric(12, 2), default=0)
    transport_allowance = Column(Numeric(12, 2), default=0)
    medical_allowance = Column(Numeric(12, 2), default=0)
    special_allowance = Column(Numeric(12, 2), default=0)
    other_allowances = Column(Numeric(12, 2), default=0)
    provident_fund = Column(Numeric(12, 2), default=0)
    professional_tax = Column(Numeric(12, 2), default=0)
    income_tax = Column(Numeric(12, 2), default=0)
    insurance = Column(Numeric(12, 2), default=0)
    other_deductions = Column(Numeric(12, 2), default=0)
    gross_salary = Column(Numeric(12, 2), nullable=False)
    total_deductions = Column(Numeric(12, 2), default=0)
    net_salary = Column(Numeric(12, 2), nullable=False)
    currency = Column(String(10), default='USD')
    payment_frequency = Column(Enum(PaymentFrequency), default=PaymentFrequency.Monthly)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(Integer)


class Payroll(Base):
    __tablename__ = "payroll"
    payroll_id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.employee_id"), nullable=False)
    pay_period_start = Column(Date, nullable=False)
    pay_period_end = Column(Date, nullable=False)
    payment_date = Column(Date)
    basic_salary = Column(Numeric(12, 2), nullable=False)
    allowances = Column(Numeric(12, 2), default=0)
    overtime_pay = Column(Numeric(12, 2), default=0)
    bonuses = Column(Numeric(12, 2), default=0)
    commissions = Column(Numeric(12, 2), default=0)
    gross_pay = Column(Numeric(12, 2), nullable=False)
    tax_deductions = Column(Numeric(12, 2), default=0)
    insurance_deductions = Column(Numeric(12, 2), default=0)
    retirement_deductions = Column(Numeric(12, 2), default=0)
    loan_deductions = Column(Numeric(12, 2), default=0)
    other_deductions = Column(Numeric(12, 2), default=0)
    total_deductions = Column(Numeric(12, 2), default=0)
    net_pay = Column(Numeric(12, 2), nullable=False)
    status = Column(Enum(PayrollStatus), default=PayrollStatus.Draft)
    payment_method = Column(Enum(PaymentMethod))
    notes = Column(Text)
    processed_by = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class Bonus(Base):
    __tablename__ = "bonuses"
    bonus_id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.employee_id"), nullable=False)
    bonus_type = Column(String(50), nullable=False)
    amount = Column(Numeric(12, 2), nullable=False)
    bonus_date = Column(Date, nullable=False)
    reason = Column(Text)
    approved_by = Column(Integer, ForeignKey("employees.employee_id"))
    status = Column(Enum(BonusStatus), default=BonusStatus.Pending)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class JobPosting(Base):
    __tablename__ = "job_postings"
    posting_id = Column(Integer, primary_key=True, index=True)
    position_id = Column(Integer, ForeignKey("job_positions.position_id"), nullable=False)
    job_title = Column(String(100), nullable=False)
    department_id = Column(Integer, ForeignKey("departments.department_id"), nullable=False)
    vacancies = Column(Integer, default=1)
    job_description = Column(Text, nullable=False)
    requirements = Column(Text)
    min_experience = Column(Integer)
    max_experience = Column(Integer)
    min_salary = Column(Numeric(12, 2))
    max_salary = Column(Numeric(12, 2))
    location = Column(String(100))
    employment_type = Column(Enum(EmploymentType))
    posted_date = Column(Date, nullable=False)
    closing_date = Column(Date)
    status = Column(Enum(JobPostingStatus), default=JobPostingStatus.Open)
    posted_by = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class JobApplication(Base):
    __tablename__ = "job_applications"
    application_id = Column(Integer, primary_key=True, index=True)
    posting_id = Column(Integer, ForeignKey("job_postings.posting_id"), nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=False)
    current_company = Column(String(200))
    current_position = Column(String(100))
    total_experience = Column(Integer)
    expected_salary = Column(Numeric(12, 2))
    notice_period = Column(Integer)
    resume_path = Column(String(255))
    cover_letter = Column(Text)
    status = Column(Enum(ApplicationStatus), default=ApplicationStatus.Applied)
    applied_date = Column(DateTime(timezone=True), server_default=func.now())
    notes = Column(Text)


class Interview(Base):
    __tablename__ = "interviews"
    interview_id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("job_applications.application_id"), nullable=False)
    interview_round = Column(String(50), nullable=False)
    interview_type = Column(Enum(InterviewType), nullable=False)
    scheduled_date = Column(Date, nullable=False)
    scheduled_time = Column(Time, nullable=False)
    duration_minutes = Column(Integer, default=60)
    interviewer_id = Column(Integer, ForeignKey("employees.employee_id"))
    location = Column(String(100))
    meeting_link = Column(String(255))
    status = Column(Enum(InterviewStatus), default=InterviewStatus.Scheduled)
    feedback = Column(Text)
    rating = Column(Integer)
    result = Column(Enum(InterviewResult))
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class OnboardingTask(Base):
    __tablename__ = "onboarding_tasks"
    task_id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.employee_id"), nullable=False)
    task_name = Column(String(200), nullable=False)
    task_description = Column(Text)
    assigned_to = Column(Integer, ForeignKey("employees.employee_id"))
    due_date = Column(Date)
    status = Column(Enum(TaskStatus), default=TaskStatus.Pending)
    completion_date = Column(Date)
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class PerformanceCycle(Base):
    __tablename__ = "performance_cycles"
    cycle_id = Column(Integer, primary_key=True, index=True)
    cycle_name = Column(String(100), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    review_deadline = Column(Date)
    status = Column(Enum(CycleStatus), default=CycleStatus.Active)
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class PerformanceReview(Base):
    __tablename__ = "performance_reviews"
    review_id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.employee_id"), nullable=False)
    reviewer_id = Column(Integer, ForeignKey("employees.employee_id"), nullable=False)
    cycle_id = Column(Integer, ForeignKey("performance_cycles.cycle_id"), nullable=False)
    review_date = Column(Date, nullable=False)
    review_period_start = Column(Date, nullable=False)
    review_period_end = Column(Date, nullable=False)
    technical_skills_rating = Column(Integer)
    communication_rating = Column(Integer)
    teamwork_rating = Column(Integer)
    leadership_rating = Column(Integer)
    productivity_rating = Column(Integer)
    overall_rating = Column(Numeric(3, 2))
    strengths = Column(Text)
    areas_for_improvement = Column(Text)
    achievements = Column(Text)
    goals_next_period = Column(Text)
    reviewer_comments = Column(Text)
    employee_comments = Column(Text)
    status = Column(Enum(ReviewStatus), default=ReviewStatus.Draft)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class EmployeeGoal(Base):
    __tablename__ = "employee_goals"
    goal_id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.employee_id"), nullable=False)
    goal_title = Column(String(200), nullable=False)
    goal_description = Column(Text)
    category = Column(String(50))
    start_date = Column(Date, nullable=False)
    target_date = Column(Date, nullable=False)
    completion_date = Column(Date)
    progress_percentage = Column(Integer, default=0)
    status = Column(Enum(GoalStatus), default=GoalStatus.NotStarted)
    priority = Column(Enum(Priority), default=Priority.Medium)
    set_by = Column(Integer, ForeignKey("employees.employee_id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class TrainingProgram(Base):
    __tablename__ = "training_programs"
    program_id = Column(Integer, primary_key=True, index=True)
    program_name = Column(String(200), nullable=False)
    program_code = Column(String(20), unique=True, nullable=False)
    description = Column(Text)
    trainer_name = Column(String(100))
    training_type = Column(Enum(TrainingType))
    duration_hours = Column(Integer)
    start_date = Column(Date)
    end_date = Column(Date)
    location = Column(String(100))
    max_participants = Column(Integer)
    cost_per_participant = Column(Numeric(10, 2))
    status = Column(Enum(TrainingStatus), default=TrainingStatus.Scheduled)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class TrainingEnrollment(Base):
    __tablename__ = "training_enrollments"
    enrollment_id = Column(Integer, primary_key=True, index=True)
    program_id = Column(Integer, ForeignKey("training_programs.program_id"), nullable=False)
    employee_id = Column(Integer, ForeignKey("employees.employee_id"), nullable=False)
    enrollment_date = Column(Date, nullable=False)
    status = Column(Enum(EnrollmentStatus), default=EnrollmentStatus.Enrolled)
    completion_date = Column(Date)
    score = Column(Numeric(5, 2))
    certificate_issued = Column(Boolean, default=False)
    certificate_path = Column(String(255))
    feedback = Column(Text)
    approved_by = Column(Integer, ForeignKey("employees.employee_id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class BenefitPlan(Base):
    __tablename__ = "benefit_plans"
    plan_id = Column(Integer, primary_key=True, index=True)
    plan_name = Column(String(100), nullable=False)
    plan_type = Column(String(50), nullable=False)
    provider = Column(String(100))
    description = Column(Text)
    employee_contribution = Column(Numeric(10, 2))
    employer_contribution = Column(Numeric(10, 2))
    coverage_amount = Column(Numeric(12, 2))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class EmployeeBenefit(Base):
    __tablename__ = "employee_benefits"
    benefit_id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.employee_id"), nullable=False)
    plan_id = Column(Integer, ForeignKey("benefit_plans.plan_id"), nullable=False)
    enrollment_date = Column(Date, nullable=False)
    effective_from = Column(Date, nullable=False)
    effective_to = Column(Date)
    status = Column(Enum(BenefitStatus), default=BenefitStatus.Active)
    beneficiary_name = Column(String(100))
    beneficiary_relationship = Column(String(50))
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class CompanyAsset(Base):
    __tablename__ = "company_assets"
    asset_id = Column(Integer, primary_key=True, index=True)
    asset_name = Column(String(100), nullable=False)
    asset_type = Column(String(50), nullable=False)
    asset_code = Column(String(50), unique=True, nullable=False)
    serial_number = Column(String(100))
    purchase_date = Column(Date)
    purchase_price = Column(Numeric(12, 2))
    warranty_expiry = Column(Date)
    status = Column(Enum(AssetStatus), default=AssetStatus.Available)
    condition_status = Column(Enum(AssetCondition))
    location = Column(String(100))
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class AssetAssignment(Base):
    __tablename__ = "asset_assignments"
    assignment_id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, ForeignKey("company_assets.asset_id"), nullable=False)
    employee_id = Column(Integer, ForeignKey("employees.employee_id"), nullable=False)
    assigned_date = Column(Date, nullable=False)
    return_date = Column(Date)
    assigned_by = Column(Integer, ForeignKey("employees.employee_id"))
    return_condition = Column(String(50))
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class DisciplinaryAction(Base):
    __tablename__ = "disciplinary_actions"
    action_id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.employee_id"), nullable=False)
    action_type = Column(String(50), nullable=False)
    severity = Column(Enum(Severity))
    incident_date = Column(Date, nullable=False)
    description = Column(Text, nullable=False)
    action_taken = Column(Text, nullable=False)
    issued_by = Column(Integer, ForeignKey("employees.employee_id"), nullable=False)
    acknowledged_by_employee = Column(Boolean, default=False)
    acknowledgment_date = Column(Date)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class ExitInterview(Base):
    __tablename__ = "exit_interviews"
    exit_id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.employee_id"), nullable=False)
    resignation_date = Column(Date, nullable=False)
    last_working_date = Column(Date, nullable=False)
    reason_for_leaving = Column(String(100))
    feedback = Column(Text)
    would_recommend_company = Column(Boolean)
    would_consider_returning = Column(Boolean)
    conducted_by = Column(Integer, ForeignKey("employees.employee_id"))
    interview_date = Column(Date)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class UserRole(Base):
    __tablename__ = "user_roles"
    role_id = Column(Integer, primary_key=True, index=True)
    role_name = Column(String(50), unique=True, nullable=False)
    description = Column(Text)
    permissions = Column(JSON)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class EmployeeSystemAccess(Base):
    __tablename__ = "employee_system_access"
    access_id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.employee_id"), nullable=False)
    role_id = Column(Integer, ForeignKey("user_roles.role_id"), nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    last_login = Column(DateTime(timezone=True))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    employee = relationship("Employee", back_populates="system_access")
    role = relationship("UserRole")


class AuditLog(Base):
    __tablename__ = "audit_log"
    log_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("employees.employee_id"))
    action = Column(String(100), nullable=False)
    table_name = Column(String(50))
    record_id = Column(Integer)
    old_values = Column(JSON)
    new_values = Column(JSON)
    ip_address = Column(String(45))
    user_agent = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
