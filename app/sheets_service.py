"""
Google Sheets Service
Handles reading course/FAQ data from Google Sheets and writing leads to sheets.
"""
import json
import os
import logging
from typing import Optional
from datetime import datetime

logger = logging.getLogger(__name__)

# In-memory lead storage (fallback when Google Sheets is not configured)
_local_leads = []

from app.knowledge_base import COURSES as _sample_courses
from app.knowledge_base import FAQS as _sample_faqs

# Cached sheet data
_sheet_data_cache = None
_sheet_cache_time = None
CACHE_DURATION = 300  # 5 minutes


def _try_load_google_sheets():
    """Try to connect to Google Sheets and read data."""
    try:
        import gspread
        from google.oauth2.service_account import Credentials
        from app.config import settings

        if not settings.GOOGLE_SHEET_ID or not os.path.exists(settings.GOOGLE_CREDENTIALS_FILE):
            return None

        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
        creds = Credentials.from_service_account_file(
            settings.GOOGLE_CREDENTIALS_FILE, scopes=scopes
        )
        client = gspread.authorize(creds)
        sheet = client.open_by_key(settings.GOOGLE_SHEET_ID)
        return sheet
    except Exception as e:
        logger.warning(f"Google Sheets not available: {e}")
        return None


def get_course_data() -> list[dict]:
    """
    Get course data from Google Sheets or return sample data.
    Tries Google Sheets first, falls back to built-in sample data.
    """
    global _sheet_data_cache, _sheet_cache_time

    # Check cache
    if _sheet_data_cache and _sheet_cache_time:
        elapsed = (datetime.now() - _sheet_cache_time).total_seconds()
        if elapsed < CACHE_DURATION:
            return _sheet_data_cache

    # Try Google Sheets
    sheet = _try_load_google_sheets()
    if sheet:
        try:
            worksheet = sheet.worksheet("Courses")
            records = worksheet.get_all_records()
            if records:
                _sheet_data_cache = records
                _sheet_cache_time = datetime.now()
                return records
        except Exception as e:
            logger.warning(f"Error reading courses from Google Sheets: {e}")

    # Fallback to sample data
    return _sample_courses


def get_faq_data() -> list[dict]:
    """Get FAQ data from Google Sheets or return built-in FAQs."""
    sheet = _try_load_google_sheets()
    if sheet:
        try:
            worksheet = sheet.worksheet("FAQ")
            records = worksheet.get_all_records()
            if records:
                return records
        except Exception as e:
            logger.warning(f"Error reading FAQ from Google Sheets: {e}")

    # Fallback to centralized FAQs
    return _sample_faqs


def save_lead(lead_data: dict) -> bool:
    """
    Save a lead to Google Sheets and/or local storage.
    Returns True on success.
    """
    lead_data["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Always save locally
    _local_leads.append(lead_data)

    # Try Google Sheets
    sheet = _try_load_google_sheets()
    if sheet:
        try:
            try:
                worksheet = sheet.worksheet("Leads")
            except Exception:
                worksheet = sheet.add_worksheet(title="Leads", rows=1000, cols=10)
                worksheet.append_row(["Name", "Email", "Phone", "Course", "Message", "Source", "Timestamp"])

            worksheet.append_row([
                lead_data.get("name", ""),
                lead_data.get("email", ""),
                lead_data.get("phone", ""),
                lead_data.get("course", ""),
                lead_data.get("message", ""),
                lead_data.get("source", "chatbot"),
                lead_data.get("timestamp", ""),
            ])
            logger.info(f"Lead saved to Google Sheets: {lead_data.get('email')}")
            return True
        except Exception as e:
            logger.warning(f"Error saving lead to Google Sheets: {e}")

    # Try to save to a local CSV file for persistence
    try:
        import csv
        file_path = "leads.csv"
        file_exists = os.path.isfile(file_path)
        with open(file_path, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=["name", "email", "phone", "course", "message", "source", "timestamp"])
            if not file_exists:
                writer.writeheader()
            writer.writerow({
                "name": lead_data.get("name", ""),
                "email": lead_data.get("email", ""),
                "phone": lead_data.get("phone", ""),
                "course": lead_data.get("course", ""),
                "message": lead_data.get("message", ""),
                "source": lead_data.get("source", "chatbot"),
                "timestamp": lead_data.get("timestamp", ""),
            })
    except Exception as e:
        logger.warning(f"Could not save lead to CSV: {e}")

    logger.info(f"Lead saved locally: {lead_data.get('email')}")
    return True


def get_all_leads() -> list[dict]:
    """Get all stored leads."""
    return _local_leads


def search_courses(query: str) -> list[dict]:
    """Search courses matching a query string."""
    courses = get_course_data()
    query_lower = query.lower()
    results = []

    for course in courses:
        course_str = " ".join(str(v).lower() for v in course.values())
        if query_lower in course_str:
            results.append(course)

    return results if results else courses  # Return all if no match found


def load_sheet_from_url(sheet_url: str) -> Optional[list[dict]]:
    """
    Load data from a Google Sheet URL.
    Extracts the sheet ID from the URL and reads the data.
    """
    try:
        import re
        # Extract sheet ID from URL
        match = re.search(r'/spreadsheets/d/([a-zA-Z0-9-_]+)', sheet_url)
        if not match:
            return None

        sheet_id = match.group(1)

        import gspread
        from google.oauth2.service_account import Credentials
        from app.config import settings

        if not os.path.exists(settings.GOOGLE_CREDENTIALS_FILE):
            return None

        scopes = [
            "https://www.googleapis.com/auth/spreadsheets.readonly",
            "https://www.googleapis.com/auth/drive.readonly"
        ]
        creds = Credentials.from_service_account_file(
            settings.GOOGLE_CREDENTIALS_FILE, scopes=scopes
        )
        client = gspread.authorize(creds)
        sheet = client.open_by_key(sheet_id)
        worksheet = sheet.get_worksheet(0)
        records = worksheet.get_all_records()
        return records
    except Exception as e:
        logger.error(f"Error loading sheet from URL: {e}")
        return None
