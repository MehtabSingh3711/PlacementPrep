import sys
import os
from sqlalchemy.orm import Session
from datetime import date
from app import models, database
from app.core import security

def seed_data():
    db = database.SessionLocal()
    try:
        print("Checking for existing data...")
        
        # 1. Check/Create Roles
        admin_role = db.query(models.UserRole).filter(models.UserRole.role_name == "Admin").first()
        if not admin_role:
             admin_role = models.UserRole(role_name="Admin", description="Administrator with full access", permissions={"all": True})
             db.add(admin_role)
             db.commit()
             db.refresh(admin_role)
             print(f"Created Role: Admin (ID: {admin_role.role_id})")
        else:
             print(f"Role 'Admin' exists (ID: {admin_role.role_id})")
        
        employee_role = db.query(models.UserRole).filter(models.UserRole.role_name == "Employee").first()
        if not employee_role:
            employee_role = models.UserRole(role_name="Employee", description="Standard employee access", permissions={"all": False})
            db.add(employee_role)
            db.commit()
            db.refresh(employee_role)
            print(f"Created Role: Employee (ID: {employee_role.role_id})")
        else:
            print(f"Role 'Employee' exists (ID: {employee_role.role_id})")

        # 2. Check/Create Root Department
        dept = db.query(models.Department).filter(models.Department.department_code == "HQ-000").first()
        if not dept:
            dept = models.Department(
                department_name="Management",
                department_code="HQ-000",
                description="Headquarters"
            )
            db.add(dept)
            db.commit()
            db.refresh(dept)
            print(f"Created Department: Management (ID: {dept.department_id})")
        else:
            print(f"Department 'Management' exists (ID: {dept.department_id})")

        # 3. Check/Create Root Position
        pos = db.query(models.JobPosition).filter(models.JobPosition.position_code == "CEO-001").first()
        if not pos:
            pos = models.JobPosition(
                position_title="CEO",
                position_code="CEO-001",
                department_id=dept.department_id,
                job_level="Executive",
                min_salary=0,
                max_salary=0
            )
            db.add(pos)
            db.commit()
            db.refresh(pos)
            print(f"Created Position: CEO (ID: {pos.position_id})")
        else:
            print(f"Position 'CEO' exists (ID: {pos.position_id})")

        # 4. Check/Create Admin Employee
        admin_emp = db.query(models.Employee).filter(models.Employee.employee_code == "EMP-001").first()
        if not admin_emp:
            # Use string mapping to map Enum value
            admin_emp = models.Employee(
                employee_code="EMP-001",
                first_name="Super",
                last_name="Admin",
                email="admin@hrms.com",
                department_id=dept.department_id,
                position_id=pos.position_id,
                date_of_joining=date.today(),
                employment_type="Full-time", 
                employment_status="Active"
            )
            db.add(admin_emp)
            db.commit()
            db.refresh(admin_emp)
            print(f"Created Employee: Super Admin (ID: {admin_emp.employee_id})")
        else:
            print(f"Employee 'Super Admin' exists (ID: {admin_emp.employee_id})")

        # 5. Check/Create System Access (Login)
        sys_access = db.query(models.EmployeeSystemAccess).filter(models.EmployeeSystemAccess.username == "admin1").first()
        if not sys_access:
            hashed_password = security.get_password_hash("admin123")
            sys_access = models.EmployeeSystemAccess(
                employee_id=admin_emp.employee_id,
                role_id=admin_role.role_id,
                username="admin1",
                password_hash=hashed_password,
                is_active=True
            )
            db.add(sys_access)
            db.commit()
            print("Created Login: username='admin1', password='admin123'")
        else:
            print("Login 'admin1' already exists.")
        
        print("Seed complete successfully!")

    except Exception as e:
        print(f"Error Seeding Data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    sys.path.append(os.getcwd())
    seed_data()
