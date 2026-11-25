import urllib.request
import json
import re
import xml.etree.ElementTree as ET
import sqlite3
from pathlib import Path

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

DB_PATH = Path('applications.db')

def get_applied():
    if not DB_PATH.exists():
        return set(), set()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT recipient_email, company FROM applications")
    rows = c.fetchall()
    emails = {r[0].lower().strip() for r in rows if r[0]}
    companies = {r[1].lower().strip() for r in rows if r[1]}
    conn.close()
    return emails, companies

def clean_html(raw_html):
    if not raw_html:
        return ""
    cleanr = re.compile(r'<.*?>|&[a-z0-9#]+;')
    text = re.sub(cleanr, ' ', raw_html)
    return ' '.join(text.split())

def extract_emails(text):
    if not text:
        return []
    cleaned_text = re.sub(r'\[at\]|\(at\)', '@', text, flags=re.IGNORECASE)
    cleaned_text = re.sub(r'\[dot\]|\(dot\)', '.', cleaned_text, flags=re.IGNORECASE)
    found = re.findall(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', cleaned_text)
    cleaned = []
    ignored = ['remoteok', 'example.com', 'domain.com', 'w3.org', 'sentry.io', 'github.com', 'schema.org', 'arbeitnow.com', 'ycombinator.com', 'weworkremotely.com', 'remotive.com']
    for e in found:
        e = e.strip(".,;:()<>[]\"' ")
        domain = e.split('@')[-1].lower() if '@' in e else ''
        if not any(ign in domain for ign in ignored) and '.' in domain:
            cleaned.append(e)
    return list(dict.fromkeys(cleaned))

def evaluate_job(title, company, description, tags=None):
    t_lower = (title or "").lower()
    d_lower = (description or "").lower()
    tags_lower = [t.lower() for t in (tags or [])]
    full_text = f"{t_lower} {' '.join(tags_lower)} {d_lower[:500]}"

    # Disqualify irrelevant non-tech/non-design
    irrelevant = [
        'accountant', 'legal', 'tax', 'nurse', 'recruiter', 'hr manager',
        'creative director', 'data analyst', 'business analyst', 'marketing manager',
        'sales manager', 'payroll', 'academic', 'inpatient coding'
    ]
    if any(irr in t_lower for irr in irrelevant):
        return None

    # Categorize
    is_uiux = any(k in t_lower for k in [
        'ui/ux', 'uiux', 'ux/ui', 'ui designer', 'ux designer', 'product designer',
        'interaction designer', 'visual designer', 'web designer'
    ]) or (any(k in tags_lower for k in ['ui/ux', 'ui designer', 'ux designer', 'design']) and ('design' in t_lower or 'product' in t_lower))

    is_react = any(k in t_lower for k in [
        'react', 'react.js', 'reactjs', 'next.js', 'nextjs'
    ]) or any(k in tags_lower for k in ['react', 'nextjs', 'next.js'])

    is_webdev = any(k in t_lower for k in [
        'web developer', 'web dev', 'frontend', 'front-end', 'front end',
        'ui developer', 'ui engineer', 'javascript developer', 'typescript developer'
    ]) or any(k in tags_lower for k in ['frontend', 'front-end', 'web development'])

    if is_uiux:
        category = "UI/UX Designer"
        role_type = "uiux"
    elif is_react:
        category = "React Developer"
        role_type = "frontend"
    elif is_webdev:
        category = "Web Developer"
        role_type = "frontend"
    else:
        return None

    # Seniority classification
    senior_patterns = [
        r'\bsenior\b', r'\bsr\.?\b', r'\blead\b', r'\bprincipal\b',
        r'\bhead of\b', r'\bdirector\b', r'\bstaff\b', r'\barchitect\b'
    ]
    is_senior = any(re.search(pat, t_lower) for pat in senior_patterns)

    junior_patterns = [
        r'\bjunior\b', r'\bjr\.?\b', r'\bentry\b', r'\bintern\b',
        r'\bassociate\b', r'\b0-2\b', r'\b1-2\b', r'\b1-3\b',
        r'\bgraduate\b', r'\bearly[- ]career\b'
    ]
    is_junior = any(re.search(pat, t_lower) for pat in junior_patterns) or any(re.search(pat, d_lower[:400]) for pat in junior_patterns)

    return {
        'category': category,
        'role_type': role_type,
        'is_senior': is_senior,
        'is_junior': is_junior
    }

def fetch_all():
    leads = []
    seen_keys = set()

    # --- 1. RemoteOK ---
    print("Scraping RemoteOK API...")
    rok_tags = ['', 'junior', 'react', 'javascript', 'ui', 'ux', 'designer', 'web-dev']
    for tag in rok_tags:
        url = f"https://remoteok.com/api?tag={tag}" if tag else "https://remoteok.com/api"
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=12) as resp:
                data = json.loads(resp.read().decode())
                for item in data[1:]:
                    jid = item.get('id')
                    key = ('remoteok', str(jid))
                    if key in seen_keys:
                        continue
                    seen_keys.add(key)

                    title = item.get('position', '')
                    company = item.get('company', '')
                    desc = item.get('description', '')
                    tags = item.get('tags', [])

                    eval_res = evaluate_job(title, company, desc, tags)
                    if eval_res:
                        emails = extract_emails(desc)
                        s_min = item.get('salary_min')
                        s_max = item.get('salary_max')
                        salary = f"${s_min:,} - ${s_max:,}" if s_min and s_max else "Not specified"
                        leads.append({
                            'source': 'RemoteOK',
                            'title': title,
                            'company': company,
                            'category': eval_res['category'],
                            'role_type': eval_res['role_type'],
                            'is_senior': eval_res['is_senior'],
                            'is_junior': eval_res['is_junior'],
                            'location': item.get('location', 'Remote') or 'Remote',
                            'salary': salary,
                            'url': item.get('url') or item.get('apply_url'),
                            'apply_url': item.get('apply_url') or item.get('url'),
                            'emails': emails,
                            'date': item.get('date', ''),
                            'raw_snippet': clean_html(desc)[:300]
                        })
        except Exception as e:
            print(f"RemoteOK error ({tag}): {e}")

    # --- 2. WeWorkRemotely ---
    print("Scraping We Work Remotely Feeds...")
    wwr_feeds = [
        'https://weworkremotely.com/categories/remote-front-end-programming-jobs.rss',
        'https://weworkremotely.com/categories/remote-full-stack-programming-jobs.rss',
        'https://weworkremotely.com/categories/remote-design-jobs.rss'
    ]
    for feed_url in wwr_feeds:
        try:
            req = urllib.request.Request(feed_url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=12) as resp:
                xml_content = resp.read().decode('utf-8', errors='ignore')
                root = ET.fromstring(xml_content)
                for item in root.findall('./channel/item'):
                    link = item.findtext('link', '')
                    key = ('wwr', link)
                    if key in seen_keys:
                        continue
                    seen_keys.add(key)

                    title_raw = item.findtext('title', '')
                    desc = item.findtext('description', '')
                    pub_date = item.findtext('pubDate', '')

                    company = "Unknown"
                    job_title = title_raw
                    if ':' in title_raw:
                        parts = title_raw.split(':', 1)
                        company = parts[0].strip()
                        job_title = parts[1].strip()

                    eval_res = evaluate_job(job_title, company, desc)
                    if eval_res:
                        emails = extract_emails(desc)
                        leads.append({
                            'source': 'WeWorkRemotely',
                            'title': job_title,
                            'company': company,
                            'category': eval_res['category'],
                            'role_type': eval_res['role_type'],
                            'is_senior': eval_res['is_senior'],
                            'is_junior': eval_res['is_junior'],
                            'location': 'Remote',
                            'salary': 'Not specified',
                            'url': link,
                            'apply_url': link,
                            'emails': emails,
                            'date': pub_date,
                            'raw_snippet': clean_html(desc)[:300]
                        })
        except Exception as e:
            print(f"WWR error: {e}")

    # --- 3. Remotive ---
    print("Scraping Remotive API...")
    for cat_slug in ['software-dev', 'design']:
        try:
            req = urllib.request.Request(f'https://remotive.com/api/remote-jobs?category={cat_slug}&limit=60', headers=HEADERS)
            with urllib.request.urlopen(req, timeout=12) as resp:
                data = json.loads(resp.read().decode())
                for item in data.get('jobs', []):
                    jid = item.get('id')
                    key = ('remotive', str(jid))
                    if key in seen_keys:
                        continue
                    seen_keys.add(key)

                    title = item.get('title', '')
                    desc = item.get('description', '')
                    tags = item.get('tags', [])
                    eval_res = evaluate_job(title, item.get('company_name'), desc, tags)
                    if eval_res:
                        emails = extract_emails(desc)
                        leads.append({
                            'source': 'Remotive',
                            'title': title,
                            'company': item.get('company_name', 'Unknown'),
                            'category': eval_res['category'],
                            'role_type': eval_res['role_type'],
                            'is_senior': eval_res['is_senior'],
                            'is_junior': eval_res['is_junior'],
                            'location': item.get('candidate_required_location', 'Remote'),
                            'salary': item.get('salary', 'Not specified'),
                            'url': item.get('url'),
                            'apply_url': item.get('url'),
                            'emails': emails,
                            'date': item.get('publication_date', ''),
                            'raw_snippet': clean_html(desc)[:300]
                        })
        except Exception as e:
            print(f"Remotive error: {e}")

    # --- 4. Hacker News Who is Hiring ---
    print("Scraping Hacker News Who is Hiring...")
    story_id = 50338728
    queries = ['react', 'frontend', 'web', 'designer', 'ui', 'ux']
    for q in queries:
        try:
            url = f"https://hn.algolia.com/api/v1/search?tags=comment,story_{story_id}&query={q}&hitsPerPage=50"
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode())
                for hit in data.get('hits', []):
                    c_id = hit.get('objectID')
                    key = ('hn', str(c_id))
                    if key in seen_keys:
                        continue
                    seen_keys.add(key)

                    text = hit.get('comment_text', '')
                    cleaned = clean_html(text)
                    if not re.search(r'\bremote\b', cleaned, re.IGNORECASE):
                        continue

                    # Filter out job seekers posting "SEEKING WORK"
                    if re.search(r'\bseeking work\b|\bseeking freelance\b|\br[eé]sum[eé]\b|\bportfolio:|\bfor hire\b', cleaned, re.IGNORECASE):
                        continue

                    first_line = cleaned.split('\n')[0] if cleaned else ''
                    emails = extract_emails(cleaned)
                    parts = [p.strip() for p in first_line.split('|')]
                    company = parts[0] if parts else "HackerNews Company"
                    title = parts[1] if len(parts) > 1 else first_line[:50]

                    eval_res = evaluate_job(title + " " + cleaned[:200], company, cleaned)
                    if eval_res:
                        leads.append({
                            'source': 'HackerNews (Who is Hiring)',
                            'title': title,
                            'company': company,
                            'category': eval_res['category'],
                            'role_type': eval_res['role_type'],
                            'is_senior': eval_res['is_senior'],
                            'is_junior': eval_res['is_junior'],
                            'location': 'Remote',
                            'salary': 'See posting',
                            'url': f"https://news.ycombinator.com/item?id={c_id}",
                            'apply_url': f"https://news.ycombinator.com/item?id={c_id}",
                            'emails': emails,
                            'date': hit.get('created_at', ''),
                            'raw_snippet': cleaned[:300]
                        })
        except Exception as e:
            print(f"HN error ({q}): {e}")

    return leads

def main():
    leads = fetch_all()
    applied_emails, applied_companies = get_applied()

    # Deduplicate by company + title
    dedup = {}
    for l in leads:
        k = (l['company'].lower().strip(), l['title'].lower().strip())
        if k not in dedup:
            dedup[k] = l
    unique_leads = list(dedup.values())

    print(f"\n=======================================================")
    print(f"Found {len(unique_leads)} unique matching job openings across boards.")
    print(f"=======================================================\n")

    # Add status
    for l in unique_leads:
        already = (l['company'].lower().strip() in applied_companies) or any(e.lower().strip() in applied_emails for e in l['emails'])
        l['already_applied'] = already

    # Categorize leads
    junior_web_devs = [l for l in unique_leads if (l['is_junior'] or (not l['is_senior'] and 'junior' in l['title'].lower())) and l['category'] in ['Web Developer', 'Frontend Developer', 'React Developer']]
    react_devs = [l for l in unique_leads if l['category'] == 'React Developer']
    uiux_designers = [l for l in unique_leads if l['category'] == 'UI/UX Designer']
    web_devs = [l for l in unique_leads if l['category'] == 'Web Developer' or (l['category'] == 'Frontend Developer' and not l['is_senior'])]

    # Save to json
    with open('fresh_scanned_leads.json', 'w', encoding='utf-8') as f:
        json.dump(unique_leads, f, indent=2)

    print(f"Summary by Category:")
    print(f"- Junior / Entry Web & React Developers: {len(junior_web_devs)}")
    print(f"- React Developers (All Seniority): {len(react_devs)}")
    print(f"- UI/UX Designers (All Seniority): {len(uiux_designers)}")
    print(f"- Web / Frontend Developers (Junior/Mid): {len(web_devs)}")

    direct_email_leads = [l for l in unique_leads if l['emails'] and not l['already_applied']]
    print(f"\nDirect Email Leads (Ready for send_application.py): {len(direct_email_leads)}")
    for i, l in enumerate(direct_email_leads, 1):
        print(f"[{i}] {l['title']} @ {l['company']} ({l['category']})")
        print(f"    Emails: {', '.join(l['emails'])} | Source: {l['source']}")
        print(f"    URL: {l['url']}")

if __name__ == '__main__':
    main()
