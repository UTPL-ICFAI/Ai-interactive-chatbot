# 📄 Ushnik Technologies: AI Chatbot - Master Documentation

---

## 🏗️ 1. System Overview & Architecture

The **Ushnik AI Chatbot** is a professional-grade, decoupled full-stack application designed for lead generation and automated customer support.

### A. The Request Lifecycle
1.  **Client Entry**: The user interacts with the **Modern Glassmorphism UI** (`static/style.css`).
2.  **State Management**: `app.js` handles the frontend state—tracking message counts for lead prompts.
3.  **API Gateway**: `main.py` (FastAPI) receives the JSON payload over a persistent HTTP/1.1 connection.
4.  **AI Orchestrator**: `chat_engine.py` runs the intent analysis. It searches the **Knowledge Repository** (`knowledge_base.py`) before synthesizing a GPT-like response.
5.  **Persistence Layer**: Lead data is simultaneously dispatched to two locations:
    -   **Google Sheets API** (via `sheets_service.py`) for the live student database.
    -   **Local Server Memory** as a high-availability fallback.
6.  **Automation Trigger**: The `email_service` builds a dual-part MIME message (`text/plain` and `text/html`) and delivers it using TLS encryption to the student and admin.

---

## 🛠️ 2. Comprehensive Tech Stack

| Component | Technology | Role |
| :--- | :--- | :--- |
| **Backend Core** | **Python 3.12+** | Logic, data processing, and automation. |
| **API Framework** | **FastAPI** | High-performance, asynchronous web server. |
| **AI Strategy** | **Hybrid / Intent-Based** | Pattern-matching engine with a GPT synthesis layer. |
| **Database (LIVE)** | **Google Sheets API** | Real-time cloud storage for student leads. |
| **Email Relay** | **SMTP (STARTTLS)** | Secure delivery of enrollment confirmations. |
| **Design System** | **Glassmorphism / CSS3** | Premium UI using variables and @keyframes. |
| **Scripting** | **Vanilla ES6 JS** | Frontend interactivity and DOM manipulation. |
| **Typography** | **Google Fonts (Outfit/Inter)** | Premium brand fonts. |

---

## 📁 3. Detailed Project Structure

-   `/app`: The engine of the application.
    -   `main.py`: The entry point. Defines `/api/chat` and `/api/lead` endpoints.
    -   `chat_engine.py`: The "Brain". Detects user intents and crafts professional replies.
    -   `knowledge_base.py`: The source of truth for company services, courses, and FAQs.
    -   `email_service.py`: Handles all SMTP communications.
    -   `sheets_service.py`: Manages OAuth2 credentials and writing to the Google Sheets API.
    -   `config.py`: Centralized environment manager (loads `.env`).
-   `/static`: The face of the application.
    -   `index.html`: Optimized HTML5 structure for accessibility and SEO.
    -   `style.css`: The "Ushnik Design Language" system.
    -   `app.js`: Connects the UI to the backend APIs.
-   `.env`: Secret store (SMTP keys, Spreadsheet IDs, API keys).
-   `requirements.txt`: Master list of Python dependencies.

<div style="page-break-after: always;"></div>

## 🚀 4. API Reference Guide

### 💬 Chat Endpoint
**Endpoint:** `/api/chat`  
**Method:** `POST`

**Request Body:**
```json
{
  "message": "Tell me about your courses.",
  "conversation_history": []
}
```

### 📈 Lead Submission
**Endpoint:** `/api/lead`  
**Method:** `POST`

**Request Body:**
```json
{
  "name": "Jane Smith",
  "email": "jane@example.com",
  "phone": "9988776655",
  "course": "AI & ML",
  "message": "When is the next intake?"
}
```

<div style="page-break-after: always;"></div>

## ⚙️ 5. Installation & Setup

### 📋 Prerequisites
- Python 3.12+
- Google App Password (for SMTP)

### 🚀 Setup Steps
1. **Virtual Env**: `python -m venv venv`
2. **Activate**: `.\venv\Scripts\activate`
3. **Install**: `pip install -r requirements.txt`
4. **Environment**: Update `.env` with your API keys and credentials.
5. **Run**: `run_app.bat`

---

## 📘 6. Operational Guide

### 📝 Updating Data
You can modify the chatbot's knowledge without touching the code by updating the Python lists in `app/knowledge_base.py`.

### 🛡️ Security Protocol
- **XSS Protection**: All user messages are sanitized using HTML escaping.
- **Error Handling**: Form validation ignores non-numeric characters in phone fields.

---
*Document Version: 2.1.0*
*Last Updated: 2026-03-13*
*Built for: Ushnik Technologies*
