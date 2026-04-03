"""
Configuration module for Ushnik Chatbot
Loads environment variables and provides centralized config access.
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    # OpenAI
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")

    # Google Sheets
    GOOGLE_SHEET_ID: str = os.getenv("GOOGLE_SHEET_ID", "")
    GOOGLE_CREDENTIALS_FILE: str = os.getenv("GOOGLE_CREDENTIALS_FILE", "credentials.json")

    # Email / SMTP
    SMTP_HOST: str = os.getenv("SMTP_HOST", "smtp.gmail.com")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USERNAME: str = os.getenv("SMTP_USERNAME", "")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "")
    FROM_EMAIL: str = os.getenv("FROM_EMAIL", "")

    # Company Info
    COMPANY_NAME: str = os.getenv("COMPANY_NAME", "Ushnik Technologies Pvt. Ltd.")
    COMPANY_PHONE: str = os.getenv("COMPANY_PHONE", "+91 7702901217")
    COMPANY_EMAIL: str = os.getenv("COMPANY_EMAIL", "info@ushniktechnologies.com")
    COMPANY_ADDRESS: str = os.getenv(
        "COMPANY_ADDRESS",
        "Flat 107, Gayathri Nest Apartments, Telecom Nagar, Gachibowli, Hyderabad-500032"
    )

    # Server
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))

    # Company Knowledge Base (built-in)
    COMPANY_KNOWLEDGE = {
        "name": "Ushnik Technologies Pvt. Ltd.",
        "tagline": "AI at Work, Innovation in Action",
        "description": "Ushnik Technologies turns complex ideas into powerful products with innovative digital solutions that fuel business growth.",
        "services": {
            "AI & ML": {
                "description": "Harness the power of Generative AI and advanced machine learning.",
                "details": "AI & Data Solutions including NLP, Computer Vision, Predictive Analytics, LLM Integration, and Custom AI Models."
            },
            "Cybersecurity": {
                "description": "Protect your digital assets with cutting-edge security strategies.",
                "details": "Network Security, Penetration Testing, Security Audit, Vulnerability Assessment, and Compliance Management."
            },
            "Web Development": {
                "description": "AI-driven web development accelerates design, enhances user experience.",
                "details": "From design to deployment, we craft seamless, scalable, and responsive web experiences using modern frameworks."
            },
            "Digital Marketing": {
                "description": "AI-powered digital marketing enhances customer engagement for optimized strategies.",
                "details": "SEO, SEM, Social Media Marketing, Content Strategy, and Performance Analytics."
            },
            "Business Consulting": {
                "description": "Strategic business consulting for digital transformation.",
                "details": "IT Strategy, Process Optimization, Digital Transformation, Cloud Migration, and SAP Implementation."
            }
        },
        "industries": [
            "Automotive", "Retail", "Telecom", "Travel", "Insurance",
            "Government", "Healthcare", "Hospitality", "Manufacturing",
            "Media", "Education"
        ],
        "key_features": [
            "On-Time Delivery System",
            "Reliable Customer Support",
            "Innovative Solutions",
            "Quality Assurance",
            "Expert Consultation",
            "Cutting-Edge Technology"
        ],
        "contact": {
            "phone": "+91 7702901217",
            "email": "info@ushniktechnologies.com",
            "address": "Flat 107, Gayathri Nest Apartments, Telecom Nagar, Gachibowli, Hyderabad-500032"
        },
        "stats": {
            "years_experience": "5+",
            "team_members": "15+",
            "projects_completed": "50+"
        }
    }


settings = Settings()
