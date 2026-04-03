
---

## 🏗️ System Architecture

```mermaid
graph TD
    A["🌐 User (Website Visitor)"] --> B["💬 Chat Widget (HTML/CSS/JS)"]
    A --> C["📋 Contact Form"]
    B --> D["⚡ FastAPI Backend"]
    C --> D
    D --> E["🤖 AI Chat Engine"]
    D --> F["📊 Google Sheets Service"]
    D --> G["📧 Email Service"]
    E --> H["🧠 OpenAI GPT"]
    E --> I["📝 Built-in Knowledge Base"]
    F --> J["📋 Course Data Sheet"]
    F --> K["❓ FAQ Sheet"]
    F --> L["👤 Leads Sheet"]
    G --> M["📨 Welcome Email (50% OFF)"]
    G --> N["🔔 Admin Notification"]
    D --> O["🎉 Marketing Popup"]
```

---

## ✨ Features

### 1️⃣ AI Interactive Chatbot
- **Dual-mode AI**: Uses OpenAI GPT when configured, falls back to intelligent keyword-based responses
- Answers questions about courses, services, fees, admissions, contact info
- Markdown-formatted rich responses with emojis
- Conversation history tracking
- Quick reply buttons for common questions

### 2️⃣ Google Sheets Integration
- **Read course data** from Google Sheets in real-time
- **Read FAQ data** from a dedicated FAQ sheet
- **Store leads** automatically to a Leads sheet
- **URL-based loading** – share any Google Sheet URL and the bot can read it
- Falls back to built-in sample data when Sheets is not configured

### 3️⃣ Lead Capture System
- In-chat lead form (appears after 3 messages)
- Full-page contact form with course selection
- Validates name, email, phone before submission
- Auto-saves to Google Sheets + local storage

### 4️⃣ Marketing Popup
After contact form submission:
- 🎉 **Animated popup** with confetti effect
- Shows "Admissions Are Open!" message
- Displays **50% OFF** discount offer
- Customizable title, message, and discount

### 5️⃣ Email Automation
- **Welcome email** sent to user with:
  - Rich HTML template matching company branding
  - 50% discount offer banner
  - Course information
  - Company contact details
- **Admin notification** sent to company with lead details

### 6️⃣ Premium UI/UX
- Dark theme with glassmorphism effects
- Animated gradient orbs in hero section
- Smooth micro-animations throughout
- Responsive design (mobile + desktop)
- Animated stat counters
- Dynamic course card loading

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | HTML5, CSS3, Vanilla JavaScript |
| **Backend** | Python 3.10+, FastAPI |
| **AI Engine** | OpenAI GPT-3.5 (optional) + Built-in NLP |
| **Database** | Google Sheets API + In-memory storage |
| **Email** | SMTP (Gmail / SendGrid compatible) |
| **Fonts** | Google Fonts (Inter, Outfit) |
| **Server** | Uvicorn (ASGI) |

---

## 📁 Project Structure

```
agent/
├── app/
│   ├── __init__.py          # Package init
│   ├── main.py              # FastAPI application & API routes
│   ├── config.py            # Configuration & company knowledge base
│   ├── chat_engine.py       # AI chat response engine
│   ├── sheets_service.py    # Google Sheets integration
│   └── email_service.py     # Email templates & sending
├── static/
│   ├── index.html           # Landing page + chat widget
│   ├── style.css            # Complete design system
│   └── app.js               # Frontend JavaScript
├── .env                     # Environment variables (edit this)
├── .env.example             # Template for .env
├── requirements.txt         # Python dependencies
└── run_app.bat              # One-click run script
```

---

## 🚀 Setup Instructions

### Quick Start (No API keys needed)
The chatbot works out of the box with built-in responses!

```bash
# 1. Run the batch file
double-click run_app.bat

# 2. Open browser
http://localhost:8000
```

### Full Setup (With all features)

#### Step 1: OpenAI API (for AI responses)
1. Get an API key from [platform.openai.com](https://platform.openai.com)
2. Edit [.env](file:///c:/Users/105sn/OneDrive/Desktop/agent/.env):
   ```
   OPENAI_API_KEY=sk-your-actual-key
   ```

#### Step 2: Google Sheets (for data integration)
1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a project → Enable Google Sheets API
3. Create a Service Account → Download `credentials.json`
4. Place `credentials.json` in the project root
5. Create a Google Sheet with tabs: **Courses**, **FAQ**, **Leads**
6. Share the sheet with the service account email
7. Edit [.env](file:///c:/Users/105sn/OneDrive/Desktop/agent/.env):
   ```
   GOOGLE_SHEET_ID=your-sheet-id-from-url
   GOOGLE_CREDENTIALS_FILE=credentials.json
   ```

#### Step 3: Email (for notifications)
1. Use Gmail App Password or SendGrid
2. Edit [.env](file:///c:/Users/105sn/OneDrive/Desktop/agent/.env):
   ```
   SMTP_HOST=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USERNAME=your-email@gmail.com
   SMTP_PASSWORD=your-app-password
   FROM_EMAIL=your-email@gmail.com
   ```

---

## 📡 API Documentation

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Serve the landing page |
| `POST` | `/api/chat` | Send/receive chat messages |
| `POST` | `/api/lead` | Submit contact form → triggers email + popup |
| `GET` | `/api/courses` | Get all available courses |
| `GET` | `/api/courses/search?q=AI` | Search courses by keyword |
| `GET` | `/api/leads` | Get all captured leads (admin) |
| `GET` | `/api/health` | Health check + configuration status |

### Chat API Example
```json
POST /api/chat
{
    "message": "What is the AI course fee?",
    "conversation_history": []
}

Response:
{
    "status": "success",
    "response": "🎓 **AI & Machine Learning**\n\n📅 Duration: 3 months\n💰 Fee: ₹40,000\n🔥 Discount: 50%...",
    "timestamp": "2026-03-11T11:20:48"
}
```

### Lead API Example
```json
POST /api/lead
{
    "name": "Sneha",
    "email": "sneha@gmail.com",
    "phone": "+91 9876543210",
    "course": "AI & Machine Learning",
    "message": "Interested in AI course"
}

Response:
{
    "status": "success",
    "email_sent": true,
    "popup": {
        "title": "🎉 Admissions Are Open!",
        "message": "Thank you, Sneha! You are eligible for 50% OFF...",
        "discount": "50%"
    }
}
```

---

## 📊 Google Sheet Structure

### Courses Tab
| Course | Duration | Fee | Discount | Mode | Description |
|--------|----------|-----|----------|------|-------------|
| AI & Machine Learning | 3 months | ₹40,000 | 50% | Online / Offline | Master GenAI, Deep Learning... |
| Cybersecurity | 2 months | ₹35,000 | 30% | Online / Offline | Ethical Hacking, Pen Testing... |

### FAQ Tab
| question | answer |
|----------|--------|
| What courses do you offer? | We offer AI & ML, Cybersecurity... |
| Do you provide certificates? | Yes! Industry-recognized certificates... |

### Leads Tab (Auto-populated)
| Name | Email | Phone | Course | Message | Source | Timestamp |
|------|-------|-------|--------|---------|--------|-----------|
| Sneha | sneha@gmail.com | 98765 | AI/ML | Interested | chatbot | 2026-03-11 |

---

## 💡 Chat Flow

```mermaid
graph TD
    A["User opens website"] --> B["Chat widget appears with welcome message"]
    B --> C["User asks question"]
    C --> D{"AI processes message"}
    D --> E["Bot responds with rich formatted answer"]
    E --> F{"Message count >= 3?"}
    F -->|Yes| G["Lead form appears in chat"]
    F -->|No| C
    G --> H["User fills Name, Email, Phone, Course"]
    H --> I["Submit"]
    I --> J["Lead saved to Google Sheets"]
    J --> K["Welcome email sent to user"]
    K --> L["Admin notification sent"]
    L --> M["🎉 Marketing popup with confetti!"]
    M --> N["50% OFF displayed"]
```

---

## 🎨 Customization Guide

### Change Company Info
Edit [app/config.py](file:///c:/Users/105sn/OneDrive/Desktop/agent/app/config.py) → `COMPANY_KNOWLEDGE` dictionary

### Change Courses
Edit [app/sheets_service.py](file:///c:/Users/105sn/OneDrive/Desktop/agent/app/sheets_service.py) → `_sample_courses` list

### Change Chat Responses
Edit [app/chat_engine.py](file:///c:/Users/105sn/OneDrive/Desktop/agent/app/chat_engine.py) → `_keyword_response()` function

### Change Popup Message
Edit [app/main.py](file:///c:/Users/105sn/OneDrive/Desktop/agent/app/main.py) → [submit_lead()](file:///c:/Users/105sn/OneDrive/Desktop/agent/app/main.py#93-129) → `popup` object

### Change Colors
Edit [static/style.css](file:///c:/Users/105sn/OneDrive/Desktop/agent/static/style.css) → CSS Variables at `:root`

### Change Email Template
Edit [app/email_service.py](file:///c:/Users/105sn/OneDrive/Desktop/agent/app/email_service.py) → [_build_welcome_email()](file:///c:/Users/105sn/OneDrive/Desktop/agent/app/email_service.py#14-164) function

---

> [!TIP]
> The chatbot works **without any API keys** using the built-in knowledge base! Configure OpenAI, Google Sheets, and SMTP for the full experience.

> [!IMPORTANT]
> **Server URL**: `http://localhost:8000`
> **API Docs**: `http://localhost:8000/docs` (auto-generated Swagger UI)
