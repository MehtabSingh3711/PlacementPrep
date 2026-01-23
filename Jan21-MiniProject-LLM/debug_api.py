import requests
import uuid
import time

BASE_URL = "http://127.0.0.1:8003"
CHAT_URL = f"{BASE_URL}/chat"
HISTORY_URL_XY = f"{BASE_URL}/history"

print("--- Starting Context Awareness Test ---")

# Step 1: Send first message
payload1 = {"message": "My name is Antigravity."}
print(f"\n1. Sending: {payload1['message']}")
try:
    resp1 = requests.post(CHAT_URL, json=payload1)
    resp1.raise_for_status()
    data1 = resp1.json()
    session_id = data1["session_id"]
    reply1 = data1["response"]
    print(f"   Received Session ID: {session_id}")
    print(f"   Bot Reply: {reply1}")
except Exception as e:
    print(f"   !!! Error in Step 1: {e}")
    exit(1)

# Step 2: Send second message with session_id
payload2 = {
    "session_id": session_id,
    "message": "What is my name?"
}
print(f"\n2. Sending: {payload2['message']} (with session_id)")
try:
    resp2 = requests.post(CHAT_URL, json=payload2)
    resp2.raise_for_status()
    data2 = resp2.json()
    reply2 = data2["response"]
    print(f"   Bot Reply: {reply2}")
    
    if "Antigravity" in reply2:
        print("   SUCCESS! Context was maintained.")
    else:
        print("   FAILURE! Context was lost.")
except Exception as e:
    print(f"   !!! Error in Step 2: {e}")

# Step 3: Check History Endpoint
print(f"\n3. Checking History for Session {session_id}")
try:
    hist_url = f"{HISTORY_URL_XY}/{session_id}"
    resp3 = requests.get(hist_url)
    resp3.raise_for_status()
    history_data = resp3.json()
    print(f"   History Items: {len(history_data.get('history', []))}")
    for msg in history_data.get('history', []):
        print(f"   - [{msg['role']}]: {msg['content']}")
except Exception as e:
    print(f"   !!! Error fetching history: {e}")
