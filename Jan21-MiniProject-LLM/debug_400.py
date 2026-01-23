import os
import requests
from dotenv import load_dotenv

load_dotenv()

HF_TOKEN = os.getenv("HF_API_TOKEN")
# Ensure we are testing the model currently in .env
MODEL_ID = os.getenv("HF_MODEL_ID")

url = "https://router.huggingface.co/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json"
}

print(f"Testing Model: {MODEL_ID}")
print(f"Token: {HF_TOKEN[:4]}...")

# Minimal Payload
payload = {
    "model": MODEL_ID,
    "messages": [{"role": "user", "content": "Hi"}],
    "max_tokens": 10
}

try:
    print("Sending request...")
    response = requests.post(url, headers=headers, json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response Body: {response.text}")
except Exception as e:
    print(f"Error: {e}")
