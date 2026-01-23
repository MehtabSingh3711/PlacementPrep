import os
import requests
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_ID = os.getenv("GROQ_MODEL_ID", "llama3-8b-8192")

url = "https://api.groq.com/openai/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}

print(f"Testing Model: {MODEL_ID}")
print(f"Key: {GROQ_API_KEY[:4]}...{GROQ_API_KEY[-4:]}" if GROQ_API_KEY else "Key: None")

payload = {
    "model": MODEL_ID,
    "messages": [
        {
            "role": "system",
            "content": "You are a helpful, polite, and concise general conversational assistant. Maintain continuity using prior conversation context."
        },
        {"role": "user", "content": "Hello"}
    ],
    "max_tokens": 512,
    "temperature": 0.7,
    "top_p": 0.95,
    "stream": False
}

try:
    print("Sending request...")
    response = requests.post(url, headers=headers, json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response Body: {response.text}")
except Exception as e:
    print(f"Error: {e}")
