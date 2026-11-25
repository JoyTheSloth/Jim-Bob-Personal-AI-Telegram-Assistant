"""Send a weekly HTML email summary of applications sent in the last 7 days."""
import os
import sqlite3
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import tracker

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

def send_weekly_summary():
    gmail_user = os.getenv("GMAIL_USER")
    gmail_pass = os.getenv("GMAIL_APP_PASSWORD")
    if not gmail_user or not gmail_pass or not tracker.DB_PATH.exists():
        return

    conn = sqlite3.connect(tracker.DB_PATH)
    c = conn.cursor()
    c.execute(
        "SELECT company, recipient_email, role, sent_at FROM applications "
        "WHERE datetime(sent_at) >= datetime('now', '-7 days') ORDER BY sent_at DESC"
    )
    rows = c.fetchall()
    conn.close()

    table_rows = "".join(
        f"<tr><td style='padding:8px;border-bottom:1px solid #eee;'><b>{comp}</b></td>"
        f"<td style='padding:8px;border-bottom:1px solid #eee;'>{email}</td>"
        f"<td style='padding:8px;border-bottom:1px solid #eee;'>{role}</td>"
        f"<td style='padding:8px;border-bottom:1px solid #eee;'>{str(sent_at)[:10]}</td></tr>"
        for comp, email, role, sent_at in rows
    ) or "<tr><td colspan='4' style='padding:8px;'>No applications sent in the last 7 days.</td></tr>"

    html_body = (
        f"<html><body style='font-family:Arial,sans-serif;color:#111;'>"
        f"<h2>Jim Bob's Weekly Outreach Summary ({len(rows)} sent)</h2>"
        f"<table style='width:100%;border-collapse:collapse;'>"
        f"<tr style='background:#f4f4f5;text-align:left;'><th style='padding:8px;'>Company</th>"
        f"<th style='padding:8px;'>Email</th><th style='padding:8px;'>Role</th><th style='padding:8px;'>Date</th></tr>"
        f"{table_rows}</table></body></html>"
    )
    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"Jim Bob Weekly Summary: {len(rows)} Applications Sent"
    msg["From"] = gmail_user
    msg["To"] = gmail_user
    msg.attach(MIMEText(html_body, "html"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(gmail_user, gmail_pass)
        server.sendmail(gmail_user, gmail_user, msg.as_string())
    print(f"Sent weekly summary ({len(rows)} applications) to {gmail_user}")

if __name__ == "__main__":
    send_weekly_summary()
