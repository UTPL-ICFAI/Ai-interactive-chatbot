# 🤖 Ushnik Technologies AI Chatbot

A premium, professional-grade AI assistant designed for **Ushnik Technologies**. This chatbot manages student inquiries, provides dynamic information about courses and services, and automates lead generation with instant email fulfillment.

---

## 🚀 Key Features

### 💎 Premium Experience
- **SaaS-Inspired UI**: Sleek, modern interface using **Outfit** and **Inter** fonts.
- **Responsive Design**: Fully optimized for mobile and desktop browsers.
- **Micro-Animations**: Fluid message entry and interactive component transitions.

### 🧠 Intelligent Conversational Flow
- **AI-Powered Engine**: Uses a hybrid logic of intent detection and contextual search.
- **Dynamic Reponses**: Simulates GPT-like behavior with varied greetings and contextual synthesization.
- **Smart Knowledge Base**: Pre-loaded with comprehensive data on Ushnik's services, courses, and company stats.

### 📊 Lead Generation & Automation
- **Mandatory Lead Form**: High-conversion form captures student details after information is delivered.
- **Google Sheets Integration**: Automatically logs every student inquiry into a central Google Sheet.
- **Instant Email Automation**: Sends a professional HTML welcome/marketing email to students immediately upon registration.
- **Admin Notifications**: Notifies you instantly via email whenever a new lead is captured.

---

## 🛠️ Technology Stack
- **Backend**: Python 3.12+ / FastAPI (High-performance API)
- **Frontend**: Vanilla JS / CSS3 (no heavy frameworks for instant loading)
- **Integration**: Google Sheets API
- **Automation**: SMTP (Gmail)

---

## ⚙️ Configuration & Setup

### 1. Environment Variables (`.env`)
Create/edit the `.env` file in the root directory with the following:
```env
# AI
OPENAI_API_KEY=your_openai_key_here

# Google Sheets
GOOGLE_SHEET_ID=your_sheet_id_here
GOOGLE_CREDENTIALS_FILE=credentials.json

# Email (SMTP)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password_here
FROM_EMAIL=your_email@gmail.com

# Company Info
COMPANY_NAME=Ushnik Technologies Pvt. Ltd.
COMPANY_PHONE=+91 7702901217
```

### 2. Google Sheets Setup
- Place your `credentials.json` file in the root directory.
- Create a Google Sheet and copy its ID into the `.env` file.
- The app will automatically create a "Leads" tab if it doesn't exist.

### 3. Running the Application
Simply run the included batch file:
```bash
./run_app.bat
```
The app will be available at `http://localhost:8000`.

---

## 📁 Project Structure
- **/app**: Core Python logic
    - `main.py`: API Endpoints (FastAPI)
    - `chat_engine.py`: AI Response Logic
    - `email_service.py`: Automated Emailing
    - `sheets_service.py`: Google Sheets Integration
    - `knowledge_base.py`: Company Data Repository
    - `config.py`: Environment Loader
- **/static**: Frontend assets
    - `index.html`: Main Chat Interface
    - `style.css`: Premium Design System
    - `app.js`: Frontend Logic & API Handling

---

## 📧 Email Automation Info
The system uses **Gmail SMTP**. To enable this:
1. Enable **2-Step Verification** on your Gmail account.
2. Generate an **App Password** at [Google Security](https://myaccount.google.com/apppasswords).
3. Use that 16-character code in your `.env` file.

---

## 📚 Documentation

Detailed documentation is available in the [documentation](./documentation/) folder:
- [System Architecture](./documentation/system_overview.md)
- [API Reference](./documentation/api_guide.md)
- [Installation Guide](./documentation/installation_guide.md)
- [User Manual](./documentation/user_guide.md)

---
*Developed for Ushnik Technologies – AI at Work, Innovation in Action.*
