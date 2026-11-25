import urllib.request
import json
import ssl

ctx = ssl._create_unverified_context()
token = '9035857763:AAEJrmBAWReDBxA_jhUyhQCfVbke7FZHaxU'
chat_id = 5691910977

text = """Here are the 3 reasons you can copy-paste for your interview answer:

1. Over-Ownership & Delegation:
"I sometimes tend to take end-to-end personal ownership of every single detail—from UI craft to deployment configs. In larger teams, this can occasionally delay delegation. I am actively working on trusting and delegating earlier to maximize team leverage."

2. Speed vs. Perfectionism (The Craft Trap):
"I care deeply about sub-second performance, clean architectural boundaries, and pixel-perfect UX. If a company prioritizes shipping dirty, throwaway prototypes over sustainable architecture, my drive for polish might initially cause friction until we explicitly align on speed-over-craft expectations."

3. Modern Stack & Product Alignment:
"My core leverage and deepest passion lie in modern, reactive web ecosystems (React 19, Next.js, TypeScript, LLM/RAG pipelines). If the role predominantly involves maintaining 10+ year legacy monolithic codebases with minimal room for modern workflows, a specialized legacy engineer would objectively be a stronger match."
"""

payload = json.dumps({'chat_id': chat_id, 'text': text}).encode('utf-8')
req = urllib.request.Request(
    f'https://api.telegram.org/bot{token}/sendMessage',
    data=payload,
    headers={'Content-Type': 'application/json'},
    method='POST'
)
with urllib.request.urlopen(req, context=ctx) as res:
    print('Telegram message sent successfully:', res.status)
