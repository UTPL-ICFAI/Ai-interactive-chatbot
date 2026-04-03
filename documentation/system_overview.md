# 📘 Ushnik Technologies: AI Chatbot (The Professional Edition)

This document contains the complete technical architecture and operational guide for the **Ushnik AI Chatbot**. It is designed to be a standalone reference for any developer or stakeholder.

---

## 🏗️ 1. Technical Architecture & System Flow

The system is built as a **Decoupled Full-Stack Application** with a focus on real-time asynchronous processing.

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

---

## 🚨 4. Operational Maintenance

### 📝 Updating Data
You can modify the chatbot's knowledge without touching the code.
-   **Method 1 (Dynamic)**: Update your Google Sheet spreadsheet. The app caches data but fetches fresh info every 5 minutes.
-   **Method 2 (Static)**: Modify the Python lists in `app/knowledge_base.py`.

### 📧 Automated Emails
The system is built to send emails from **`kolanusnehareddie@gmail.com`**.
-   **Requirement**: Google 2-Step Verification must be enabled.
-   **Configuration**: The 16-character **App Password** must be kept updated in the `.env` file under `SMTP_PASSWORD`.

### 🛡️ Security Protocol
-   **XSS Protection**: All user messages are sanitized using HTML escaping.
-   **Error Handling**: Form validation ignores non-numeric characters in phone fields and enforces valid email addresses before processing.

---
*Document Version: 2.1.0*
*Last Updated: 2026-03-11*
*Built for: Ushnik Technologies*
