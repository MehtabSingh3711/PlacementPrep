from fastapi.testclient import TestClient
from app.main import app
from app import schemas

client = TestClient(app)

from app import models, database

def get_valid_ids():
    db = database.SessionLocal()
    try:
        dept = db.query(models.Department).first()
        pos = db.query(models.JobPosition).first()
        role = db.query(models.UserRole).filter(models.UserRole.role_name == "Employee").first()
        return dept.department_id, pos.position_id, role.role_id
    finally:
        db.close()

def test_onboarding():
    # Login as admin to get token
    login_response = client.post("/auth/login", json={"username": "admin1", "password": "admin123"})
    if login_response.status_code != 200:
        print(f"Login failed: {login_response.text}")
        return
    token = login_response.json()["access_token"]
    
    dept_id, pos_id, role_id = get_valid_ids()
    print(f"Using Dept ID: {dept_id}, Pos ID: {pos_id}, Role ID: {role_id}")

    # Prepare onboarding data (Flat Structure)
    data = {
        # Employee Fields
        "first_name": "Jane",
        "last_name": "Doe",
        "email": "jane.doe.flat@example.com",
        "department_id": dept_id, 
        "position_id": pos_id,   
        "date_of_joining": "2024-02-01",
        "employment_type": "Full-time",
        "employment_status": "Active",
        
        # System Access Fields
        "username": "janedoe_flat",
        "password": "password123",
        "role_id": role_id,
        
        # Initial Task Fields
        "task_name": "Complete Profile",
        "task_description": "Fill personal details",
        "task_due_date": "2024-02-05"
    }
    
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/workflows/onboarding", json=data, headers=headers)
    print(f"Onboarding Response: {response.status_code}")
    print(f"Response Body: {response.json()}")

if __name__ == "__main__":
    test_onboarding()
