import urllib.request
import json
import ssl

ctx = ssl._create_unverified_context()
token = '9035857763:AAEJrmBAWReDBxA_jhUyhQCfVbke7FZHaxU'
chat_id = 5691910977

text = """📋 3 Authentic Weaknesses for Interview (Ready to Copy):

1. Saying 'Yes' Too Quickly (Over-Committing)
"Early in my career, I found it difficult to say no to new feature requests or architectural experiments, which occasionally led to stretched work hours and context-switching. To manage this, I now rigorously evaluate scope, communicate trade-offs upfront, and prioritize tasks using clear milestone roadmaps."

2. Difficulty Letting Go of Incomplete Solutions
"I tend to stay hooked on debugging obscure edge cases until they are 100% resolved. While thorough, I realized it can sometimes delay initial feedback loops. I have trained myself to set explicit timeboxes (e.g., 45 minutes) before stepping back, asking for peer input, or finding a cleaner workaround."

3. Reluctance to Share Work Before It Feels 'Polished'
"Coming from a strong UI/UX and product background, I instinctively dislike showing raw, unstyled mockups or half-baked flows. However, I’ve learned that early alignment beats late perfection, so I now actively share rough wireframes and early prototypes to gather fast stakeholder feedback."
"""

payload = json.dumps({'chat_id': chat_id, 'text': text}).encode('utf-8')
req = urllib.request.Request(
    f'https://api.telegram.org/bot{token}/sendMessage',
    data=payload,
    headers={'Content-Type': 'application/json'},
    method='POST'
)
with urllib.request.urlopen(req, context=ctx) as res:
    print('Telegram message sent:', res.status)
