"""
Ushnik Technologies Interactive Chatbot - Main Application
FastAPI backend serving the chat widget, lead capture, and email automation.
"""
import logging
import json
from datetime import datetime
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import Optional

from app.config import settings
from app.chat_engine import get_chat_response
from app.sheets_service import get_course_data, save_lead, get_all_leads, search_courses
from app.email_service import send_welcome_email, send_admin_notification

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Ushnik Technologies Chatbot",
    description="Interactive AI Chatbot for Lead Generation & Customer Support",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
static_dir = Path(__file__).parent.parent / "static"
static_dir.mkdir(exist_ok=True)
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")


# ============== Pydantic Models ==============

class ChatMessage(BaseModel):
    message: str
    conversation_history: Optional[list] = []

class LeadForm(BaseModel):
    name: str
    email: str
    phone: str
    course: Optional[str] = ""
    message: Optional[str] = ""


# ============== API Routes ==============

@app.get("/", response_class=HTMLResponse)
async def serve_home():
    """Serve the main chat widget page."""
    html_path = Path(__file__).parent.parent / "static" / "index.html"
    if html_path.exists():
        return HTMLResponse(content=html_path.read_text(encoding="utf-8"))
    return HTMLResponse(content="<h1>Ushnik Chatbot - Setup Required</h1>")


@app.post("/api/chat")
async def chat_endpoint(msg: ChatMessage):
    """Process a chat message and return AI response."""
    try:
        response = get_chat_response(msg.message, msg.conversation_history or [])
        return JSONResponse(content={
            "status": "success",
            "response": response,
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Chat error: {e}")
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": "Sorry, something went wrong. Please try again."}
        )


@app.post("/api/lead")
async def submit_lead(lead: LeadForm):
    """Submit a lead (contact form) and trigger automations."""
    try:
        lead_data = lead.model_dump()

        # Save lead to Google Sheets / local storage
        save_lead(lead_data)

        # Send welcome email to user
        email_sent = send_welcome_email(
            name=lead.name,
            email=lead.email,
            course=lead.course or "General Inquiry"
        )

        # Send admin notification
        send_admin_notification(lead_data)

        return JSONResponse(content={
            "status": "success",
            "message": "Thank you for registering!",
            "email_sent": email_sent,
            "popup": {
                "title": "🎉 Admissions Are Open!",
                "message": f"Thank you, {lead.name}! You are eligible for 50% OFF on your first course.",
                "cta": "Explore Courses",
                "discount": "50%"
            }
        })
    except Exception as e:
        logger.error(f"Lead submission error: {e}")
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": "Submission failed. Please try again."}
        )


@app.get("/api/courses")
async def get_courses():
    """Get all available courses."""
    try:
        courses = get_course_data()
        return JSONResponse(content={
            "status": "success",
            "courses": courses,
            "count": len(courses)
        })
    except Exception as e:
        logger.error(f"Courses error: {e}")
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": "Failed to load courses."}
        )


@app.get("/api/courses/search")
async def search_courses_endpoint(q: str = ""):
    """Search courses by keyword."""
    try:
        results = search_courses(q)
        return JSONResponse(content={
            "status": "success",
            "courses": results,
            "query": q,
            "count": len(results)
        })
    except Exception as e:
        logger.error(f"Search error: {e}")
        return JSONResponse(status_code=500, content={"status": "error"})


@app.get("/api/leads")
async def get_leads():
    """Get all leads (admin endpoint)."""
    leads = get_all_leads()
    return JSONResponse(content={
        "status": "success",
        "leads": leads,
        "count": len(leads)
    })


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return JSONResponse(content={
        "status": "healthy",
        "service": "Ushnik Chatbot",
        "timestamp": datetime.now().isoformat(),
        "openai_configured": bool(settings.OPENAI_API_KEY and not settings.OPENAI_API_KEY.startswith("sk-your")),
        "email_configured": bool(settings.SMTP_USERNAME and settings.SMTP_PASSWORD and not settings.SMTP_PASSWORD.startswith("your")),
        "sheets_configured": bool(settings.GOOGLE_SHEET_ID and not settings.GOOGLE_SHEET_ID.startswith("your"))
    })


# ============== Run ==============

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True
    )
