import os
import requests
from dotenv import load_dotenv

load_dotenv()

HF_TOKEN = os.getenv("HF_API_TOKEN")
MODEL_ID = "google/gemma-1.1-2b-it"

url = "https://router.huggingface.co/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json"
}

print(f"Testing Model: {MODEL_ID}")

payload = {
    "model": MODEL_ID,
    "messages": [{"role": "user", "content": "Hello! who are you?"}],
    "max_tokens": 50
}

try:
    response = requests.post(url, headers=headers, json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response Body: {response.text}")
except Exception as e:
    print(f"Error: {e}")
