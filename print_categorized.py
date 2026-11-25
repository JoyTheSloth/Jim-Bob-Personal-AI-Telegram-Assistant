import json

with open('fresh_scanned_leads.json', 'r', encoding='utf-8') as f:
    leads = json.load(f)

print('=== 1. JUNIOR / ENTRY / ASSOCIATE WEB & REACT DEVELOPERS ===')
for l in leads:
    if l.get('is_junior'):
        print(f"* [{l['source']}] {l['title']} @ {l['company']}")
        print(f"  Category: {l['category']} | Location: {l['location']} | Salary: {l['salary']}")
        print(f"  URL: {l['url']}")
        print(f"  Emails: {l['emails']}")
        print(f"  Snippet: {l['raw_snippet'][:120]}...")
        print()

print('\n=== 2. REACT DEVELOPERS ===')
for l in leads:
    if l.get('category') == 'React Developer' and not l.get('is_junior'):
        senior_str = " (Senior)" if l.get('is_senior') else " (Mid/Open)"
        print(f"* [{l['source']}] {l['title']} @ {l['company']}{senior_str}")
        print(f"  Location: {l['location']} | Salary: {l['salary']}")
        print(f"  URL: {l['url']}")
        print(f"  Emails: {l['emails']}")
        print()

print('\n=== 3. UI/UX & PRODUCT DESIGNERS ===')
for l in leads:
    if l.get('category') == 'UI/UX Designer':
        senior_str = " (Senior/Lead)" if l.get('is_senior') else " (Mid/Open)"
        print(f"* [{l['source']}] {l['title']} @ {l['company']}{senior_str}")
        print(f"  Location: {l['location']} | Salary: {l['salary']}")
        print(f"  URL: {l['url']}")
        print(f"  Emails: {l['emails']}")
        print()

print('\n=== 4. WEB / FRONTEND DEVELOPERS ===')
for l in leads:
    if l.get('category') == 'Web Developer' and not l.get('is_junior'):
        senior_str = " (Senior)" if l.get('is_senior') else " (Mid/Open)"
        print(f"* [{l['source']}] {l['title']} @ {l['company']}{senior_str}")
        print(f"  Location: {l['location']} | Salary: {l['salary']}")
        print(f"  URL: {l['url']}")
        print(f"  Emails: {l['emails']}")
        print()
