import json
import sqlite3
from pathlib import Path

DB_PATH = Path('applications.db')

def get_applied():
    if not DB_PATH.exists():
        return set(), set()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT recipient_email, company FROM applications")
    rows = c.fetchall()
    emails = {r[0].lower() for r in rows if r[0]}
    companies = {r[1].lower() for r in rows if r[1]}
    conn.close()
    return emails, companies

def run():
    with open('verified_leads.json', 'r', encoding='utf-8') as f:
        leads = json.load(f)

    applied_emails, applied_companies = get_applied()

    seen = set()
    unique_leads = []
    for l in leads:
        key = (l.get('company', '').lower().strip(), l.get('title', '').lower().strip())
        if key in seen:
            continue
        seen.add(key)
        unique_leads.append(l)

    print(f"Total Unique Leads: {len(unique_leads)}")

    email_leads = []
    junior_leads = []
    react_leads = []
    uiux_leads = []
    webdev_leads = []

    # Noise filter for job seekers in HN
    def is_job_seeker(l):
        text = (l.get('raw_snippet', '') + ' ' + l.get('title', '')).lower()
        if 'willing to relocate' in text or 'résumé' in text or 'resume/cv' in text or 'building real-time ai systems' in text:
            return True
        return False

    for l in unique_leads:
        if is_job_seeker(l):
            continue

        company = l.get('company', '')
        title = l.get('title', '')
        cat = l.get('category', '')
        emails = l.get('emails', [])
        fresh_emails = [e for e in emails if e.lower() not in applied_emails]
        l['fresh_emails'] = fresh_emails

        # Status
        already_applied = (company.lower() in applied_companies) or any(e.lower() in applied_emails for e in emails)
        l['already_applied'] = already_applied

        if fresh_emails:
            email_leads.append(l)

        if l.get('is_junior'):
            junior_leads.append(l)
        elif cat == 'UI/UX Designer':
            uiux_leads.append(l)
        elif cat == 'React Developer':
            react_leads.append(l)
        elif cat in ['Frontend Developer', 'Web Developer']:
            webdev_leads.append(l)

    print(f"\n--- Direct Email Outreach Leads (Fresh & Unsent): {len(email_leads)} ---")
    for i, l in enumerate(email_leads, 1):
        print(f"[{i}] {l['title']} @ {l['company']} ({l['category']})")
        print(f"    Source: {l['source']} | Location: {l['location']}")
        print(f"    Emails: {', '.join(l['fresh_emails'])}")
        print(f"    URL: {l['url']}")

    print(f"\n--- Junior / Entry-Level Leads: {len(junior_leads)} ---")
    for i, l in enumerate(junior_leads, 1):
        applied_mark = " [ALREADY APPLIED]" if l['already_applied'] else ""
        print(f"[{i}] {l['title']} @ {l['company']} ({l['category']}){applied_mark}")
        print(f"    Source: {l['source']} | Location: {l['location']} | Salary: {l['salary']}")
        print(f"    URL: {l['url']}")

    print(f"\n--- Remote UI/UX Designer Leads (Mid/Open): {len(uiux_leads)} ---")
    for i, l in enumerate(uiux_leads, 1):
        print(f"[{i}] {l['title']} @ {l['company']}")
        print(f"    Source: {l['source']} | Location: {l['location']} | URL: {l['url']}")

    print(f"\n--- Remote React Developer Leads (Mid/Open): {len(react_leads)} ---")
    for i, l in enumerate(react_leads, 1):
        print(f"[{i}] {l['title']} @ {l['company']}")
        print(f"    Source: {l['source']} | Location: {l['location']} | URL: {l['url']}")

    print(f"\n--- Remote Frontend / Web Developer Leads (Mid/Open): {len(webdev_leads)} ---")
    for i, l in enumerate(webdev_leads, 1):
        print(f"[{i}] {l['title']} @ {l['company']}")
        print(f"    Source: {l['source']} | Location: {l['location']} | URL: {l['url']}")

if __name__ == "__main__":
    run()
