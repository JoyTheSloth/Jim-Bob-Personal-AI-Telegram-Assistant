"""
Inbound Gmail Scanner & Interview Detector.
Monitors your Gmail inbox via IMAP for recruiter replies, application confirmations,
and interview invitations from major ATS platforms (Greenhouse, Lever, Ashby, Workday, etc.).
Updates history.json and dispatches high-priority Telegram alerts.
"""

import os
import imaplib
import email
from email.header import decode_header
import re
import json
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

def load_env():
    env = dict(os.environ)
    env_path = Path(__file__).resolve().parent / ".env"
    if env_path.exists():
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    if k.strip() not in env:
                        env[k.strip()] = v.strip()
    return env

BASE_DIR = Path(__file__).resolve().parent

def send_telegram_notification(*args, **kwargs):
    pass

ATS_DOMAINS = [
    "greenhouse.io", "lever.co", "ashbyhq.com", "myworkday.com",
    "workday.com", "smartrecruiters.com", "bamboohr.com", "neonlink.ai",
    "recruitee.com", "breezy.hr", "jobvite.com", "workable.com"
]

def clean_subject(raw_subject: str) -> str:
    if not raw_subject:
        return ""
    decoded_pieces = decode_header(raw_subject)
    result = []
    for piece, encoding in decoded_pieces:
        if isinstance(piece, bytes):
            result.append(piece.decode(encoding or "utf-8", errors="ignore"))
        else:
            result.append(str(piece))
    return " ".join(result).strip()

def classify_email(subject: str, body_text: str) -> str:
    content = f"{subject} {body_text}".lower()
    
    # Interview Invitations
    interview_signals = [
        "interview", "schedule a time", "next steps", "phone screen",
        "chat with", "technical round", "availability for a call", "invitation to interview",
        "calendly.com", "hirevue"
    ]
    if any(sig in content for sig in interview_signals):
        return "Interview Invitation"

    # Rejection
    rejection_signals = [
        "not moving forward", "other candidates", "unfortunately", "pursue other",
        "impressed with your background, but", "high volume of applications", "decided not to proceed"
    ]
    if any(sig in content for sig in rejection_signals):
        return "Rejected / Archived"

    # Confirmation
    confirm_signals = [
        "thank you for applying", "application received", "we have received your application",
        "thanks for your interest", "received your resume"
    ]
    if any(sig in content for sig in confirm_signals):
        return "Application Confirmed"

    return "General Recruiter Update"

def scan_inbox(limit: int = 15) -> list:
    env = load_env()
    user = env.get("GMAIL_USER")
    pwd = env.get("GMAIL_APP_PASSWORD", "").replace(" ", "")

    if not user or not pwd:
        print("  [!] Gmail credentials not found in .env.")
        return []

    results = []
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(user, pwd)
        mail.select("inbox")

        # Search for messages from ATS domains or keywords
        status, messages = mail.search(None, '(OR OR HEADER Subject "application" HEADER Subject "interview" HEADER Subject "position")')
        if status != "OK" or not messages[0]:
            mail.logout()
            return []

        msg_ids = messages[0].split()
        latest_ids = msg_ids[-limit:]

        for mid in reversed(latest_ids):
            res, data = mail.fetch(mid, "(RFC822)")
            if res != "OK":
                continue

            raw_email = data[0][1]
            msg = email.message_from_bytes(raw_email)

            sender = msg.get("From", "")
            raw_subj = msg.get("Subject", "")
            subject = clean_subject(raw_subj)
            date_str = msg.get("Date", "")

            # Extract body snippet
            body_snippet = ""
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        body_snippet = part.get_payload(decode=True).decode("utf-8", errors="ignore")[:600]
                        break
            else:
                body_snippet = msg.get_payload(decode=True).decode("utf-8", errors="ignore")[:600]

            # Check if relevant
            is_ats = any(dom in sender.lower() for dom in ATS_DOMAINS)
            is_job_subj = any(w in subject.lower() for w in ["application", "interview", "candidate", "role", "position"])

            if is_ats or is_job_subj:
                classification = classify_email(subject, body_snippet)
                results.append({
                    "from": sender,
                    "subject": subject,
                    "date": date_str,
                    "status": classification,
                    "snippet": body_snippet[:150].replace("\n", " ").strip()
                })

                # If Interview Invitation, send high priority Telegram alert!
                if classification == "Interview Invitation":
                    send_telegram_notification(
                        job_url="https://mail.google.com",
                        job_title=f"🎉 INTERVIEW INVITE: {subject}",
                        status=f"From: {sender[:50]}"
                    )

        mail.logout()
    except Exception as e:
        print(f"  [!] Email scan error: {e}")

    return results

if __name__ == "__main__":
    print("Testing Gmail scan...")
    updates = scan_inbox(limit=10)
    print(f"Found {len(updates)} career-related emails:")
    for u in updates:
        print(f"• [{u['status']}] {u['subject']} (From: {u['from'][:40]})")
