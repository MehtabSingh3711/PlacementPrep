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

---

## 📅 21st January 2026: Multi-LLM Chatbot with Gradio

### 🎓 What was Taught
We built a **Context-Aware Chatbot** that can switch between different Large Language Models (LLMs) like **Groq (Llama 3)**, **Gemini**, and **Phi**. The focus was on:
- Building a modular backend to support multiple LLM providers.
- Creating a modern, user-friendly frontend using **Gradio**.
- Managing chat history and context for better conversational flow.

### 🛠️ Implementation (`Jan21-MiniProject-LLM`)
The project consists of a FastAPI backend and a Gradio frontend.

**Key Components:**
1.  **Backend (`backend/main.py`)**:
    - Handles chat requests and routes them to the selected LLM service.
    - Manages session state and context.
2.  **Frontend (`frontend/app.py`)**:
    - Built with **Gradio** for a clean chat interface.
    - Connects to the backend via REST API.
3.  **LLM Services (`backend/services/`)**:
    - Modular integration for varying LLMs.

### 🚀 Usage
**Backend:**
```bash
cd Jan21-MiniProject-LLM/backend
uvicorn main:app --reload --port 8003
```

**Frontend:**
```bash
cd Jan21-MiniProject-LLM/frontend
python app.py
```
Access the chatbot at: `http://127.0.0.1:7860`

---

## 📅 22nd January 2026: LMS Backend (FastAPI & PostgreSQL)

### 🎓 What was Taught
We started building the backend for a comprehensive **Learning Management System (LMS)**. The lesson focused on professional database design and authentication foundations using **PostgreSQL** and **FastAPI**.
- Setting up a **PostgreSQL** database with `sqlalchemy`.
- Defining robust **Pydantic models** and **SQLAlchemy ORM models**.
- Implementing user registration with field validations (Email, Username).

### 🛠️ Implementation (`Jan22-FastAPI-Postgres`)
We implemented the **User Management Module**.

**Key Components:**
1.  **Database Models (`models.py`)**:
    - Defines the `User` table with fields: `id`, `email`, `username`, `password`, `first_name`, `last_name`, `phone_number`.
    - Includes timestamps (`created_at`) and status (`is_active`).
2.  **API Endpoints (`main.py`)**:
    - `POST /users/`: Registers a new user, ensuring email and username uniqueness.
    - `GET /users/{id}`: Retrieves user details.
3.  **Schemas (`schemas.py`)**:
    - Pydantic models for request validation (`UserCreate`) and response formatting (`UserResponse`).

### 🚀 Usage
```bash
cd Jan22-FastAPI-Postgres
uvicorn main:app --reload
```
API Docs: `http://127.0.0.1:8000/docs`

---

## 📅 23rd January 2026: ML Model Deployment with FastAPI

### 🎓 What was Taught
We integrated **Machine Learning** with **FastAPI** to serve predictions via a REST API. We also built a frontend using **Gradio**.
- Training a **Decision Tree Classifier** using `scikit-learn`.
- Creating a **FastAPI** endpoint to serve model predictions.
- Building a **Gradio** interface for interactive testing.

### 🛠️ Implementation (`Jan23-ML-FastAPI`)
We built an **Exoplanet Habitability Classifier**.

**Key Components:**
1.  **Model Training (`model_training.ipynb`)**:
    - Trained a `DecisionTreeClassifier` on an Exoplanet dataset.
    - Features: Distance (AU), Temperature (K), Pressure (atm), Water (%), Oxygen (%).
2.  **API Service (`model-api.py`)**:
    - `POST /predict`: Accepts exoplanet features and returns `"habitable"` or `"uninhabitable"`.
3.  **Frontend (`model_training.ipynb`)**:
    - A **Gradio** interface embedded in the notebook allows users to input features and see predictions instantly.

### 🚀 Usage
**Run the API:**
```bash
cd Jan23-ML-FastAPI
uvicorn model-api:app --reload
```
API Docs: `http://127.0.0.1:8000/docs`
