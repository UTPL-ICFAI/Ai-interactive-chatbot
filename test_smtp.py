import smtplib
from dotenv import load_dotenv
import os

load_dotenv()

host = "smtp.gmail.com"
port = 587
user = os.getenv("SMTP_USERNAME")
pwd = os.getenv("SMTP_PASSWORD")

print(f"Testing with User: {user}")
print(f"Testing with Pwd: {pwd}")

try:
    server = smtplib.SMTP(host, port)
    server.starttls()
    server.login(user, pwd)
    print("SUCCESS: Connection and Login successful!")
    server.quit()
except Exception as e:
    print(f"FAILED: {e}")
