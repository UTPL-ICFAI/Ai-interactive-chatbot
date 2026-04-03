"""
Email Service
Sends marketing and confirmation emails to leads.
"""
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.config import settings

logger = logging.getLogger(__name__)


def _build_welcome_email(name: str, course: str, email: str) -> MIMEMultipart:
    """Build a beautiful HTML welcome/marketing email."""
    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"🌟 Join Us Today! Special 50% OFF Admission for {name} | {settings.COMPANY_NAME}"
    msg["From"] = f"Ushnik Admissions <{settings.FROM_EMAIL}>"
    msg["To"] = email

    # Plain text fallback
    text = f"""
Dear {name},

Thank you for showing interest in {settings.COMPANY_NAME}!

🎓 Course: {course}
🎉 Admissions are currently OPEN
🔥 You are eligible for 50% OFF on your first course!

Our admissions team will contact you shortly with more details.

If you have any questions, feel free to:
📞 Call us: {settings.COMPANY_PHONE}
📧 Email us: {settings.COMPANY_EMAIL}
📍 Visit us: {settings.COMPANY_ADDRESS}

Best regards,
Admissions Team
{settings.COMPANY_NAME}
"""

    # Rich HTML email
    html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f0f2f5;">
    <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #f0f2f5; padding: 40px 20px;">
        <tr>
            <td align="center">
                <table width="600" cellpadding="0" cellspacing="0" style="background-color: #ffffff; border-radius: 16px; overflow: hidden; box-shadow: 0 4px 24px rgba(0,0,0,0.1);">
                    <!-- Header -->
                    <tr>
                        <td style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 40px 30px; text-align: center;">
                            <h1 style="color: #ffffff; margin: 0; font-size: 28px; font-weight: 700;">
                                🎉 Admissions Are Open!
                            </h1>
                            <p style="color: rgba(255,255,255,0.9); margin: 10px 0 0; font-size: 16px;">
                                {settings.COMPANY_NAME}
                            </p>
                        </td>
                    </tr>

                    <!-- Body -->
                    <tr>
                        <td style="padding: 40px 30px;">
                            <p style="font-size: 18px; color: #333; margin: 0 0 20px;">
                                Dear <strong>{name}</strong>,
                            </p>
                            <p style="font-size: 16px; color: #555; line-height: 1.6; margin: 0 0 25px;">
                                We saw your interest in our courses! We'd love for you to **join us** and start your career journey with the best training in the industry.
                            </p>

                            <!-- Discount Banner -->
                            <table width="100%" cellpadding="0" cellspacing="0" style="background: linear-gradient(135deg, #ff6b6b, #ee5a24); border-radius: 12px; margin: 0 0 25px;">
                                <tr>
                                    <td style="padding: 25px; text-align: center;">
                                        <p style="color: #fff; font-size: 14px; margin: 0 0 5px; text-transform: uppercase; letter-spacing: 2px;">
                                            Exclusive Offer
                                        </p>
                                        <p style="color: #fff; font-size: 36px; font-weight: 800; margin: 0;">
                                            50% OFF
                                        </p>
                                        <p style="color: rgba(255,255,255,0.9); font-size: 14px; margin: 5px 0 0;">
                                            on your first course enrollment
                                        </p>
                                    </td>
                                </tr>
                            </table>

                            <!-- Course Info -->
                            <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #f8f9ff; border-radius: 12px; border: 1px solid #e8eaff; margin: 0 0 25px;">
                                <tr>
                                    <td style="padding: 20px;">
                                        <p style="font-size: 14px; color: #667eea; margin: 0 0 10px; text-transform: uppercase; letter-spacing: 1px; font-weight: 600;">
                                            Your Interested Course
                                        </p>
                                        <p style="font-size: 20px; color: #333; margin: 0; font-weight: 700;">
                                            🎓 {course}
                                        </p>
                                    </td>
                                </tr>
                            </table>

                            <p style="font-size: 16px; color: #555; line-height: 1.6; margin: 0 0 25px;">
                                Our admissions team will contact you shortly with detailed course information, curriculum, and enrollment steps.
                            </p>

                            <!-- CTA Button -->
                            <table width="100%" cellpadding="0" cellspacing="0">
                                <tr>
                                    <td align="center" style="padding: 10px 0 25px;">
                                        <a href="https://ushniktechnologies.com/" style="background: linear-gradient(135deg, #667eea, #764ba2); color: #fff; padding: 14px 40px; border-radius: 50px; text-decoration: none; font-size: 16px; font-weight: 600; display: inline-block;">
                                            Join Us Today! →
                                        </a>
                                    </td>
                                </tr>
                            </table>

                            <!-- Divider -->
                            <hr style="border: none; border-top: 1px solid #eee; margin: 0 0 25px;">

                            <!-- Contact Info -->
                            <p style="font-size: 14px; color: #888; margin: 0 0 10px;">
                                <strong>Need help?</strong> Reach out to us:
                            </p>
                            <p style="font-size: 14px; color: #888; line-height: 1.8; margin: 0;">
                                📞 {settings.COMPANY_PHONE}<br>
                                📧 {settings.COMPANY_EMAIL}<br>
                                📍 {settings.COMPANY_ADDRESS}
                            </p>
                        </td>
                    </tr>

                    <!-- Footer -->
                    <tr>
                        <td style="background-color: #f8f9fa; padding: 25px 30px; text-align: center; border-top: 1px solid #eee;">
                            <p style="font-size: 13px; color: #999; margin: 0;">
                                © 2025 {settings.COMPANY_NAME}. All rights reserved.
                            </p>
                            <p style="font-size: 12px; color: #bbb; margin: 5px 0 0;">
                                AI at Work, Innovation in Action
                            </p>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>
"""

    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")
    msg.attach(part1)
    msg.attach(part2)

    return msg


def send_welcome_email(name: str, email: str, course: str) -> bool:
    """
    Send a welcome/marketing email to a new lead.
    Returns True on success, False on failure.
    """
    if not settings.SMTP_USERNAME or not settings.SMTP_PASSWORD:
        logger.warning("SMTP not configured – skipping email send")
        return False

    try:
        msg = _build_welcome_email(name, course, email)

        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
            server.send_message(msg)

        logger.info(f"Welcome email sent to {email}")
        return True

    except Exception as e:
        logger.error(f"Failed to send email to {email}: {e}")
        return False


def send_admin_notification(lead_data: dict) -> bool:
    """Send notification to admin about a new lead."""
    if not settings.SMTP_USERNAME or not settings.SMTP_PASSWORD:
        return False

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"🆕 New Lead: {lead_data.get('name', 'Unknown')} – {lead_data.get('course', 'N/A')}"
        msg["From"] = f"{settings.COMPANY_NAME} Bot <{settings.FROM_EMAIL}>"
        msg["To"] = settings.COMPANY_EMAIL

        html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; padding: 20px;">
            <h2 style="color: #667eea;">🆕 New Lead Received</h2>
            <table style="border-collapse: collapse; width: 100%; max-width: 500px;">
                <tr style="background: #f8f9ff;">
                    <td style="padding: 12px; border: 1px solid #ddd; font-weight: bold;">Name</td>
                    <td style="padding: 12px; border: 1px solid #ddd;">{lead_data.get('name', '')}</td>
                </tr>
                <tr>
                    <td style="padding: 12px; border: 1px solid #ddd; font-weight: bold;">Email</td>
                    <td style="padding: 12px; border: 1px solid #ddd;">{lead_data.get('email', '')}</td>
                </tr>
                <tr style="background: #f8f9ff;">
                    <td style="padding: 12px; border: 1px solid #ddd; font-weight: bold;">Phone</td>
                    <td style="padding: 12px; border: 1px solid #ddd;">{lead_data.get('phone', '')}</td>
                </tr>
                <tr>
                    <td style="padding: 12px; border: 1px solid #ddd; font-weight: bold;">Course</td>
                    <td style="padding: 12px; border: 1px solid #ddd;">{lead_data.get('course', '')}</td>
                </tr>
                <tr style="background: #f8f9ff;">
                    <td style="padding: 12px; border: 1px solid #ddd; font-weight: bold;">Message</td>
                    <td style="padding: 12px; border: 1px solid #ddd;">{lead_data.get('message', '')}</td>
                </tr>
                <tr>
                    <td style="padding: 12px; border: 1px solid #ddd; font-weight: bold;">Time</td>
                    <td style="padding: 12px; border: 1px solid #ddd;">{lead_data.get('timestamp', '')}</td>
                </tr>
            </table>
        </body>
        </html>
        """

        msg.attach(MIMEText(html, "html"))

        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
            server.send_message(msg)

        logger.info(f"Admin notification sent for lead: {lead_data.get('name')}")
        return True

    except Exception as e:
        logger.error(f"Failed to send admin notification: {e}")
        return False
