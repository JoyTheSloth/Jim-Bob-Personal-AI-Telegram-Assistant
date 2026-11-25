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

    def is_hiring(l):
        text = (l.get('raw_snippet', '') + ' ' + l.get('title', '')).lower()
        return not any(w in text for w in ['willing to relocate', 'seeking freelance', 'seeking work', 'résumé', 'cv:'])

    clean = [l for l in leads if is_hiring(l)]

    print(f"Total clean postings: {len(clean)}")

    # Groupings
    junior_leads = []
    uiux_leads = []
    react_leads = []
    webdev_leads = []
    email_leads = []

    seen = set()
    for l in clean:
        key = (l.get('company', '').lower().strip(), l.get('title', '').lower().strip())
        if key in seen:
            continue
        seen.add(key)

        company = l.get('company', '')
        emails = l.get('emails', [])
        applied = (company.lower() in applied_companies) or any(e.lower() in applied_emails for e in emails)
        l['already_applied'] = applied

        if emails:
            email_leads.append(l)

        if l.get('is_junior'):
            junior_leads.append(l)
        elif l.get('category') == 'UI/UX Designer':
            uiux_leads.append(l)
        elif l.get('category') == 'React Developer':
            react_leads.append(l)
        else:
            webdev_leads.append(l)

    print("\n================== JUNIOR / ENTRY OPENINGS ==================")
    for i, l in enumerate(junior_leads, 1):
        status = "[ALREADY APPLIED]" if l['already_applied'] else "[FRESH]"
        print(f"{i}. {status} {l['title']} @ {l['company']}")
        print(f"   Category: {l['category']} | Source: {l['source']} | Loc: {l['location']}")
        print(f"   Emails: {l.get('emails')} | Salary: {l.get('salary')}")
        print(f"   URL: {l['url']}")

    print("\n================== UI/UX DESIGNER OPENINGS ==================")
    for i, l in enumerate(uiux_leads, 1):
        status = "[ALREADY APPLIED]" if l['already_applied'] else "[FRESH]"
        print(f"{i}. {status} {l['title']} @ {l['company']}")
        print(f"   Category: {l['category']} | Source: {l['source']} | Loc: {l['location']}")
        print(f"   Emails: {l.get('emails')} | Salary: {l.get('salary')}")
        print(f"   URL: {l['url']}")

    print("\n================== TOP REACT OPENINGS ==================")
    for i, l in enumerate(react_leads[:15], 1):
        status = "[ALREADY APPLIED]" if l['already_applied'] else "[FRESH]"
        print(f"{i}. {status} {l['title']} @ {l['company']}")
        print(f"   Category: {l['category']} | Source: {l['source']} | Loc: {l['location']}")
        print(f"   Emails: {l.get('emails')} | Salary: {l.get('salary')}")
        print(f"   URL: {l['url']}")

    print("\n================== DIRECT EMAIL OUTREACH LEADS ==================")
    for i, l in enumerate(email_leads, 1):
        status = "[ALREADY APPLIED]" if l['already_applied'] else "[FRESH]"
        print(f"{i}. {status} {l['title']} @ {l['company']}")
        print(f"   Role Type: {l.get('role_type')} | Category: {l.get('category')}")
        print(f"   Emails: {l.get('emails')}")
        print(f"   Source: {l['source']} | URL: {l['url']}")
        print(f"   Snippet: {l.get('raw_snippet', '')[:160]}...")

if __name__ == '__main__':
    run()
