# 🚀 Ushnik Chatbot API Documentation

Welcome to the API documentation for the **Ushnik AI Chatbot**. This system provides robust endpoints for real-time chat, lead capture, and course management.

---

## 🛠️ Base URL
All API requests should be made to:
`http://localhost:8000/api`

---

## 💬 1. Chat Endpoint
**Endpoint:** `/chat`  
**Method:** `POST`  
**Description:** Send a message to the AI and receive a context-aware response.

### Request Body
```json
{
  "message": "Hello, tell me about your courses.",
  "conversation_history": [
    {"role": "user", "content": "Hi"},
    {"role": "assistant", "content": "Hello! How can I help you today?"}
  ]
}
```

### Success Response
```json
{
  "status": "success",
  "response": "We offer several premium courses, including Full Stack Development and AI/ML...",
  "timestamp": "2026-03-13T09:40:00Z"
}
```

---

## 📈 2. Lead Submission
**Endpoint:** `/lead`  
**Method:** `POST`  
**Description:** Captures student enrollment details and triggers automated welcome emails.

### Request Body
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "9876543210",
  "course": "Full Stack Development",
  "message": "Interested in the next batch."
}
```

### Success Response
```json
{
  "status": "success",
  "message": "Thank you for registering!",
  "email_sent": true,
  "popup": {
    "title": "🎉 Admissions Are Open!",
    "message": "Thank you, John Doe! You are eligible for 50% OFF.",
    "cta": "Explore Courses",
    "discount": "50%"
  }
}
```

---

## 📚 3. Course Management
### Get All Courses
**Endpoint:** `/courses`  
**Method:** `GET`

### Search Courses
**Endpoint:** `/courses/search`  
**Method:** `GET`  
**Parameters:** `q` (query string)

---

## 🏥 4. Health Check
**Endpoint:** `/health`  
**Method:** `GET`  
**Description:** Check the status of the system and external service configurations (OpenAI, SMTP, Sheets).
