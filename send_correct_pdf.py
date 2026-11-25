import urllib.request
import ssl
from pathlib import Path

ctx = ssl._create_unverified_context()
token = '9035857763:AAEJrmBAWReDBxA_jhUyhQCfVbke7FZHaxU'
chat_id = '5691910977'
pdf_path = Path(r'C:\Users\joyde\.gemini\antigravity\scratch\job-application-automator\Joydeep_Das_Product_Engineer_Latest.pdf')

boundary = '----WebKitFormBoundary7MA4YWxkTrZu0gW'
with open(pdf_path, 'rb') as f:
    pdf_bytes = f.read()

parts = [
    f'--{boundary}\r\nContent-Disposition: form-data; name="chat_id"\r\n\r\n{chat_id}\r\n'.encode('utf-8'),
    f'--{boundary}\r\nContent-Disposition: form-data; name="caption"\r\n\r\n✅ UPDATED & CORRECT: Joydeep Das - Product Engineer & Full-Stack AI Systems (Geetbih Tech LLP / 2gather, Value Axis Wealth, Skill Arbitrage, Resume Darzi & Job Dalal)\r\n'.encode('utf-8'),
    f'--{boundary}\r\nContent-Disposition: form-data; name="document"; filename="Joydeep_Das_Product_Engineer.pdf"\r\nContent-Type: application/pdf\r\n\r\n'.encode('utf-8'),
    pdf_bytes,
    f'\r\n--{boundary}--\r\n'.encode('utf-8')
]

payload = b''.join(parts)
req = urllib.request.Request(
    f'https://api.telegram.org/bot{token}/sendDocument',
    data=payload,
    headers={'Content-Type': f'multipart/form-data; boundary={boundary}'},
    method='POST'
)

with urllib.request.urlopen(req, context=ctx) as resp:
    print('Telegram send status:', resp.status)
