from fastapi import FastAPI, HTTPException
from backend.models.schemas import ChatRequest, ChatResponse, HistoryResponse, Message
from backend.services.sheets_service import sheets_service
from backend.services.llm_service import llm_service

import uuid
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Context-Aware Chatbot Backend")

@app.get("/")
async def root():
    return {"message": "Chatbot Backend is running"}

@app.get("/health")
async def health():
    return {
        "status": "running",
        "sheets_connected": not sheets_service.mock_mode,
        "spreadsheet_id": sheets_service.spreadsheet_id,
        "active_sessions_in_memory": len(sheets_service._memory)
    }

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        session_id = request.session_id
        if not session_id:
            session_id = str(uuid.uuid4())
        
        # Ensure sheet exists for the session (idempotent check inside service)
        sheets_service.create_session_sheet(session_id)
        
        user_message = request.message
        
        # 1. Fetch history for context (keep it simple: last 10 messages)
        full_history = sheets_service.get_history(session_id)
        logger.info(f"Fetched {len(full_history)} messages of context for session {session_id}")
        logger.info(f"Context Sample: {full_history[-2:] if full_history else 'Empty'}")
        
        # 2. Generate response
        bot_response_text = llm_service.generate_response(user_message, history=full_history)
        
        # 3. Persist messages logic
        # Ideally, we append user message then bot message. 
        # But for strictly correct history in Sheets, we should append user msg first.
        sheets_service.append_message(session_id, "user", user_message)
        sheets_service.append_message(session_id, "bot", bot_response_text)
        
        return ChatResponse(session_id=session_id, response=bot_response_text)

    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        # If it's a validation error, it might be hidden, let's log the raw body if accessible (hard in fastapi exception handler directly, but let's improve logging)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/history/{session_id}", response_model=HistoryResponse)
async def get_history(session_id: str):
    try:
        raw_history = sheets_service.get_history(session_id)
        formatted_history = []
        for row in raw_history:
            # Gspread returns dicts with keys matching header
            formatted_history.append(Message(
                role=row.get("Role", "unknown"), 
                content=row.get("Message", ""),
                timestamp=str(row.get("Timestamp", ""))
            ))
        return HistoryResponse(session_id=session_id, history=formatted_history)
    except Exception as e:
        logger.error(f"Error fetching history: {e}")
        # Return empty if fails to be safe
        return HistoryResponse(session_id=session_id, history=[])
