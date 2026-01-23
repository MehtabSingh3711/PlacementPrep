# Product Requirements Document (PRD)

## Context-Aware General Conversational Chatbot with Persistent Memory

**Document Version:** 1.0  
**Date:** January 21, 2026  
**Document Owner:** Senior Product Manager & System Architect  
**Status:** Draft for Review

---

## 1. Executive Summary

This document specifies the requirements for a context-aware general conversational chatbot system that maintains persistent memory across sessions using Google Sheets as an external storage mechanism. The system leverages open-source Large Language Models (LLMs) via the Hugging Face Inference API, implements a Java-based desktop frontend using JavaFX, and utilizes a Python backend for orchestration. The architecture is designed for academic evaluation with emphasis on simplicity, explainability, and minimal resource consumption.

---

## 2. Problem Statement

### 2.1 Background

Modern conversational AI systems require the ability to maintain context across multiple interactions to provide coherent, relevant, and personalized responses. However, implementing such systems often involves complex infrastructure, proprietary APIs, and significant computational resources. Educational and research environments require accessible, transparent, and cost-effective solutions that demonstrate fundamental concepts of context-aware conversational AI without the overhead of enterprise-grade infrastructure.

### 2.2 Problem Definition

There exists a gap in available reference implementations for:
- Context-aware conversational systems using open-source LLMs
- Persistent memory management using accessible cloud storage (Google Sheets)
- Multi-user session isolation without database infrastructure
- Desktop-based conversational interfaces suitable for academic demonstration

### 2.3 Current Limitations

Existing solutions present the following challenges:
- Stateless chatbot implementations lack conversational continuity
- Local model inference requires significant computational resources
- Database-backed solutions introduce unnecessary complexity
- Web-based interfaces may not suit controlled academic environments

---

## 3. Goals and Non-Goals

### 3.1 Goals

**Primary Goals**
1. Deliver a functional context-aware conversational chatbot
2. Implement persistent memory using Google Sheets
3. Ensure session isolation for multiple users
4. Maintain low CPU and memory usage
5. Provide a clean, explainable architecture

**Secondary Goals**
1. Demonstrate best practices in API integration
2. Implement graceful error handling
3. Enable future extensibility

### 3.2 Non-Goals

Out of scope:
- Local model inference or fine-tuning
- Authentication systems
- Multimodal interaction
- Mobile or web interfaces
- Paid APIs
- Production-grade scalability

---

## 4. User Personas

### 4.1 Academic Researcher
- Needs architectural clarity and inspectable memory
- Goal: Analyze conversational context handling

### 4.2 Undergraduate Student
- Needs intuitive UI and readable code
- Goal: Learn AI system integration

### 4.3 Course Instructor
- Needs reliability and multi-user support
- Goal: Classroom demonstration

---

## 5. User Flow

### 5.1 First-Time User Flow

1. User launches JavaFX application  
2. User sends first message  
3. Backend generates Session ID  
4. New Google Sheet tab created  
5. Prompt sent to Hugging Face API  
6. Response stored and displayed  

### 5.2 Returning User Flow

1. User sends message with Session ID  
2. Backend fetches last N messages  
3. Context-aware prompt constructed  
4. Response generated and stored  

### 5.3 Session Restoration

- Session ID loaded locally
- Chat history optionally restored

---

## 6. System Architecture

### 6.1 Architecture Overview

- **Frontend:** JavaFX Desktop Application
- **Backend:** Python FastAPI Server
- **LLM:** Hugging Face Inference API
- **Memory:** Google Sheets (one sheet per session)

### 6.2 Key Components

#### JavaFX Frontend
- Chat UI
- Session storage
- API communication

#### FastAPI Backend
- Session management
- Prompt building
- API orchestration

#### Google Sheets Memory
- Sheet per session
- Append-only message log

---

## 7. Functional Requirements

### 7.1 Session Management
- UUID-based Session IDs
- Session persistence
- Isolation across users

### 7.2 Conversation Management
- Message input & display
- Context window (default: 10 messages)
- Immediate persistence

### 7.3 LLM Integration
- Hugging Face Inference API
- Configurable model
- Timeout & retry handling

### 7.4 Google Sheets Integration
- Single spreadsheet
- New tab per session
- Schema: Timestamp | Role | Message

### 7.5 Error Handling
- Network failures
- API errors
- Validation errors

---

## 8. Non-Functional Requirements

### Performance
- Median response < 6 seconds
- Low CPU usage on client

### Reliability
- Persistent storage before response
- Automatic recovery from transient failures

### Usability
- Clear UI feedback
- Minimal setup time

### Security
- API keys via environment variables
- Session isolation

### Maintainability
- Modular code
- Externalized configuration
- Structured logging

---

## 9. Data Model

### Spreadsheet Structure
- One spreadsheet
- One sheet per session

### Sheet Schema

| Column | Name | Description |
|------|------|-------------|
| A | Timestamp | ISO 8601 |
| B | Role | User / Bot |
| C | Message | UTF-8 text |

---

## 10. API Specification

### POST /chat

**Request**
```json
{
  "session_id": "optional",
  "message": "Hello"
}
Response

{
  "session_id": "uuid",
  "response": "Hello! How can I help?"
}

### GET /history/{session_id}

Returns recent messages for a session.

### 11. Prompt Design Strategy
System Instruction
You are a helpful, polite, and concise general conversational assistant.
Maintain continuity using prior conversation context.

Prompt Structure

System instruction

Conversation history

Current user message

### 12. Assumptions & Constraints
Assumptions

Stable internet access

Valid API credentials

Constraints

External API rate limits

Google Sheets storage limits

### 13. Risks & Mitigation
Risk	Mitigation
API latency	Loading indicators
Rate limits	Retry & backoff
Long chats	Context truncation
### 14. Future Enhancements

Database-backed memory

Chat summarization

Streaming responses

Multiple conversations per user

Export chat history

### 15. Success Metrics

Correct context usage

Zero cross-session leakage

Reliable persistence

Smooth demo experience

### 16. Conclusion

This PRD defines a minimal, explainable, and academically strong context-aware chatbot system. The design demonstrates practical AI system architecture while remaining lightweight, transparent, and suitable for educational evaluation.

### 17. Appendix
Configuration Variables
HF_API_TOKEN
HF_MODEL_ID
GOOGLE_SHEETS_ID
GOOGLE_CREDENTIALS_PATH
CONTEXT_WINDOW_SIZE
BACKEND_URL

### 18. Abbreviations

LLM – Large Language Model

API – Application Programming Interface

PRD – Product Requirements Document

---

**End of Document**