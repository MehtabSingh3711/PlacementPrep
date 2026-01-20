# Placement Preparation Roadmap

This repository tracks my daily progress and learnings during the placement preparation course.

---

## 📅 20th January 2026: FastAPI & Google Sheets Integration

### 🎓 What was Taught
We learned how to build a backend service using **FastAPI** and connect it to a cloud-based database using **Google Sheets**. The goal was to understand how to:
- Create RESTful API endpoints (GET, POST).
- Authenticate with Google Cloud APIs using Service Accounts.
- Perform CRUD operations on a Google Sheet programmatically.

### 🛠️ Implementation (`20jan.py`)
I built an **Employee Management System** where employee data is stored in a Google Sheet instead of a traditional SQL database.

**Key Components:**
1.  **FastAPI App**: The core web server handling HTTP requests.
2.  **Google Sheets API**: Used to read and write data to the spreadsheet `EmployeeData`.
3.  **Pydantic Models**: Used for data validation (ensuring every employee has a name, department, and salary).

### ⚙️ How It Works

1.  **Setup**:
    - The app initializes with `SERVICE_ACCOUNT_FILE` covering credentials.
    - It connects to the specific Google Sheet ID.

2.  **Adding an Employee (POST `/employee`)**:
    - The user sends JSON data (Name, Dept, Salary).
    - The system reads the current sheet to calculate a new unique ID (max ID + 1).
    - It appends the new row `[ID, Name, Department, Salary]` to the sheet using `sheet.values().append`.

3.  ** retrieving an Employee (GET `/employee/{name}`)**:
    - The user requests an employee by name.
    - The system fetches all rows from the sheet.
    - It iterates through the rows to find a matching name (case-insensitive).
    - Returns the employee details if found, or a 404 error if not.

### 🚀 Usage
```bash
# Start the server
uvicorn 20jan:app --reload

# The API is now available at http://127.0.0.1:8000
# Automatic Docs (Swagger UI): http://127.0.0.1:8000/docs
```
