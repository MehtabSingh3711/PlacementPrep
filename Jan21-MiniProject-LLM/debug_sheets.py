import traceback
from backend.services.sheets_service import sheets_service
import uuid

session_id = f"debug_{str(uuid.uuid4())[:8]}"
print(f"Testing with Session ID: {session_id}")

try:
    print("1. Creating Sheet...")
    sheets_service.create_session_sheet(session_id)
    print("   Created/Found.")
    
    print("2. Appending Message...")
    sheets_service.append_message(session_id, "user", "Hello World")
    print("   Appended.")

    print("3. Fetching History...")
    history = sheets_service.get_history(session_id)
    print(f"   History: {history}")

except Exception:
    print("!!! ERROR OCCURRED !!!")
    traceback.print_exc()
