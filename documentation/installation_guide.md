# 🛠️ Installation & Setup Guide

This guide will walk you through setting up the **Ushnik AI Chatbot** on your local machine.

---

## 📋 Prerequisites
- **Python 3.12+**
- **Git**
- **Google Account** (for SMTP and Google Sheets)

---

## ⚙️ Step-by-Step Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd agent
```

### 2. Create a Virtual Environment
```bash
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy the `.env.example` file to `.env` and fill in your credentials.
```bash
cp .env.example .env
```

| Variable | Description |
| :--- | :--- |
| `OPENAI_API_KEY` | Your OpenAI API key (for GPT synthesis). |
| `GOOGLE_SHEET_ID` | The ID of your Google Sheet for leads. |
| `SMTP_USERNAME` | Your email address. |
| `SMTP_PASSWORD` | Your 16-character Google App Password. |

### 5. Run the Application
You can use the provided batch file or run directly with Python.
```bash
.\run_app.bat
# OR
uvicorn app.main:app --reload
```

---

## 📧 Email Configuration (Gmail)
To allow the chatbot to send enrollment emails:
1.  Enable **2-Step Verification** in your Google Account.
2.  Search for **"App Passwords"** in your Google Account settings.
3.  Generate a new app password for "Other (Custom name)".
4.  Copy the 16-character code into your `.env` file as `SMTP_PASSWORD`.

---

## 📊 Google Sheets Setup
Ensure you have a service account or an API key configured to write to your `GOOGLE_SHEET_ID`. The sheet should have headers: `Timestamp`, `Name`, `Email`, `Phone`, `Course`, `Message`.
