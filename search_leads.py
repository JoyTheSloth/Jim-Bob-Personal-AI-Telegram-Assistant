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
    cleanr = re.compile('<.*?>')
    return re.sub(cleanr, ' ', raw_html)

def extract_emails(text):
    if not text:
        return []
    # Find email addresses
    found = re.findall(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', text)
    cleaned = []
    ignored = ['remoteok', 'example.com', 'domain.com', 'w3.org', 'sentry.io', 'github.com', 'schema.org', 'arbeitnow.com']
    for e in found:
        e = e.strip(".,;:()<>[]\"'")
        if not any(ign in e.lower() for ign in ignored) and '.' in e.split('@')[-1]:
            cleaned.append(e)
    return list(dict.fromkeys(cleaned))

def categorize_role(title, tags, description):
    t_lower = (title or "").lower()
    desc_lower = (description or "").lower()
    tags_lower = [t.lower() for t in (tags or [])]
    full_text = f"{t_lower} {' '.join(tags_lower)}"

    # Seniority check
    senior_keywords = ['senior', 'sr.', 'lead', 'principal', 'head of', 'director', 'staff', 'vp', 'architect', 'expert', 'manager']
    is_senior = any(re.search(r'\b' + re.escape(sk) + r'\b', t_lower) for sk in senior_keywords)
    
    # Junior / Entry / Mid check
    is_junior = any(jk in full_text or jk in desc_lower[:300] for jk in ['junior', 'jr.', 'entry', 'intern', 'associate', '0-2', '1-2', '1-3', 'graduate', 'early career'])

    category = None
    role_type = None # for send_application.py ('frontend', 'uiux', 'fde')

    if any(k in t_lower for k in ['ui/ux', 'uiux', 'ux/ui', 'ui designer', 'ux designer', 'product designer', 'visual designer', 'web designer']):
        category = "UI/UX Designer"
        role_type = "uiux"
    elif any(k in t_lower for k in ['react', 'frontend', 'front-end', 'front end', 'next.js', 'vue', 'angular']):
        category = "React / Frontend Developer"
        role_type = "frontend"
    elif any(k in t_lower for k in ['web developer', 'web dev', 'wordpress', 'shopify', 'javascript developer']):
        category = "Web Developer"
        role_type = "frontend"
    elif any(k in tags_lower for k in ['react', 'frontend', 'front-end']):
        category = "React / Frontend Developer"
        role_type = "frontend"
    elif any(k in tags_lower for k in ['ui/ux', 'ui designer', 'ux designer', 'design']):
        category = "UI/UX Designer"
        role_type = "uiux"

    return category, role_type, is_senior, is_junior

def fetch_remoteok():
    leads = []
    try:
        req = urllib.request.Request('https://remoteok.com/api', headers=HEADERS)
        with urllib.request.urlopen(req, timeout=12) as resp:
            data = json.loads(resp.read().decode())
            for item in data[1:]: # skip first disclaimer
                title = item.get('position', '')
                tags = item.get('tags', [])
                desc = item.get('description', '')
                cat, rtype, is_senior, is_jr = categorize_role(title, tags, desc)
                if cat:
                    emails = extract_emails(desc)
                    leads.append({
                        'source': 'RemoteOK',
                        'title': title,
                        'company': item.get('company', 'Unknown'),
                        'category': cat,
                        'role_type': rtype,
                        'is_senior': is_senior,
                        'is_junior': is_jr,
                        'location': item.get('location', 'Remote'),
                        'salary': f"${item.get('salary_min', 0):,} - ${item.get('salary_max', 0):,}" if item.get('salary_min') else "Not specified",
                        'url': item.get('url') or item.get('apply_url'),
                        'apply_url': item.get('apply_url') or item.get('url'),
                        'emails': emails,
                        'date': item.get('date')
                    })
    except Exception as e:
        print(f"[RemoteOK] Error: {e}")
    return leads

def fetch_jobicy():
    leads = []
    try:
        req = urllib.request.Request('https://jobicy.com/api/v2/remote-jobs?count=100', headers=HEADERS)
        with urllib.request.urlopen(req, timeout=12) as resp:
            data = json.loads(resp.read().decode())
            for item in data.get('jobs', []):
                title = item.get('jobTitle', '')
                desc = item.get('jobDescription', '')
                tags = [item.get('jobCategory', '')]
                cat, rtype, is_senior, is_jr = categorize_role(title, tags, desc)
                if cat:
                    emails = extract_emails(desc)
                    leads.append({
                        'source': 'Jobicy',
                        'title': title,
                        'company': item.get('companyName', 'Unknown'),
                        'category': cat,
                        'role_type': rtype,
                        'is_senior': is_senior,
                        'is_junior': is_jr,
                        'location': item.get('jobGeo', 'Remote'),
                        'salary': item.get('annualSalaryMin', '') or "Not specified",
                        'url': item.get('url'),
                        'apply_url': item.get('url'),
                        'emails': emails,
                        'date': item.get('pubDate')
                    })
    except Exception as e:
        print(f"[Jobicy] Error: {e}")
    return leads

def fetch_remotive():
    leads = []
    for cat_slug in ['software-dev', 'design']:
        try:
            req = urllib.request.Request(f'https://remotive.com/api/remote-jobs?category={cat_slug}&limit=50', headers=HEADERS)
            with urllib.request.urlopen(req, timeout=12) as resp:
                data = json.loads(resp.read().decode())
                for item in data.get('jobs', []):
                    title = item.get('title', '')
                    desc = item.get('description', '')
                    tags = item.get('tags', [])
                    cat, rtype, is_senior, is_jr = categorize_role(title, tags, desc)
                    if cat:
                        emails = extract_emails(desc)
                        leads.append({
                            'source': 'Remotive',
                            'title': title,
                            'company': item.get('company_name', 'Unknown'),
                            'category': cat,
                            'role_type': rtype,
                            'is_senior': is_senior,
                            'is_junior': is_jr,
                            'location': item.get('candidate_required_location', 'Remote'),
                            'salary': item.get('salary', 'Not specified'),
                            'url': item.get('url'),
                            'apply_url': item.get('url'),
                            'emails': emails,
                            'date': item.get('publication_date')
                        })
        except Exception as e:
            print(f"[Remotive {cat_slug}] Error: {e}")
    return leads

def fetch_arbeitnow():
    leads = []
    try:
        req = urllib.request.Request('https://www.arbeitnow.com/api/job-board-api', headers=HEADERS)
        with urllib.request.urlopen(req, timeout=12) as resp:
            data = json.loads(resp.read().decode())
            for item in data.get('data', []):
                title = item.get('title', '')
                desc = item.get('description', '')
                tags = item.get('tags', [])
                if not item.get('remote', False):
                    continue
                cat, rtype, is_senior, is_jr = categorize_role(title, tags, desc)
                if cat:
                    emails = extract_emails(desc)
                    leads.append({
                        'source': 'Arbeitnow',
                        'title': title,
                        'company': item.get('company_name', 'Unknown'),
                        'category': cat,
                        'role_type': rtype,
                        'is_senior': is_senior,
                        'is_junior': is_jr,
                        'location': item.get('location', 'Remote'),
                        'salary': "Not specified",
                        'url': item.get('url'),
                        'apply_url': item.get('url'),
                        'emails': emails,
                        'date': datetime.fromtimestamp(item.get('created_at', 0)).strftime("%Y-%m-%d") if item.get('created_at') else None
                    })
    except Exception as e:
        print(f"[Arbeitnow] Error: {e}")
    return leads

def fetch_weworkremotely():
    leads = []
    feeds = [
        'https://weworkremotely.com/categories/remote-front-end-programming-jobs.rss',
        'https://weworkremotely.com/categories/remote-design-jobs.rss'
    ]
    for feed_url in feeds:
        try:
            req = urllib.request.Request(feed_url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=12) as resp:
                xml_content = resp.read().decode('utf-8', errors='ignore')
                root = ET.fromstring(xml_content)
                for item in root.findall('./channel/item'):
                    title = item.findtext('title', '')
                    link = item.findtext('link', '')
                    desc = item.findtext('description', '')
                    pub_date = item.findtext('pubDate', '')
                    
                    # Split title format: "Company: Job Title"
                    company = "Unknown"
                    job_title = title
                    if ':' in title:
                        parts = title.split(':', 1)
                        company = parts[0].strip()
                        job_title = parts[1].strip()

                    cat, rtype, is_senior, is_jr = categorize_role(job_title, [], desc)
                    if cat:
                        emails = extract_emails(desc)
                        leads.append({
                            'source': 'WeWorkRemotely',
                            'title': job_title,
                            'company': company,
                            'category': cat,
                            'role_type': rtype,
                            'is_senior': is_senior,
                            'is_junior': is_jr,
                            'location': 'Remote',
                            'salary': "Not specified",
                            'url': link,
                            'apply_url': link,
                            'emails': emails,
                            'date': pub_date
                        })
        except Exception as e:
            print(f"[WWR] Error: {e}")
    return leads

def run():
    all_leads = []
    print("Fetching from RemoteOK...")
    all_leads.extend(fetch_remoteok())
    print("Fetching from Jobicy...")
    all_leads.extend(fetch_jobicy())
    print("Fetching from Remotive...")
    all_leads.extend(fetch_remotive())
    print("Fetching from Arbeitnow...")
    all_leads.extend(fetch_arbeitnow())
    print("Fetching from WeWorkRemotely RSS...")
    all_leads.extend(fetch_weworkremotely())

    print(f"\nTotal fetched matching leads across categories: {len(all_leads)}")

    # Group by category and junior/mid vs senior
    filtered_leads = [l for l in all_leads if not l['is_senior']]
    print(f"Junior/Mid/Entry leads (excluding Senior/Lead): {len(filtered_leads)}")

    with open('fresh_leads.json', 'w', encoding='utf-8') as f:
        json.dump(all_leads, f, indent=2)

    return all_leads

if __name__ == "__main__":
    run()
