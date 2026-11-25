import json
import sqlite3
from pathlib import Path

DB_PATH = Path('applications.db')

def get_applied_emails():
    if not DB_PATH.exists():
        return set()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT recipient_email FROM applications")
    emails = {row[0].lower() for row in cursor.fetchall() if row[0]}
    cursor.execute("SELECT company FROM applications")
    companies = {row[0].lower() for row in cursor.fetchall() if row[0]}
    conn.close()
    return emails, companies

def analyze():
    with open('verified_leads.json', 'r', encoding='utf-8') as f:
        leads = json.load(f)

    applied_emails, applied_companies = get_applied_emails()

    email_leads = []
    portal_junior_leads = []
    portal_mid_leads = []
    portal_senior_leads = []

    for l in leads:
        company_lower = (l.get('company') or '').lower()
        emails = [e for e in l.get('emails', []) if e.lower() not in applied_emails]
        if company_lower in applied_companies and not emails:
            continue

        l['fresh_emails'] = emails
        if emails:
            email_leads.append(l)
        elif l.get('is_junior'):
            portal_junior_leads.append(l)
        elif not l.get('is_senior'):
            portal_mid_leads.append(l)
        else:
            portal_senior_leads.append(l)

    print(f"Total leads analyzed: {len(leads)}")
    print(f"Direct Email Outreach Leads: {len(email_leads)}")
    print(f"Junior / Entry Web / React / UI-UX Portal Leads: {len(portal_junior_leads)}")
    print(f"Mid-Level Web / React / UI-UX Portal Leads: {len(portal_mid_leads)}")
    print(f"Senior Leads: {len(portal_senior_leads)}")

    print("\n--- DIRECT EMAIL LEADS ---")
    for i, l in enumerate(email_leads, 1):
        print(f"[{i}] [{l['category']}] {l['title']} at {l['company']}")
        print(f"    Emails: {', '.join(l['fresh_emails'])}")
        print(f"    Source: {l['source']} | URL: {l['url']}")
        print(f"    Snippet: {l.get('raw_snippet', '')[:120]}...")

    print("\n--- JUNIOR / ENTRY PORTAL LEADS ---")
    for i, l in enumerate(portal_junior_leads, 1):
        print(f"[{i}] [{l['category']}] {l['title']} at {l['company']}")
        print(f"    Source: {l['source']} | Location: {l['location']} | Salary: {l['salary']}")
        print(f"    Apply URL: {l['url']}")

    print("\n--- FRESH MID / OPEN PORTAL LEADS (Top 10) ---")
    for i, l in enumerate(portal_mid_leads[:10], 1):
        print(f"[{i}] [{l['category']}] {l['title']} at {l['company']}")
        print(f"    Source: {l['source']} | Location: {l['location']} | Salary: {l['salary']}")
        print(f"    Apply URL: {l['url']}")

if __name__ == "__main__":
    analyze()
