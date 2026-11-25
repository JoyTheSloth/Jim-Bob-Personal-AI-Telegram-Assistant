import urllib.request
import json
import re

headers = {'User-Agent': 'Mozilla/5.0'}

# 1. HN items
for hn_id in [50384008, 50357360, 50370710]:
    url = f'https://hn.algolia.com/api/v1/items/{hn_id}'
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=10) as r:
        item = json.loads(r.read().decode())
        print(f"=== HN {hn_id} ===")
        text = item.get('text', '')
        text = re.sub(r'<p>', '\n\n', text)
        text = re.sub(r'<.*?>', '', text)
        text = text.replace('&#x2F;', '/').replace('&amp;', '&').replace('&#x27;', "'")
        print(text)
        print('\n' + '-'*60)

# 2. RemoteOK Leap Tools
try:
    with open('verified_leads.json', 'r', encoding='utf-8') as f:
        leads = json.load(f)
    for l in leads:
        if 'leap' in l.get('company', '').lower():
            print("=== LEAP TOOLS ===")
            print(l['title'], l['company'], l['emails'])
            print(l.get('raw_snippet'))
            break
except Exception as e:
    print(e)
