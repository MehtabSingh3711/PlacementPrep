# Comprehensive Code Walkthrough: 20th Jan.py

This document provides a detailed, line-by-line explanation of the `20th Jan.py` file. It covers everything from basic imports to advanced API logic.

---

## 1. Imports (Lines 1-5)

```python
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google.oauth2 import service_account
from googleapiclient.discovery import build
```

*   **`FastAPI`**: The main class for creating the web API. It handles routing and request processing.
*   **`HTTPException`**: Used to return HTTP error codes (like 404 Not Found) to the client.
*   **`CORSMiddleware`**: Security feature to allow web pages from other domains to access this API.
*   **`BaseModel`**: From Pydantic, used to define the structure and data types of request bodies (data validation).
*   **`service_account`**: Google library to handle authentication using a "Service Account" (a robot account).
*   **`build`**: Function to construct the "service" object that lets us talk to Google APIs (like Sheets).

---

## 2. App Initialization & CORS (Lines 7-15)

```python
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

*   **`app = FastAPI()`**: Creates the application instance. This `app` variable is what the server runs.
*   **`app.add_middleware(...)`**: Configures **CORS (Cross-Origin Resource Sharing)**.
    *   `allow_origins=["*"]`: Allows *any* website to send requests to this API. Important for development but risky in production.
    *   `allow_methods=["*"]`: Allows all HTTP methods (GET, POST, etc.).

---

## 3. Configuration Constants (Lines 17-20)

```python
SERV_ACC = 'SERVICE_ACCOUNT_FILE.json' 
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SPREADSHEET_ID = '1yyugyZnb3bHSODDGQHrNGCB8G0Q9dZLiiid3EyBYlXI'
RANGE_NAME = 'Sheet1!A:D'
```

*   **`SERV_ACC`**: The filename of the JSON key file containing the service account credentials. This acts as the password for the bot.
*   **`SCOPES`**: Permissions requested. Here, we request full access to Google Spreadsheets.
*   **`SPREADSHEET_ID`**: The unique ID found in the URL of your Google Sheet.
*   **`RANGE_NAME`**: Targeted cells. `Sheet1!A:D` means we cover columns A, B, C, and D in "Sheet1".

---

## 4. Google Helper Function (Lines 22-26)

```python
def get_service():
    creds = service_account.Credentials.from_service_account_file(
        SERV_ACC, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=creds)
    return service
```

*   **Purpose**: This function performs authentication every time we need to talk to Google.
*   **`Credentials.from_service_account_file`**: reads the JSON file and prepares to log in.
*   **`build('sheets', 'v4', ...)`**: Connects to the Google Sheets API (version 4) using the verified credentials.

---

## 5. Data Model (Lines 28-31)

```python
class Employee(BaseModel):
    name: str
    department: str
    salary: float
```

*   **Purpose**: Defines what a valid "Employee" looks like.
*   If a user sends data without a `salary` (float), FastAPI will automatically reject it with an error. This ensures data integrity.

---

## 6. POST Endpoint: Create Employee (Lines 33-64)

```python
@app.post("/employee")
def create_employee(employee: Employee):
```
*   **Decorator `@app.post`**: Tells FastAPI to run this function when a POST request hits `/employee`.
*   **`employee: Employee`**: FastAPI reads the JSON body of the request and validates it against our Pydantic model.

### 6.1 Logic Part 1: Reading Existing Data
```python
    service = get_service()
    sheet = service.spreadsheets()
    
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                range=RANGE_NAME).execute()
    values = result.get('values', [])
```
*   Connects to Google Sheets.
*   **`.get(...).execute()`**: Downloads the data from the sheet instantly.
*   **`values`**: A list of lists, where each inner list is a row from the sheet.

### 6.2 Logic Part 2: ID Calculation
```python
    new_id = 1
    if values and len(values) > 1:
        # Complex list comprehension to find current IDs
        try:
             ids = [int(row[0]) for row in values[1:] if row and row[0].isdigit()]
             if ids:
                 new_id = max(ids) + 1
        except Exception:
             pass
```
*   **Goal**: Auto-increment the ID (like SQL Auto-Increment).
*   It looks at all rows starting from the second one (`values[1:]`), assuming the first row is headers.
*   It extracts the first column (`row[0]`), converts to integer, finds the maximum, and adds 1.
*   Includes error handling (`try/except`) to ignore bad data (like empty rows or non-number IDs).

### 6.3 Logic Part 3: Appending Data
```python
    row = [new_id, employee.name, employee.department, employee.salary]
    body = { 'values': [row] }
    
    result = sheet.values().append(
        spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME,
        valueInputOption='USER_ENTERED', body=body).execute()
```
*   **`row`**: Constructs the new row with the calculated ID and user-provided data.
*   **`.append(...)`**: Adds the new row to the bottom of the sheet.
*   **`valueInputOption='USER_ENTERED'`**: Tells Google to treat the data as if a user typed it (e.g., parsing numbers correctly).

---

## 7. GET Endpoint: Get Employee (Lines 66-87)

```python
@app.get("/employee/{name}")
def get_employee(name: str):
```
*   **Path Parameter `{name}`**: Captures part of the URL (e.g., `/employee/Mehtab`) and passes it as the argument `name`.

```python
    # ... (Setup and reading sheet again) ...
    
    if not values:
        raise HTTPException(status_code=404, detail="No data found")
```
*   If the sheet is completely empty, return a 404 error immediately.

```python
    for row in values:
        if len(row) > 1 and row[1].strip().lower() == name.strip().lower():
            return {
                "id": row[0],
                "name": row[1],
                "department": row[2] if len(row) > 2 else None,
                "salary": row[3] if len(row) > 3 else None
            }
```
*   **Search Logic**: Loops through every row in the downloaded data.
    *   **`row[1]`**: Checks the Name column.
    *   **`.strip().lower()`**: Normalizes text (removes spaces, makes lowercase) so "Mehtab" matches "mehtab ".
*   **Return**: If found, constructs a JSON response. It uses safety checks (`if len(row) > 2`) to handle cases where a row might be incomplete (missing salary/dept).

```python
    raise HTTPException(status_code=404, detail="Employee not found")
```
*   If the loop finishes without finding a match, the function raises a 404 error.

---

## 8. Root Endpoint (Lines 89-91)

```python
@app.get("/")
def read_root():
    return {"message": "Employee API is running"}
```
*   A simple endpoint to verifying the server is up and running.
