import requests
from backend.config import GROQ_API_KEY, GROQ_MODEL_ID
import logging

logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self):
        # Groq OpenAI-compatible endpoint
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }

    def generate_response(self, prompt: str, history: list = None) -> str:
        messages = []
        
        # Add system prompt
        messages.append({
            "role": "system",
            "content": "You are a helpful, polite, and concise general conversational assistant. Maintain continuity using prior conversation context."
        })

        # Add history
        if history:
            for msg in history:
                role = msg.get("Role") or msg.get("role")
                content = msg.get("Message") or msg.get("content")
                # Normalize roles
                if role == "bot":
                    role = "assistant"
                messages.append({"role": role, "content": content})
        
        # Add current user prompt
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": GROQ_MODEL_ID,
            "messages": messages,
            "max_tokens": 512,
            "temperature": 0.7,
            "top_p": 0.95,
            "stream": False
        }

        try:
            response = requests.post(self.api_url, headers=self.headers, json=payload)
            response.raise_for_status()
            result = response.json()
            
            # Parse OpenAI-format response
            if "choices" in result and len(result["choices"]) > 0:
                return result["choices"][0]["message"]["content"]
            else:
                return "No response generated."

        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP Error calling Groq API: {e}")
            if e.response.status_code == 401:
                return "Error: Invalid Groq API Key."
            return f"Error: {e}"
        except Exception as e:
            logger.error(f"Error calling Groq API: {e}")
            return "An unexpected error occurred."

llm_service = LLMService()
