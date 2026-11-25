import json

with open('verified_leads.json', 'r', encoding='utf-8') as f:
    leads = json.load(f)

for i, l in enumerate(leads):
    if l.get('emails'):
        print(f"=== Lead #{i} ===")
        print(f"Title: {l['title']}")
        print(f"Company: {l['company']}")
        print(f"Source: {l['source']}")
        print(f"Emails: {l['emails']}")
        print(f"URL: {l['url']}")
        print(f"Text Snippet:\n{l.get('raw_snippet', '')}\n")
