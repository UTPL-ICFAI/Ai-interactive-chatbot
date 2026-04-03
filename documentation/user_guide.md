# 📘 User Manual & Operational Guide

This guide describes how to operate the **Ushnik AI Chatbot** once it is running.

---

## 💬 Interacting with the Chatbot
The chatbot is visible in the bottom-right corner of the web application.

### Key Features:
1.  **Intent Discovery**: Ask about courses like "HTML", "Python", or "Graphic Design".
2.  **Lead Capture**: After 3-5 messages, the chatbot will automatically prompt you for your contact details.
3.  **Real-time Assistance**: Get instant answers to FAQs about admission, fees, and syllabus.

---

## 📈 Managing Lead Data
All enrollment submissions are tracked in two places:

### 1. Google Sheets (Primary)
Check your configured Spreadsheet ID for new rows.
-   **Headers**: Name, Email, Phone, Course, Message.
-   **Updates**: Leads appear in the sheet within seconds of submission.

### 2. Admin Interface
You can view leads by visiting the `/api/leads` endpoint directly in your browser or through a custom admin dashboard.

---

## 📝 Updating Chatbot Knowledge
To change the chatbot's responses or add new courses:
1.  Open `app/knowledge_base.py`.
2.  Modify the `COURSES` or `FAQS` lists.
3.  Save the file. The changes are applied instantly if `uvicorn` is in reload mode.

---

## 🆘 Troubleshooting
-   **Chat not responding**: Check the log console for API errors. Ensure your `OPENAI_API_KEY` is valid.
-   **Emails not sending**: Verify `SMTP_PASSWORD` is a 16-character App Password, not your regular Gmail password.
-   **Leads not in Sheets**: Check if the Spreadsheet ID is correct and shared with the appropriate service account.
