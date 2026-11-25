import json

with open('fresh_leads.json', 'r', encoding='utf-8') as f:
    leads = json.load(f)

non_senior = [l for l in leads if not l['is_senior']]

print(f"=== FRESH LEADS: JUNIOR / MID / GENERAL ({len(non_senior)} Found) ===")
for i, l in enumerate(non_senior, 1):
    level = "JUNIOR/ENTRY" if l['is_junior'] else "MID/OPEN"
    print(f"\n[{i}] [{level}] [{l['category']}] {l['title']}")
    print(f"    Company:  {l['company']} ({l['source']})")
    print(f"    Location: {l['location']}")
    print(f"    Salary:   {l['salary']}")
    print(f"    URL:      {l['url']}")
    if l['emails']:
        print(f"    Direct Contact Emails: {', '.join(l['emails'])}")

print("\n" + "="*60)
print(f"=== SENIOR / LEAD OPENINGS ({len(leads) - len(non_senior)} Found) ===")
senior_leads = [l for l in leads if l['is_senior']]
for i, l in enumerate(senior_leads[:10], 1):
    print(f"[{i}] [{l['category']}] {l['title']} at {l['company']} ({l['source']}) -> {l['url']}")
