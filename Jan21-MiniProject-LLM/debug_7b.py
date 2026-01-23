import os
import requests
from dotenv import load_dotenv

load_dotenv()

HF_TOKEN = os.getenv("HF_API_TOKEN")
url = "https://router.huggingface.co/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json"
}

model_id = "Qwen/Qwen2.5-7B-Instruct" 

print(f"Testing Token: {HF_TOKEN[:4]}...{HF_TOKEN[-4:]}")
print(f"--- Testing Model: {model_id} ---")

payload = {
    "model": model_id,
    "messages": [{"role": "user", "content": "Hello"}],
    "max_tokens": 10
}

try:
    response = requests.post(url, headers=headers, json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response Body: {response.text}")
except Exception as e:
    print(f"Error: {e}")
