# 💬 ChitChat - Real-Time Messaging App

![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)

> **"Connect instantly, chat seamlessly."**

**ChitChat** is a modern, high-performance real-time chat application built with the power of **FastAPI** and **React**. Designed for speed and scalability, it leverages **WebSockets** for instant messaging and **MongoDB** for persistent data storage. Whether you're chatting one-on-one or in groups, ChitChat delivers a fluid experience wrapped in a beautiful interface.

---

## 🚀 Key Features

*   **⚡ Real-Time Messaging**: Powered by WebSockets for instant data delivery. No polling required!
*   **🔐 Secure Authentication**: Robust JWT-based authentication for secure login and registration.
*   **👥 Private & Group Chats**: Support for 1-on-1 conversations and multi-user groups.
*   **🎨 AI-Driven UI**: Stunning user interface built with **Tailwind CSS** and **Framer Motion** for smooth animations called "Matcha Zen".
*   **📱 Responsive Design**: Fully responsive layout that looks great on desktop and mobile.
*   **💾 Persistent History**: All conversations are stored safely in MongoDB.

---

## 🛠️ Tech Stack

### **Frontend**
![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)
![Vite](https://img.shields.io/badge/Vite-646CFF?style=for-the-badge&logo=vite&logoColor=white)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)
![Framer Motion](https://img.shields.io/badge/Framer_Motion-0055FF?style=for-the-badge&logo=framer&logoColor=white)

*   **Framework**: React 19 (Vite)
*   **Styling**: Tailwind CSS, clsx, tailwind-merge
*   **Icons**: Lucide React
*   **State/Routing**: React Router DOM
*   **HTTP Client**: Axios

### **Backend**
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-47A248?style=for-the-badge&logo=mongodb&logoColor=white)

*   **Framework**: FastAPI
*   **Database**: MongoDB (Motor Async Driver)
*   **Authentication**: JWT (JSON Web Tokens)
*   **Protocols**: HTTP/2, WebSockets

### **Deployment**
*   **Frontend**: Vercel
*   **Backend**: Render

---

## 📂 Project Structure

```bash
Jan28-DSA-ChatApp/
├── 📂 backend/              # FastAPI Backend
│   ├── 📄 main.py           # Entry point & WebSocket logic
│   ├── 📄 auth.py           # JWT Authentication handlers
│   ├── 📄 database.py       # MongoDB Connection
│   ├── 📄 models.py         # Pydantic Schemas
│   └── 📄 requirements.txt  # Python Dependencies
├── 📂 frontend/             # React Frontend
│   ├── 📂 src/              # Source Code
│   │   ├── 📂 components/   # Reusable UI components
│   │   ├── 📄 App.jsx       # Main App Component
│   │   └── 📄 main.jsx      # DOM Entry
│   ├── 📄 package.json      # Node Dependencies
│   └── 📄 tailwind.config.js# Tailwind Configuration
└── 📄 README.md             # Project Documentation
```

---

## 🏁 Getting Started

Follow these steps to set up the project locally.

### 1. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up Environment Variables
# Create a .env file and add your MongoDB URL:
# MONGODB_URL=mongodb+srv://<user>:<password>@cluster.mongodb.net/?retryWrites=true&w=majority

# Run the server
uvicorn main:app --reload
```
*The backend will start at `http://127.0.0.1:8000`*

### 2. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install Node modules
npm install

# Start the development server
npm run dev
```
*The frontend will start at `http://localhost:5173` (or similar)*

---

## 🔌 API Endpoints

### **Authentication**
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/auth/register` | Register a new user |
| `POST` | `/auth/login` | Login and retrieve JWT token |

### **Chat Operations**
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/users` | List all available users |
| `GET` | `/chat/recent/{id}` | Get recent conversations for a user |
| `POST` | `/chat/start` | Start a new conversation |
| `GET` | `/chat/{id}/messages` | Get message history for a chat |
| `DELETE`| `/chat/{id}` | Delete a conversation |

### **Real-Time**
| Protocol | Endpoint | Description |
| :--- | :--- | :--- |
| `WS` | `/ws/{user_id}` | WebSocket connection for live events |

---

## 📸 WebSocket Events

The application uses specific event types to handle real-time updates:

*   `message`: Client sends a message to the server.
*   `new_message`: Server broadcasts a new message to participants.
*   `new_chat`: Server notifies a user of a new conversation start.

---

## ✨ Authors
*   **Mehtab Singh** - *Developer & Designer*

---
*Built with ❤️ for High-Performance Coding*
