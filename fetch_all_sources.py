import urllib.request
import json
import re
import xml.etree.ElementTree as ET
from datetime import datetime

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def clean_html(raw_html):
    if not raw_html:
        return ""
    cleanr = re.compile(r'<.*?>|&[a-z]+;')
    text = re.sub(cleanr, ' ', raw_html)
    return ' '.join(text.split())

def extract_emails(text):
    if not text:
        return []
    cleaned_text = re.sub(r'\[at\]|\(at\)', '@', text, flags=re.IGNORECASE)
    cleaned_text = re.sub(r'\[dot\]|\(dot\)', '.', cleaned_text, flags=re.IGNORECASE)
    found = re.findall(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', cleaned_text)
    cleaned = []
    ignored = ['remoteok', 'example.com', 'domain.com', 'w3.org', 'sentry.io', 'github.com', 'schema.org', 'arbeitnow.com', 'ycombinator.com']
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
    full_title_tags = f"{t_lower} {' '.join(tags_lower)}"

    # Exclude senior/lead/manager roles (fresher & entry-level only)
    senior_titles = [
        'senior', 'sr.', 'sr ', 'staff', 'principal', 'lead', 'manager',
        'director', 'architect', 'head of', 'vp ', 'vice president', 'chief'
    ]
    if any(s in t_lower for s in senior_titles):
        return None

    # Exclude non-relevant domains
    irrelevant_titles = [
        'accountant', 'wedding coordinator', 'sales executive', 'tax manager',
        'property manager', 'operations manager', 'academic dean', 'payroll',
        'legal counsel', 'nurse', 'recruiter', 'hr manager', 'chief human resources',
        'creative director', 'data analyst', 'business analyst', 'marketing manager'
    ]
    if any(irr in t_lower for irr in irrelevant_titles):
        return None

    # Categorize
    category = None
    role_type = None

    is_uiux = any(k in t_lower for k in [
        'ui/ux', 'uiux', 'ux/ui', 'ui designer', 'ux designer', 'product designer',
        'interaction designer', 'visual designer', 'web designer'
    ]) or (any(k in tags_lower for k in ['ui/ux', 'ui designer', 'ux designer']) and 'design' in t_lower)

    is_react = any(k in t_lower for k in [
        'react', 'react.js', 'reactjs', 'next.js', 'nextjs'
    ])

    is_frontend = any(k in t_lower for k in [
        'frontend', 'front-end', 'front end', 'ui developer', 'ui engineer'
    ]) or (is_react)

    is_webdev = any(k in t_lower for k in [
        'web developer', 'web dev', 'wordpress developer', 'shopify developer',
        'javascript developer', 'typescript developer'
    ])

    if is_uiux:
        category = "UI/UX Designer"
        role_type = "uiux"
    elif is_react:
        category = "React Developer"
        role_type = "frontend"
    elif is_frontend:
        category = "Frontend Developer"
        role_type = "frontend"
    elif is_webdev:
        category = "Web Developer"
        role_type = "frontend"
    elif any(k in tags_lower for k in ['react', 'nextjs', 'next.js']) and ('developer' in t_lower or 'engineer' in t_lower):
        category = "React Developer"
        role_type = "frontend"
    elif any(k in tags_lower for k in ['frontend', 'front-end']) and ('developer' in t_lower or 'engineer' in t_lower):
        category = "Frontend Developer"
        role_type = "frontend"
    else:
        return None

    # Check Seniority
    senior_patterns = [
        r'\bsenior\b', r'\bsr\.?\b', r'\blead\b', r'\bprincipal\b',
        r'\bhead\b', r'\bdirector\b', r'\bstaff\b', r'\bvp\b',
        r'\barchitect\b', r'\bmanager\b'
    ]
    is_senior = any(re.search(pat, t_lower) for pat in senior_patterns)

    # Check Junior / Entry
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

def fetch_hn_whoishiring():
    leads = []
    print("Fetching Hacker News Who is Hiring (November 2026)...")
    # Query story 50338728
    story_id = 50338728
    queries = ['react', 'frontend', 'web', 'designer', 'ui', 'ux']
    seen_ids = set()

    for q in queries:
        try:
            url = f"https://hn.algolia.com/api/v1/search?tags=comment,story_{story_id}&query={q}&hitsPerPage=50"
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode())
                for hit in data.get('hits', []):
                    c_id = hit.get('objectID')
                    if c_id in seen_ids:
                        continue
                    seen_ids.add(c_id)

                    text = hit.get('comment_text', '')
                    cleaned = clean_html(text)
                    first_line = cleaned.split('\n')[0] if cleaned else ''
                    
                    # Must be remote friendly
                    if not re.search(r'\bremote\b', cleaned, re.IGNORECASE):
                        continue

                    emails = extract_emails(cleaned)
                    
                    # Extract company name from first line pattern: "Company | Role | Location | ..."
                    parts = [p.strip() for p in first_line.split('|')]
                    company = parts[0] if parts else "HN Company"
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
                            'date': hit.get('created_at'),
                            'raw_snippet': cleaned[:250]
                        })
        except Exception as e:
            print(f"[HN query={q}] Error: {e}")
    return leads

def fetch_remoteok_all():
    leads = []
    print("Fetching RemoteOK...")
    tags = ['', 'react', 'javascript', 'ui', 'ux', 'designer', 'junior']
    seen_ids = set()

    for tag in tags:
        url = f"https://remoteok.com/api?tag={tag}" if tag else "https://remoteok.com/api"
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=12) as resp:
                data = json.loads(resp.read().decode())
                for item in data[1:]:
                    jid = item.get('id')
                    if jid in seen_ids:
                        continue
                    seen_ids.add(jid)

                    title = item.get('position', '')
                    company = item.get('company', '')
                    desc = item.get('description', '')
                    item_tags = item.get('tags', [])

                    eval_res = evaluate_job(title, company, desc, item_tags)
                    if eval_res:
                        emails = extract_emails(desc)
                        salary_min = item.get('salary_min')
                        salary_max = item.get('salary_max')
                        salary = f"${salary_min:,} - ${salary_max:,}" if salary_min and salary_max else "Not specified"
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
                            'date': item.get('date'),
                            'raw_snippet': clean_html(desc)[:250]
                        })
        except Exception as e:
            print(f"[RemoteOK tag={tag}] Error: {e}")
    return leads

def fetch_weworkremotely_all():
    leads = []
    print("Fetching We Work Remotely...")
    feeds = [
        'https://weworkremotely.com/categories/remote-front-end-programming-jobs.rss',
        'https://weworkremotely.com/categories/remote-full-stack-programming-jobs.rss',
        'https://weworkremotely.com/categories/remote-design-jobs.rss'
    ]
    seen_links = set()
    for feed_url in feeds:
        try:
            req = urllib.request.Request(feed_url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=12) as resp:
                xml_content = resp.read().decode('utf-8', errors='ignore')
                root = ET.fromstring(xml_content)
                for item in root.findall('./channel/item'):
                    link = item.findtext('link', '')
                    if link in seen_links:
                        continue
                    seen_links.add(link)

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
                            'raw_snippet': clean_html(desc)[:250]
                        })
        except Exception as e:
            print(f"[WWR] Error: {e}")
    return leads

def fetch_jobicy_all():
    leads = []
    print("Fetching Jobicy...")
    try:
        req = urllib.request.Request('https://jobicy.com/api/v2/remote-jobs?count=100', headers=HEADERS)
        with urllib.request.urlopen(req, timeout=12) as resp:
            data = json.loads(resp.read().decode())
            for item in data.get('jobs', []):
                title = item.get('jobTitle', '')
                desc = item.get('jobDescription', '')
                tags = [item.get('jobCategory', '')]
                eval_res = evaluate_job(title, item.get('companyName'), desc, tags)
                if eval_res:
                    emails = extract_emails(desc)
                    leads.append({
                        'source': 'Jobicy',
                        'title': title,
                        'company': item.get('companyName', 'Unknown'),
                        'category': eval_res['category'],
                        'role_type': eval_res['role_type'],
                        'is_senior': eval_res['is_senior'],
                        'is_junior': eval_res['is_junior'],
                        'location': item.get('jobGeo', 'Remote'),
                        'salary': item.get('annualSalaryMin', '') or 'Not specified',
                        'url': item.get('url'),
                        'apply_url': item.get('url'),
                        'emails': emails,
                        'date': item.get('pubDate'),
                        'raw_snippet': clean_html(desc)[:250]
                    })
    except Exception as e:
        print(f"[Jobicy] Error: {e}")
    return leads

def fetch_remotive_all():
    leads = []
    print("Fetching Remotive...")
    for cat_slug in ['software-dev', 'design']:
        try:
            req = urllib.request.Request(f'https://remotive.com/api/remote-jobs?category={cat_slug}&limit=50', headers=HEADERS)
            with urllib.request.urlopen(req, timeout=12) as resp:
                data = json.loads(resp.read().decode())
                for item in data.get('jobs', []):
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
                            'date': item.get('publication_date'),
                            'raw_snippet': clean_html(desc)[:250]
                        })
        except Exception as e:
            print(f"[Remotive {cat_slug}] Error: {e}")
    return leads

def fetch_himalayas_all():
    print("Scraping Himalayas...")
    leads = []
    try:
        req = urllib.request.Request('https://himalayas.app/jobs/api?limit=50', headers=HEADERS)
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode('utf-8'))
        for item in data.get('jobs', []):
            title = item.get('title', '')
            company = item.get('companyName', '') or 'Remote Company'
            desc = clean_html(item.get('description', ''))
            tags = " ".join(item.get('categories', []) or [])
            eval_res = evaluate_job(title, company, desc, tags)
            if eval_res:
                category, is_junior = eval_res
                leads.append({
                    'source': 'Himalayas',
                    'company': company,
                    'title': title,
                    'category': category,
                    'is_junior': is_junior,
                    'emails': extract_emails(desc),
                    'url': item.get('applicationLink', '') or f"https://himalayas.app/jobs/{item.get('slug', '')}",
                    'apply_url': item.get('applicationLink', '') or f"https://himalayas.app/jobs/{item.get('slug', '')}",
                    'raw_snippet': desc[:400],
                })
    except Exception as e:
        print(f"Error scraping Himalayas: {e}")
    return leads

def fetch_workingnomads_all():
    print("Scraping Working Nomads...")
    leads = []
    try:
        req = urllib.request.Request('https://www.workingnomads.com/api/exposed_jobs/', headers=HEADERS)
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode('utf-8'))
        for item in data[:60]:
            title = item.get('title', '')
            company = item.get('company_name', '') or 'Remote Company'
            desc = clean_html(item.get('description', ''))
            tags = item.get('category_name', '') or ''
            eval_res = evaluate_job(title, company, desc, tags)
            if eval_res:
                category, is_junior = eval_res
                leads.append({
                    'source': 'WorkingNomads',
                    'company': company,
                    'title': title,
                    'category': category,
                    'is_junior': is_junior,
                    'emails': extract_emails(desc),
                    'url': item.get('url', ''),
                    'apply_url': item.get('url', ''),
                    'raw_snippet': desc[:400],
                })
    except Exception as e:
        print(f"Error scraping Working Nomads: {e}")
    return leads

def score_job_against_profile(title: str, description: str, tags=None) -> int:
    """Score a job (0-100) against Joydeep's Full-Stack & AI Engineer profile."""
    text = f"{title} {description} {' '.join(tags or [])}".lower()
    core_skills = [
        "react", "next.js", "nextjs", "typescript", "javascript",
        "node.js", "nodejs", "python", "fastapi", "llm", "rag",
        "ai", "gemini", "groq", "tailwind", "figma", "ui/ux", "full-stack", "fullstack"
    ]
    hits = sum(1 for s in core_skills if s in text)
    return min(100, 35 + hits * 8)

def run():
    all_leads = []
    all_leads.extend(fetch_remoteok_all())
    all_leads.extend(fetch_weworkremotely_all())
    all_leads.extend(fetch_remotive_all())
    all_leads.extend(fetch_himalayas_all())
    all_leads.extend(fetch_workingnomads_all())

    for l in all_leads:
        l['match_score'] = score_job_against_profile(l.get('title', ''), l.get('raw_snippet', ''))
    all_leads.sort(key=lambda x: x.get('match_score', 0), reverse=True)

    print(f"\n==========================================")
    print(f"Total verified matching tech/design leads: {len(all_leads)}")

    with open('verified_leads.json', 'w', encoding='utf-8') as f:
        json.dump(all_leads, f, indent=2)

    send_leads_email_digest(all_leads)
    return all_leads

def send_leads_email_digest(leads):
    import os, smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass
    gmail_user = os.getenv("GMAIL_USER")
    gmail_pass = os.getenv("GMAIL_APP_PASSWORD")
    if not gmail_user or not gmail_pass or not leads:
        return
    top_leads = leads[:15]
    rows = ""
    for l in top_leads:
        rows += (
            f"<tr>"
            f"<td style='padding:8px;border-bottom:1px solid #eee;'><b>{l.get('company','')}</b></td>"
            f"<td style='padding:8px;border-bottom:1px solid #eee;'><a href='{l.get('apply_url') or l.get('url','#')}'>{l.get('title','')}</a></td>"
            f"<td style='padding:8px;border-bottom:1px solid #eee;'>{l.get('source','')}</td>"
            f"<td style='padding:8px;border-bottom:1px solid #eee;'><b>{l.get('match_score', 0)}%</b></td>"
            f"</tr>"
        )
    html_body = (
        f"<html><body style='font-family:Arial,sans-serif;color:#111;'>"
        f"<h2>Jim Bob's Fresh Remote Leads ({len(leads)} found)</h2>"
        f"<table style='width:100%;border-collapse:collapse;'>"
        f"<tr style='background:#f4f4f5;text-align:left;'><th style='padding:8px;'>Company</th><th style='padding:8px;'>Role</th><th style='padding:8px;'>Source</th><th style='padding:8px;'>Match</th></tr>"
        f"{rows}</table></body></html>"
    )
    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"Jim Bob: {len(leads)} Fresh Remote Leads"
    msg["From"] = gmail_user
    msg["To"] = gmail_user
    msg.attach(MIMEText(html_body, "html"))
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(gmail_user, gmail_pass)
            server.sendmail(gmail_user, gmail_user, msg.as_string())
        print(f"Sent HTML leads digest to {gmail_user}")
    except Exception as e:
        print(f"Email digest error: {e}")

if __name__ == "__main__":
    run()
