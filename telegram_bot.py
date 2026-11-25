import os
import re
import ssl
import json
import asyncio
import logging
import html as html_lib
import urllib.request
from pathlib import Path
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    KeyboardButton,
    BotCommand,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)
import send_application
import tracker
import fetch_all_sources
import career_consciousness
import jim_bob_brain

# Load .env variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "9035857763:AAEJrmBAWReDBxA_jhUyhQCfVbke7FZHaxU")
ALLOWED_USER_ID = int(os.getenv("TELEGRAM_ALLOWED_USER_ID", "5691910977"))

# Lazy EasyOCR reader instance
_ocr_reader = None

def get_ocr_reader():
    global _ocr_reader
    if _ocr_reader is None:
        print("Initializing EasyOCR reader on demand...")
        ssl._create_default_https_context = ssl._create_unverified_context
        import easyocr
        _ocr_reader = easyocr.Reader(['en'], gpu=False)
        print("EasyOCR reader ready!")
    return _ocr_reader

# Init DB
tracker.init_db()

# Pending drafts stored per user
DRAFTS = {}

# User leads browser state cache
LEADS_CACHE = {}

# Persistent Menu Keyboard visible under chat input
MAIN_MENU_KEYBOARD = ReplyKeyboardMarkup(
    [
        [KeyboardButton("📬 Fresh Leads"), KeyboardButton("🔄 Fetch New Jobs")],
        [KeyboardButton("🐣 Junior Openings"), KeyboardButton("⚛️ React Jobs")],
        [KeyboardButton("🎨 UI/UX Jobs"), KeyboardButton("📊 Tracker Stats")],
        [KeyboardButton("📋 Recent Applications"), KeyboardButton("❓ Help / Commands")],
        [KeyboardButton("🔽 Minimize Menu")]
    ],
    resize_keyboard=True,
    is_persistent=False
)

async def post_init(application):
    commands = [
        BotCommand("leads", "Browse fresh remote jobs & 1-tap pitch"),
        BotCommand("fetch", "Live scrape latest jobs from 5 remote boards"),
        BotCommand("apply", "Draft application: /apply <email> [company] [role]"),
        BotCommand("check", "Check if you already applied to a company/email"),
        BotCommand("stats", "Application pipeline metrics"),
        BotCommand("list", "Recent applications log"),
        BotCommand("company", "Update company name on active draft"),
        BotCommand("subject", "Update subject line on active draft"),
        BotCommand("menu", "Show command menu keyboard"),
        BotCommand("minimize", "Minimize bottom keyboard"),
        BotCommand("help", "Command directory and usage guide"),
        BotCommand("do", "Tell Jim Bob to do ANYTHING: /do push flatzy, /do git status"),
        BotCommand("mind", "Inspect Jim Bob's inner thoughts, state of mind, & memory"),
        BotCommand("git", "Git shortcut: /git status flatzy | /git push flatzy 'msg'"),
        BotCommand("deploy", "Trigger Vercel deploy: /deploy flatzy"),
        BotCommand("update", "Draft client update: /update Flatzy client John"),
        BotCommand("shell", "Run a shell command: /shell dir C:\\Projects"),
    ]
    await application.bot.set_my_commands(commands)
    print("Registered native Telegram bot commands menu.")

def get_applied_records():
    db_path = tracker.DB_PATH
    if not db_path.exists():
        return set(), set()
    import sqlite3
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT recipient_email, company FROM applications")
    rows = c.fetchall()
    conn.close()
    emails = {r[0].lower().strip() for r in rows if r[0]}
    companies = {r[1].lower().strip() for r in rows if r[1]}
    return emails, companies

def load_filtered_leads(category_filter: str = "email"):
    leads_path = Path(__file__).parent / "verified_leads.json"
    if not leads_path.exists():
        return []

    try:
        with open(leads_path, "r", encoding="utf-8") as f:
            leads = json.load(f)
    except Exception as e:
        print(f"Error loading leads: {e}")
        return []

    applied_emails, applied_companies = get_applied_records()

    def is_seeker(l):
        text = (l.get('raw_snippet', '') + ' ' + l.get('title', '')).lower()
        if 'willing to relocate' in text or 'résumé' in text or 'resume/cv' in text or 'seeking a' in text:
            return True
        return False

    seen = set()
    results = []

    for l in leads:
        if is_seeker(l):
            continue

        company = (l.get('company') or '').strip()
        title = (l.get('title') or '').strip()
        cat = (l.get('category') or '').strip()
        key = (company.lower(), title.lower())
        if key in seen:
            continue
        seen.add(key)

        emails = l.get('emails', [])
        fresh_emails = [e for e in emails if e.lower().strip() not in applied_emails]
        is_applied = (company.lower() in applied_companies) or any(e.lower().strip() in applied_emails for e in emails)

        l_copy = dict(l)
        l_copy['fresh_emails'] = fresh_emails
        l_copy['is_applied'] = is_applied

        if category_filter in ["email", "direct"]:
            if fresh_emails and not is_applied:
                results.append(l_copy)
        elif category_filter in ["junior", "entry"]:
            if l.get('is_junior') and not is_applied:
                results.append(l_copy)
        elif category_filter in ["react", "frontend"]:
            if (cat in ['React Developer', 'Frontend Developer'] or 'react' in title.lower()) and not is_applied:
                results.append(l_copy)
        elif category_filter in ["uiux", "design"]:
            if (cat == 'UI/UX Designer' or any(k in title.lower() for k in ['ui/ux', 'design', 'figma'])) and not is_applied:
                results.append(l_copy)
        elif category_filter == "all":
            if not is_applied:
                results.append(l_copy)
        else:
            if not is_applied:
                results.append(l_copy)

    return results

def extract_job_info(text: str):
    cleaned = re.sub(r'\s*@\s*', '@', text)
    cleaned = re.sub(r'@([a-zA-Z0-9_-]+)\s*\.\s*(com|org|net|io|in|co|ai|tech|dev)\b', r'@\1.\2', cleaned)
    cleaned = re.sub(r'@([a-zA-Z0-9_-]+)(com|org|net|io|in|co|ai|tech|dev)\b', r'@\1.\2', cleaned)

    emails = re.findall(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', cleaned)
    to_email = emails[0] if emails else None

    lower = text.lower()
    if any(k in lower for k in ["hr", "human resource", "talent acquisition", "recruiter", "talent sourcer", "people operations", "recursos humanos", "ressources humaines", "personalwesen", "reclutamiento", "recrutement", "मानव संसाधन"]):
        role = "hr"
        role_title = "Talent Acquisition & Creator Sourcing Associate"
    elif any(k in lower for k in ["ai trainer", "llm trainer", "data annotator", "ai evaluation", "prompt engineer", "ai tutor"]):
        role = "ai"
        role_title = "AI Trainer & LLM Evaluation Specialist"
    elif any(k in lower for k in ["sales", "content strategist", "marketing", "growth lead", "digital marketing", "influencer"]):
        role = "sales"
        role_title = "Content Strategist & Growth Marketer"
    elif any(k in lower for k in ["ui/ux", "uiux", "uvux", "product designer", "ui designer", "ux designer", "web designer", "figma"]):
        role = "uiux"
        role_title = "UI/UX Designer & Product Designer"
    elif any(k in lower for k in ["react", "frontend", "front-end", "web dev", "front end", "next.js", "tailwind"]):
        role = "frontend"
        role_title = "Frontend Developer (React / TypeScript)"
    else:
        role = "fde"
        role_title = "Forward Deployed Engineer / Full-Stack Developer"

    company_match = re.search(r'(?:at|company:?|for)\s+([A-Z][A-Za-z0-9_\-\.\s]{2,20})', text)
    if company_match:
        company = company_match.group(1).strip()
    elif to_email:
        domain = to_email.split('@')[-1].split('.')[0]
        company = domain.capitalize() if domain not in ['gmail', 'yahoo', 'hotmail', 'outlook'] else "your team"
    else:
        company = "your team"

    return to_email, role, role_title, company

def generate_email_content(role: str, role_title: str, company: str, recipient_name: str = "", job_ref: str = ""):
    first_name = recipient_name.strip() if recipient_name else ""
    salutation = f"Hi {first_name}," if first_name else f"Hi {company} Team,"
    job_spec = f"for {job_ref}" if job_ref else f"for {role_title}"
    github_link = "https://github.com/JoyTheSloth"
    portfolio_link = "https://joydeepdas-portfolio.vercel.app"
    linkedin_link = "https://linkedin.com/in/joydeep-das-78123522a"

    if role == "uiux":
        subject = f"Product Designer (Figma / Web Systems) — {company}"
        plain_body = f"""{salutation}

Hope your week is going well!

I saw your opening {job_spec} at {company}. Given your team's focus on scalable digital experiences and design systems, I wanted to reach out directly.

A quick snapshot of my background:
• Stack: Figma, Design Systems, Typography/Token Scales, User Research, UI/UX Prototyping.
• Impact: Designed Pandalé Kolkata from scratch—driving 7,000+ unique visitors and 31,000+ views in week 1 with an intuitive mobile-first interface.
• Proof: Live production UX for 2GatherApp (Google Play) and interactive Figma design systems: {portfolio_link}.

Resume: Joydeep_Das_UIUX_CV.pdf (attached)
Portfolio: {portfolio_link}

If you feel my profile is a solid match, would you be open to submitting an internal referral or chatting for 10 minutes?

Best regards,
Joydeep Das
UI/UX & Product Designer
Phone: +91-7085917058
Portfolio: {portfolio_link} | LinkedIn: {linkedin_link}
"""
        html_body = f"""<!DOCTYPE html>
<html>
<body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; font-size: 15px; line-height: 1.65; color: #1e293b; max-width: 600px; margin: 0 auto; padding: 20px 0;">
  <p>{salutation}</p>
  <p>Hope your week is going well!</p>
  <p>I saw your opening {job_spec} at <strong>{company}</strong>. Given your team's focus on scalable digital experiences and design systems, I wanted to reach out directly.</p>
  <p style="margin-bottom: 6px;"><strong>A quick snapshot of my background:</strong></p>
  <ul style="padding-left: 20px; margin-top: 0; margin-bottom: 18px;">
    <li style="margin-bottom: 6px;"><strong>Stack:</strong> Figma, Design Systems, Typography/Token Scales, User Research, UI/UX Prototyping.</li>
    <li style="margin-bottom: 6px;"><strong>Impact:</strong> Designed Pandalé Kolkata from scratch—driving 7,000+ unique visitors and 31,000+ views in week 1 with an intuitive mobile-first interface.</li>
    <li style="margin-bottom: 6px;"><strong>Proof:</strong> Live production UX for 2GatherApp (Google Play) and interactive Figma systems on my <a href="{portfolio_link}" style="color: #2563eb; text-decoration: none;">Portfolio</a>.</li>
  </ul>
  <p style="margin: 12px 0 18px 0; font-size: 14px;">
    📄 <strong>Resume:</strong> Joydeep_Das_UIUX_CV.pdf (attached)<br>
    🎨 <strong>Portfolio:</strong> <a href="{portfolio_link}" style="color: #2563eb; text-decoration: none;">{portfolio_link}</a><br>
    💼 <strong>LinkedIn:</strong> <a href="{linkedin_link}" style="color: #2563eb; text-decoration: none;">{linkedin_link}</a>
  </p>
  <p>If you feel my profile is a solid match, would you be open to submitting an internal referral or chatting for 10 minutes?</p>
  <div style="margin-top: 24px; padding-top: 16px; border-top: 1px solid #e2e8f0; font-size: 14px; color: #475569;">
    <p style="margin: 0; font-weight: 600; color: #0f172a; font-size: 15px;">Joydeep Das</p>
    <p style="margin: 3px 0; color: #64748b;">UI/UX &amp; Product Designer</p>
    <p style="margin: 3px 0;">📞 +91-7085917058 &bull; ✉️ <a href="mailto:joy.thesloth@gmail.com" style="color: #2563eb; text-decoration: none;">joy.thesloth@gmail.com</a></p>
  </div>
</body>
</html>
"""
    elif role == "frontend":
        subject = f"Next.js dev who cut load times 30% | {company}"
        plain_body = f"""{salutation}

Hope your week is going well!

I saw your opening {job_spec} at {company}. Given your team's focus on scalable user experience and high-performance frontends, I wanted to reach out directly.

A quick snapshot of my background:
• Stack: React, Next.js (App Router, SSR), TypeScript, Tailwind CSS.
• Impact: Cut initial load times by ~30% and improved Core Web Vitals via code splitting and asset optimization.
• Proof: Clean architecture and live production demos on GitHub: {github_link}.

Resume: Joydeep_Das_Frontend_CV.pdf (attached)
Portfolio: {portfolio_link}

If you feel my profile is a solid match, would you be open to submitting an internal referral or chatting for 10 minutes?

Best regards,
Joydeep Das
Frontend Engineer
Phone: +91-7085917058
Portfolio: {portfolio_link} | GitHub: {github_link} | LinkedIn: {linkedin_link}
"""
        html_body = f"""<!DOCTYPE html>
<html>
<body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; font-size: 15px; line-height: 1.65; color: #1e293b; max-width: 600px; margin: 0 auto; padding: 20px 0;">
  <p>{salutation}</p>
  <p>Hope your week is going well!</p>
  <p>I saw your opening {job_spec} at <strong>{company}</strong>. Given your team's focus on scalable user experience and high-performance frontends, I wanted to reach out directly.</p>
  <p style="margin-bottom: 6px;"><strong>A quick snapshot of my background:</strong></p>
  <ul style="padding-left: 20px; margin-top: 0; margin-bottom: 18px;">
    <li style="margin-bottom: 6px;"><strong>Stack:</strong> React, Next.js (App Router, SSR), TypeScript, Tailwind CSS.</li>
    <li style="margin-bottom: 6px;"><strong>Impact:</strong> Cut initial load times by ~30% and improved Core Web Vitals via code splitting and asset optimization.</li>
    <li style="margin-bottom: 6px;"><strong>Proof:</strong> Clean architecture and live production demos on <a href="{github_link}" style="color: #2563eb; text-decoration: none;">GitHub</a>.</li>
  </ul>
  <p style="margin: 12px 0 18px 0; font-size: 14px;">
    📄 <strong>Resume:</strong> Joydeep_Das_Frontend_CV.pdf (attached)<br>
    🌐 <strong>Portfolio:</strong> <a href="{portfolio_link}" style="color: #2563eb; text-decoration: none;">{portfolio_link}</a><br>
    💻 <strong>GitHub:</strong> <a href="{github_link}" style="color: #2563eb; text-decoration: none;">{github_link}</a>
  </p>
  <p>If you feel my profile is a solid match, would you be open to submitting an internal referral or chatting for 10 minutes?</p>
  <div style="margin-top: 24px; padding-top: 16px; border-top: 1px solid #e2e8f0; font-size: 14px; color: #475569;">
    <p style="margin: 0; font-weight: 600; color: #0f172a; font-size: 15px;">Joydeep Das</p>
    <p style="margin: 3px 0; color: #64748b;">Frontend Engineer</p>
    <p style="margin: 3px 0;">📞 +91-7085917058 &bull; ✉️ <a href="mailto:joy.thesloth@gmail.com" style="color: #2563eb; text-decoration: none;">joy.thesloth@gmail.com</a></p>
  </div>
</body>
</html>
"""
    elif role == "hr":
        subject = f"Talent Acquisition & Creator Sourcing — Joydeep Das ({company})"
        plain_body = f"""{salutation}

Hope you're having a productive week!

I saw your talent acquisition and hiring needs at {company}. Having recruited, screened, and coordinated 60+ creators and candidates at GEETBIH Labs, I wanted to reach out directly.

A quick snapshot of my experience:
• Sourcing & Outreach: Hands-on experience identifying, qualifying, and engaging technical and creator talent.
• Process & Pipeline: Managed end-to-end applicant pipelines, candidate onboarding, and CRM tracking.
• Tech Fluency: CSE background that makes evaluating technical profiles and engineering stacks second-nature.

Resume: Joydeep_Das_Resume_HR.pdf (attached)
LinkedIn: {linkedin_link}

Would you be open to a brief 10-minute conversation to explore how I could support hiring for your team?

Best regards,
Joydeep Das
Phone: +91-7085917058 | joy.thesloth@gmail.com
"""
        html_body = f"""<!DOCTYPE html>
<html>
<body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; font-size: 15px; line-height: 1.65; color: #1e293b; max-width: 600px; margin: 0 auto; padding: 20px 0;">
  <p>{salutation}</p>
  <p>Hope you're having a productive week!</p>
  <p>I saw your talent acquisition and hiring needs at <strong>{company}</strong>. Having recruited, screened, and coordinated 60+ creators and candidates at GEETBIH Labs, I wanted to reach out directly.</p>
  <p style="margin-bottom: 6px;"><strong>A quick snapshot of my experience:</strong></p>
  <ul style="padding-left: 20px; margin-top: 0; margin-bottom: 18px;">
    <li style="margin-bottom: 6px;"><strong>Sourcing &amp; Outreach:</strong> Hands-on experience identifying, qualifying, and engaging technical and creator talent.</li>
    <li style="margin-bottom: 6px;"><strong>Process &amp; Pipeline:</strong> Managed end-to-end applicant pipelines, candidate onboarding, and CRM tracking.</li>
    <li style="margin-bottom: 6px;"><strong>Tech Fluency:</strong> CSE background that makes evaluating technical profiles and engineering stacks second-nature.</li>
  </ul>
  <p style="margin: 12px 0 18px 0; font-size: 14px;">
    📄 <strong>Resume:</strong> Joydeep_Das_Resume_HR.pdf (attached)<br>
    💼 <strong>LinkedIn:</strong> <a href="{linkedin_link}" style="color: #2563eb; text-decoration: none;">{linkedin_link}</a>
  </p>
  <p>Would you be open to a brief 10-minute conversation to explore how I could support hiring for your team?</p>
  <div style="margin-top: 24px; padding-top: 16px; border-top: 1px solid #e2e8f0; font-size: 14px; color: #475569;">
    <p style="margin: 0; font-weight: 600; color: #0f172a; font-size: 15px;">Joydeep Das</p>
    <p style="margin: 3px 0; color: #64748b;">Talent Acquisition &amp; People Operations</p>
    <p style="margin: 3px 0;">📞 +91-7085917058 &bull; ✉️ <a href="mailto:joy.thesloth@gmail.com" style="color: #2563eb; text-decoration: none;">joy.thesloth@gmail.com</a></p>
  </div>
</body>
</html>
"""
    elif role == "ai":
        subject = f"AI Trainer & LLM Evaluation Specialist — Joydeep Das ({company})"
        plain_body = f"""{salutation}

Hope your week is going well!

I noticed {company}'s work in LLM evaluation and AI model fine-tuning. As an engineer who builds, audits, and red-teams LLM systems, I wanted to connect directly.

A quick snapshot of my background:
• LLM Evaluation: Ranked #62 nationally at India Innovates 2026 for MediRAG-Eval (measuring faithfulness, groundedness, and context recall).
• Prompt & Schema Engineering: Structured multi-turn workflows with strict JSON schema guardrails preventing hallucinations.
• Hands-on AI Deployment: Shipped 6+ live AI applications using Google Gemini, Groq (Llama 3), and LangChain.

Resume: Joydeep_Das_AI.pdf (attached)
Portfolio: {portfolio_link} | GitHub: {github_link}

Would you be open to a 10-minute chat regarding how I can contribute to model alignment and evaluation for {company}?

Best regards,
Joydeep Das
Phone: +91-7085917058 | joy.thesloth@gmail.com
"""
        html_body = f"""<!DOCTYPE html>
<html>
<body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; font-size: 15px; line-height: 1.65; color: #1e293b; max-width: 600px; margin: 0 auto; padding: 20px 0;">
  <p>{salutation}</p>
  <p>Hope your week is going well!</p>
  <p>I noticed <strong>{company}</strong>'s work in LLM evaluation and AI model fine-tuning. As an engineer who builds, audits, and red-teams LLM systems, I wanted to connect directly.</p>
  <p style="margin-bottom: 6px;"><strong>A quick snapshot of my background:</strong></p>
  <ul style="padding-left: 20px; margin-top: 0; margin-bottom: 18px;">
    <li style="margin-bottom: 6px;"><strong>LLM Evaluation:</strong> Ranked #62 nationally at India Innovates 2026 for MediRAG-Eval (measuring faithfulness, groundedness, and context recall).</li>
    <li style="margin-bottom: 6px;"><strong>Prompt &amp; Schema Engineering:</strong> Structured multi-turn workflows with strict JSON schema guardrails preventing hallucinations.</li>
    <li style="margin-bottom: 6px;"><strong>Hands-on AI Deployment:</strong> Shipped 6+ live AI applications using Google Gemini, Groq (Llama 3), and LangChain.</li>
  </ul>
  <p style="margin: 12px 0 18px 0; font-size: 14px;">
    📄 <strong>Resume:</strong> Joydeep_Das_AI.pdf (attached)<br>
    🌐 <strong>Portfolio:</strong> <a href="{portfolio_link}" style="color: #2563eb; text-decoration: none;">{portfolio_link}</a><br>
    💻 <strong>GitHub:</strong> <a href="{github_link}" style="color: #2563eb; text-decoration: none;">{github_link}</a>
  </p>
  <p>Would you be open to a 10-minute chat regarding how I can contribute to model alignment and evaluation for {company}?</p>
  <div style="margin-top: 24px; padding-top: 16px; border-top: 1px solid #e2e8f0; font-size: 14px; color: #475569;">
    <p style="margin: 0; font-weight: 600; color: #0f172a; font-size: 15px;">Joydeep Das</p>
    <p style="margin: 3px 0; color: #64748b;">AI Trainer &amp; LLM Evaluation Specialist</p>
    <p style="margin: 3px 0;">📞 +91-7085917058 &bull; ✉️ <a href="mailto:joy.thesloth@gmail.com" style="color: #2563eb; text-decoration: none;">joy.thesloth@gmail.com</a></p>
  </div>
</body>
</html>
"""
    elif role == "sales":
        subject = f"Content Strategist & Growth — Joydeep Das ({company})"
        plain_body = f"""{salutation}

Hope your week is going well!

I saw your growth and content needs at {company}. Having grown digital accounts to 10M+ organic views from scratch, I wanted to reach out.

A quick snapshot of my track record:
• Audience Growth: Scaled @jethalal.das from zero to 10M+ total views and 2,000+ followers through engaging storytelling.
• Conversion & Copy: Led marketing creative campaigns for 2GatherApp driving thousands of mobile app installs.
• Analytics-Driven: Combine technical engineering instincts with rapid content experimentation.

Resume: ContenNSales.pdf (attached)
LinkedIn: {linkedin_link}

Would you be open to a quick 10-minute conversation on how I can support audience acquisition at {company}?

Best regards,
Joydeep Das
Phone: +91-7085917058 | joy.thesloth@gmail.com
"""
        html_body = f"""<!DOCTYPE html>
<html>
<body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; font-size: 15px; line-height: 1.65; color: #1e293b; max-width: 600px; margin: 0 auto; padding: 20px 0;">
  <p>{salutation}</p>
  <p>Hope your week is going well!</p>
  <p>I saw your growth and content needs at <strong>{company}</strong>. Having grown digital accounts to 10M+ organic views from scratch, I wanted to reach out.</p>
  <p style="margin-bottom: 6px;"><strong>A quick snapshot of my track record:</strong></p>
  <ul style="padding-left: 20px; margin-top: 0; margin-bottom: 18px;">
    <li style="margin-bottom: 6px;"><strong>Audience Growth:</strong> Scaled @jethalal.das from zero to 10M+ total views and 2,000+ followers through engaging storytelling.</li>
    <li style="margin-bottom: 6px;"><strong>Conversion &amp; Copy:</strong> Led marketing creative campaigns for 2GatherApp driving thousands of mobile app installs.</li>
    <li style="margin-bottom: 6px;"><strong>Analytics-Driven:</strong> Combine technical engineering instincts with rapid content experimentation.</li>
  </ul>
  <p style="margin: 12px 0 18px 0; font-size: 14px;">
    📄 <strong>Resume:</strong> ContenNSales.pdf (attached)<br>
    💼 <strong>LinkedIn:</strong> <a href="{linkedin_link}" style="color: #2563eb; text-decoration: none;">{linkedin_link}</a>
  </p>
  <p>Would you be open to a quick 10-minute conversation on how I can support audience acquisition at {company}?</p>
  <div style="margin-top: 24px; padding-top: 16px; border-top: 1px solid #e2e8f0; font-size: 14px; color: #475569;">
    <p style="margin: 0; font-weight: 600; color: #0f172a; font-size: 15px;">Joydeep Das</p>
    <p style="margin: 3px 0; color: #64748b;">Content Strategist &amp; Growth</p>
    <p style="margin: 3px 0;">📞 +91-7085917058 &bull; ✉️ <a href="mailto:joy.thesloth@gmail.com" style="color: #2563eb; text-decoration: none;">joy.thesloth@gmail.com</a></p>
  </div>
</body>
</html>
"""
    else:  # FDE / Full-Stack
        subject = f"Candidate: Full-Stack / FDE ({company}) — Joydeep Das"
        plain_body = f"""{salutation}

Hope your week is going well!

I saw your opening {job_spec} at {company}. Given your team's focus on rapid customer-facing delivery and robust AI systems, I wanted to reach out directly.

A quick snapshot of my background:
• Stack: Python (FastAPI), React, Next.js, TypeScript, GenAI (RAG, Gemini, Groq).
• Impact: Built and deployed 6+ production apps; co-built MediRAG-Eval (Rank 62 nationally in India Innovates Hackathon).
• Proof: Production deployments and live systems on GitHub: {github_link}.

Resume: Joydeep_Das_FDE_Resume.pdf (attached)
Portfolio: {portfolio_link}

If you feel my profile is a solid match, would you be open to submitting an internal referral or chatting for 10 minutes?

Best regards,
Joydeep Das
Full-Stack / Forward Deployed Engineer
Phone: +91-7085917058
Portfolio: {portfolio_link} | GitHub: {github_link} | LinkedIn: {linkedin_link}
"""
        html_body = f"""<!DOCTYPE html>
<html>
<body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; font-size: 15px; line-height: 1.65; color: #1e293b; max-width: 600px; margin: 0 auto; padding: 20px 0;">
  <p>{salutation}</p>
  <p>Hope your week is going well!</p>
  <p>I saw your opening {job_spec} at <strong>{company}</strong>. Given your team's focus on rapid customer-facing delivery and robust AI systems, I wanted to reach out directly.</p>
  <p style="margin-bottom: 6px;"><strong>A quick snapshot of my background:</strong></p>
  <ul style="padding-left: 20px; margin-top: 0; margin-bottom: 18px;">
    <li style="margin-bottom: 6px;"><strong>Stack:</strong> Python (FastAPI), React, Next.js, TypeScript, GenAI (RAG, Gemini, Groq).</li>
    <li style="margin-bottom: 6px;"><strong>Impact:</strong> Built and deployed 6+ production apps; co-built MediRAG-Eval (Rank 62 nationally in India Innovates Hackathon).</li>
    <li style="margin-bottom: 6px;"><strong>Proof:</strong> Production deployments and live systems on <a href="{github_link}" style="color: #2563eb; text-decoration: none;">GitHub</a>.</li>
  </ul>
  <p style="margin: 12px 0 18px 0; font-size: 14px;">
    📄 <strong>Resume:</strong> Joydeep_Das_FDE_Resume.pdf (attached)<br>
    🌐 <strong>Portfolio:</strong> <a href="{portfolio_link}" style="color: #2563eb; text-decoration: none;">{portfolio_link}</a><br>
    💻 <strong>GitHub:</strong> <a href="{github_link}" style="color: #2563eb; text-decoration: none;">{github_link}</a>
  </p>
  <p>If you feel my profile is a solid match, would you be open to submitting an internal referral or chatting for 10 minutes?</p>
  <div style="margin-top: 24px; padding-top: 16px; border-top: 1px solid #e2e8f0; font-size: 14px; color: #475569;">
    <p style="margin: 0; font-weight: 600; color: #0f172a; font-size: 15px;">Joydeep Das</p>
    <p style="margin: 3px 0; color: #64748b;">Full-Stack / Forward Deployed Engineer</p>
    <p style="margin: 3px 0;">📞 +91-7085917058 &bull; ✉️ <a href="mailto:joy.thesloth@gmail.com" style="color: #2563eb; text-decoration: none;">joy.thesloth@gmail.com</a></p>
  </div>
</body>
</html>
"""

    return subject, plain_body, html_body

def render_draft_preview(draft: dict) -> tuple[str, InlineKeyboardMarkup]:
    role = draft["role"]
    filename_map = {
        "uiux": "Joydeep_Das_Full_Stack_AI_Engineer_Resume.pdf",
        "frontend": "Joydeep_Das_Full_Stack_AI_Engineer_Resume.pdf",
        "fde": "Joydeep_Das_Full_Stack_AI_Engineer_Resume.pdf",
        "ai": "Joydeep_Das_Full_Stack_AI_Engineer_Resume.pdf",
        "hr": "Joydeep_Das_Resume_HR.pdf",
        "sales": "Joydeep_Das_Full_Stack_AI_Engineer_Resume.pdf",
        "developer": "Joydeep_Das_Full_Stack_AI_Engineer_Resume.pdf",
    }
    pdf_filename = filename_map.get(role, "Joydeep_Das_Full_Stack_AI_Engineer_Resume.pdf")
    
    keyboard = [
        [
            InlineKeyboardButton(f"🚀 Launch Application to {draft['to']}", callback_data="send_now"),
        ],
        [
            InlineKeyboardButton("💻 Frontend", callback_data="set_frontend"),
            InlineKeyboardButton("🎨 UI/UX", callback_data="set_uiux"),
            InlineKeyboardButton("🤖 FDE", callback_data="set_fde"),
        ],
        [
            InlineKeyboardButton("🧠 AI Trainer", callback_data="set_ai"),
            InlineKeyboardButton("👥 HR / Talent", callback_data="set_hr"),
            InlineKeyboardButton("📈 Growth / Sales", callback_data="set_sales"),
        ],
        [
            InlineKeyboardButton("❌ Scrap it", callback_data="cancel"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    preview_msg = (
        f"🎯 *Application Ready for Review:*\n\n"
        f"🏢 *Company:* `{draft['company']}`\n"
        f"📬 *Target Recruiter:* `{draft['to']}`\n"
        f"🏷️ *Role Track:* `{role.upper()}`\n"
        f"📄 *Attachment:* `{pdf_filename}` (PDF)\n"
        f"📝 *Subject:* `{draft['subject']}`\n\n"
        f"*Pitch Snippet:*\n_{draft['plain'][:320]}..._\n\n"
        f"Hit *Launch Application* to fire it off, or switch tracks below! 👇"
    )
    return preview_msg, reply_markup

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ALLOWED_USER_ID:
        await update.message.reply_text("Nah fam, you're not on the guest list. 🙅‍♂️")
        return

    welcome_text = (
        "🤠 *Jim Bob is locked in and loaded!* Your elite autonomous career scout is online! 🚀🔥\n\n"
        "⚡ *What Jim Bob can execute for you:*\n"
        "• 📸 *Vision OCR:* Send any job screenshot or photo—I'll extract the recruiter email and details.\n"
        "• 📬 *Fresh Leads:* Tap the menu buttons below or type `/leads` for verified uncontacted emails.\n"
        "• 🔄 *Live Web Scraper:* `/fetch` pulls fresh tech openings across remote boards.\n"
        "• 🎯 *Targeted Pitching:* `/apply email@domain.com [Company] [role]` or paste any JD directly.\n"
        "• 🔍 *Duplicate Immunity:* `/check <Company or Email>` prevents repeated applications.\n"
        "• 📊 *Recon Tracker:* `/stats` & `/list` keep you in control of every dispatch.\n"
        "• 🧠 *Conscious Dev Partner:* Talk to me in plain English about interview prep, your projects, or your resumes!\n\n"
        "Tap the buttons below or send over a job link to get moving! 👇"
    )
    inline_controls = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("📬 Fresh Leads", callback_data="filter_leads_email"),
            InlineKeyboardButton("🔄 Live Fetch", callback_data="trigger_fetch")
        ],
        [
            InlineKeyboardButton("🔽 Minimize Bottom Keyboard", callback_data="hide_keyboard")
        ]
    ])
    await update.message.reply_text(welcome_text, reply_markup=MAIN_MENU_KEYBOARD, parse_mode="Markdown")
    await update.message.reply_text("⚡ *Quick Controls:*", reply_markup=inline_controls, parse_mode="Markdown")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ALLOWED_USER_ID:
        return

    help_text = (
        "🛠️ *Command Center Guide:*\n\n"
        "• `/leads` or `/leads email` - Fresh leads with direct recruiter emails (1-tap apply!)\n"
        "• `/leads junior` - Entry-level & Junior remote developer/designer openings\n"
        "• `/leads react` - React, Next.js, and modern Frontend openings\n"
        "• `/leads uiux` - UI/UX & Product Design remote jobs\n"
        "• `/fetch` - Scrape & refresh latest jobs across 5 remote job boards\n"
        "• `/apply <email> [Company] [role]` - Instantly craft a custom application draft\n"
        "• `/check <company/email>` - Check if you already applied\n"
        "• `/company <name>` - Fix company name on current pending draft\n"
        "• `/subject <text>` - Custom subject line for pending draft\n"
        "• `/stats` - Total applications sent and companies reached\n"
        "• `/list` - View last 8 applications with timestamps\n\n"
        "💡 *Tip:* Use the buttons below the text bar for one-tap access!"
    )
    await update.message.reply_text(help_text, reply_markup=MAIN_MENU_KEYBOARD, parse_mode="Markdown")

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ALLOWED_USER_ID:
        return
    total, companies = tracker.get_stats()
    text = (
        f"📊 *Application Tracker Stats*\n\n"
        f"• *Total Applications Sent:* `{total}`\n"
        f"• *Companies Reached:* `{companies}`\n\n"
        f"Use `/list` to view recent applications! 🚀"
    )
    await update.message.reply_text(text, parse_mode="Markdown")

async def list_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ALLOWED_USER_ID:
        return
    rows = tracker.get_recent_applications(8)
    if not rows:
        await update.message.reply_text("No applications logged in the tracker yet bro!")
        return

    msg = "📋 *Recent Applications:*\n\n"
    for r in rows:
        app_id, company, email, role, timestamp, status = r
        msg += f"• *{company}* ({role.upper()})\n  📬 `{email}` | 🕒 {timestamp}\n"

    await update.message.reply_text(msg, parse_mode="Markdown")

async def check_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ALLOWED_USER_ID:
        return
    query = " ".join(context.args).strip() if context.args else ""
    if not query:
        await update.message.reply_text("Usage: `/check <company or email>`\nExample: `/check Stripe` or `/check jobs@linear.app`", parse_mode="Markdown")
        return

    results = tracker.check_applied(query)
    if results:
        msg = f"⚠️ *Found past application(s) matching '{query}':*\n\n"
        for r in results:
            company, email, role, timestamp, status = r
            msg += f"• *{company}* ({role.upper()})\n  📬 `{email}`\n  🕒 Applied: {timestamp} (Status: {status})\n\n"
        await update.message.reply_text(msg, parse_mode="Markdown")
    else:
        await update.message.reply_text(f"✅ Clean slate! You haven't sent an application to *{query}* yet. Go for it! 🎯", parse_mode="Markdown")

async def apply_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ALLOWED_USER_ID:
        return

    args = context.args
    if not args:
        await update.message.reply_text(
            "Usage: `/apply <email> [Company] [role]`\n"
            "• Examples:\n"
            "  `/apply jobs@resend.com Resend frontend`\n"
            "  `/apply hr@figma.com Figma uiux`\n"
            "  `/apply tech@startup.io Startup fde`",
            parse_mode="Markdown"
        )
        return

    to_email = args[0].strip()
    if "@" not in to_email or "." not in to_email:
        await update.message.reply_text("Please provide a valid recipient email address bro!", parse_mode="Markdown")
        return

    company = "your team"
    role = "frontend"
    if len(args) >= 2:
        if args[1].lower() in ["frontend", "uiux", "fde"]:
            role = args[1].lower()
        else:
            company = args[1].strip()
    if len(args) >= 3:
        if args[2].lower() in ["frontend", "uiux", "fde"]:
            role = args[2].lower()
        elif company == "your team":
            company = args[2].strip()

    if company == "your team":
        domain = to_email.split("@")[-1].split(".")[0]
        if domain not in ["gmail", "yahoo", "hotmail", "outlook"]:
            company = domain.capitalize()

    role_titles = {
        "uiux": "UI/UX Designer & Product Designer",
        "frontend": "Frontend Developer (React / TypeScript)",
        "fde": "Forward Deployed Engineer / Full-Stack Developer"
    }

    subject, plain, html = generate_email_content(role, role_titles[role], company)

    DRAFTS[ALLOWED_USER_ID] = {
        "to": to_email,
        "subject": subject,
        "plain": plain,
        "html": html,
        "role": role,
        "company": company
    }

    preview_msg, reply_markup = render_draft_preview(DRAFTS[ALLOWED_USER_ID])
    await update.message.reply_text(preview_msg, reply_markup=reply_markup, parse_mode="Markdown")

async def company_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ALLOWED_USER_ID:
        return

    draft = DRAFTS.get(ALLOWED_USER_ID)
    if not draft:
        await update.message.reply_text("No active draft to edit bro! Drop a JD or use `/apply` first.")
        return

    new_company = " ".join(context.args).strip()
    if not new_company:
        await update.message.reply_text("Usage: `/company <Company Name>`\nExample: `/company Linear`", parse_mode="Markdown")
        return

    role_titles = {
        "uiux": "UI/UX Designer & Product Designer",
        "frontend": "Frontend Developer (React / TypeScript)",
        "fde": "Forward Deployed Engineer / Full-Stack Developer"
    }
    role = draft["role"]
    subject, plain, html = generate_email_content(role, role_titles[role], new_company)
    draft["company"] = new_company
    draft["subject"] = subject
    draft["plain"] = plain
    draft["html"] = html

    preview_msg, reply_markup = render_draft_preview(draft)
    await update.message.reply_text(f"✅ Updated company to *{new_company}*!\n\n" + preview_msg, reply_markup=reply_markup, parse_mode="Markdown")

async def subject_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ALLOWED_USER_ID:
        return

    draft = DRAFTS.get(ALLOWED_USER_ID)
    if not draft:
        await update.message.reply_text("No active draft to edit bro! Drop a JD or use `/apply` first.")
        return

    new_sub = " ".join(context.args).strip()
    if not new_sub:
        await update.message.reply_text("Usage: `/subject <Custom Subject Line>`", parse_mode="Markdown")
        return

    draft["subject"] = new_sub
    preview_msg, reply_markup = render_draft_preview(draft)
    await update.message.reply_text(f"✅ Updated subject line!\n\n" + preview_msg, reply_markup=reply_markup, parse_mode="Markdown")

def build_leads_page_payload(user_id: int, page: int = 0):
    cache = LEADS_CACHE.get(user_id, {})
    leads = cache.get("leads", [])
    filter_type = cache.get("filter", "email")

    if not leads:
        msg = (
            f"🔍 No unapplied leads found for filter: <b>{filter_type}</b>.\n"
            f"Try running <code>/fetch</code> to scrape fresh jobs, or switch filters!"
        )
        buttons = [
            [
                InlineKeyboardButton("📧 Direct Email", callback_data="filter_leads_email"),
                InlineKeyboardButton("🐣 Junior", callback_data="filter_leads_junior"),
                InlineKeyboardButton("⚛️ React", callback_data="filter_leads_react"),
                InlineKeyboardButton("🎨 UI/UX", callback_data="filter_leads_uiux"),
            ],
            [
                InlineKeyboardButton("🔄 Refresh Scraping", callback_data="trigger_fetch"),
            ]
        ]
        return msg, InlineKeyboardMarkup(buttons)

    page_size = 4
    total_pages = max(1, (len(leads) + page_size - 1) // page_size)
    page = max(0, min(page, total_pages - 1))
    cache["page"] = page

    start_idx = page * page_size
    end_idx = min(start_idx + page_size, len(leads))
    page_leads = leads[start_idx:end_idx]

    header_icons = {
        "email": "📬 <b>Direct Email Outreach Leads</b> (Fresh & Unsent)",
        "junior": "🐣 <b>Junior & Entry-Level Openings</b>",
        "react": "⚛️ <b>React & Frontend Developer Openings</b>",
        "uiux": "🎨 <b>UI/UX & Product Design Openings</b>",
        "all": "💼 <b>All Fresh Tech Openings</b>"
    }

    msg = f"{header_icons.get(filter_type, '💼 Fresh Leads')} (Total: {len(leads)})\n"
    msg += f"<i>Page {page + 1} of {total_pages}</i>\n\n"

    action_buttons = []

    for i, l in enumerate(page_leads):
        global_idx = start_idx + i
        comp = html_lib.escape(l.get("company", "Company"))
        title = html_lib.escape(l.get("title", "Role"))
        src = html_lib.escape(l.get("source", "Remote"))
        loc = html_lib.escape(l.get("location", "Remote"))
        url = l.get("url") or l.get("apply_url") or ""
        emails = l.get("fresh_emails") or l.get("emails") or []

        msg += f"<b>[{global_idx + 1}] {comp}</b> — <i>{title}</i>\n"
        msg += f"📍 {loc} | 🌐 {src}\n"
        if url:
            msg += f"🔗 <a href=\"{url}\">View Job Posting</a>\n"
        if emails:
            email_str = ", ".join([f"<code>{e}</code>" for e in emails[:2]])
            msg += f"✉️ Recruiter: {email_str}\n"
            clean_comp = re.sub(r'[^a-zA-Z0-9 ]', '', comp).strip()[:14]
            action_buttons.append(
                InlineKeyboardButton(f"📨 Pitch {clean_comp}", callback_data=f"apply_lead_{global_idx}")
            )
        msg += "\n"

    keyboard = []
    # Add quick-pitch buttons (2 per row)
    for idx in range(0, len(action_buttons), 2):
        keyboard.append(action_buttons[idx:idx+2])

    # Navigation buttons
    nav_row = []
    if page > 0:
        nav_row.append(InlineKeyboardButton("⬅️ Prev", callback_data=f"lead_page_{page - 1}"))
    nav_row.append(InlineKeyboardButton(f"{page + 1}/{total_pages}", callback_data="noop"))
    if page < total_pages - 1:
        nav_row.append(InlineKeyboardButton("Next ➡️", callback_data=f"lead_page_{page + 1}"))
    keyboard.append(nav_row)

    # Filter switch row
    filter_row = [
        InlineKeyboardButton("📧 Email", callback_data="filter_leads_email"),
        InlineKeyboardButton("🐣 Junior", callback_data="filter_leads_junior"),
        InlineKeyboardButton("⚛️ React", callback_data="filter_leads_react"),
        InlineKeyboardButton("🎨 UI/UX", callback_data="filter_leads_uiux"),
    ]
    keyboard.append(filter_row)

    return msg, InlineKeyboardMarkup(keyboard)

async def leads_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ALLOWED_USER_ID:
        return

    filter_type = context.args[0].lower() if context.args else "email"
    if filter_type in ["mail", "direct"]:
        filter_type = "email"

    leads = load_filtered_leads(filter_type)
    LEADS_CACHE[ALLOWED_USER_ID] = {
        "leads": leads,
        "filter": filter_type,
        "page": 0
    }

    msg, markup = build_leads_page_payload(ALLOWED_USER_ID, 0)
    await update.message.reply_text(msg, reply_markup=markup, parse_mode="HTML", disable_web_page_preview=True)

async def fetch_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ALLOWED_USER_ID:
        return

    status_msg = await update.message.reply_text(
        "🔄 *Scanning remote job boards...*\n"
        "Pulling fresh postings from RemoteOK, HackerNews, WeWorkRemotely, Remotive, and Jobicy. Sit tight bro! 🌐⏳",
        parse_mode="Markdown"
    )

    try:
        new_leads = await asyncio.to_thread(fetch_all_sources.run)
        leads_email = load_filtered_leads("email")
        leads_junior = load_filtered_leads("junior")

        LEADS_CACHE[ALLOWED_USER_ID] = {
            "leads": leads_email,
            "filter": "email",
            "page": 0
        }

        msg, markup = build_leads_page_payload(ALLOWED_USER_ID, 0)
        await status_msg.edit_text(
            f"✅ *Scrape Complete!*\n"
            f"• Total tech leads indexed: `{len(new_leads)}`\n"
            f"• Fresh uncontacted email outreach targets: `{len(leads_email)}`\n"
            f"• Junior/Entry opportunities: `{len(leads_junior)}`\n\n"
            f"Here are the top recruiter outreach leads:",
            parse_mode="Markdown"
        )
        await update.message.reply_text(msg, reply_markup=markup, parse_mode="HTML", disable_web_page_preview=True)

    except Exception as e:
        await status_msg.edit_text(f"❌ Scraping error: `{e}`. Check console logs.", parse_mode="Markdown")

def _generate_groq_hook(job_text: str, company: str, role_title: str) -> str | None:
    """Generate a 1-sentence tailored opening hook using Groq based on the pasted job text."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key or len(job_text.strip()) < 25:
        return None
    payload = json.dumps({
        "model": "llama-3.1-8b-instant",
        "messages": [{
            "role": "user",
            "content": f"Write 1 concise, natural opening sentence for a cold job application email to {company} for {role_title}, referencing the specific tech stack or focus in this post:\n\n{job_text[:1000]}"
        }],
        "temperature": 0.4,
        "max_tokens": 80,
    }).encode("utf-8")
    req = urllib.request.Request(
        "https://api.groq.com/openai/v1/chat/completions",
        data=payload,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=8) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return data["choices"][0]["message"]["content"].strip().strip('"')

async def followups_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ALLOWED_USER_ID:
        return
    import sqlite3
    db_path = tracker.DB_PATH
    if not db_path.exists():
        await update.message.reply_text("No applications logged yet.")
        return
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT company, recipient_email, role, sent_at FROM applications WHERE datetime(sent_at) <= datetime('now', '-5 days') ORDER BY sent_at DESC LIMIT 10")
    rows = c.fetchall()
    conn.close()
    if not rows:
        await update.message.reply_text("✅ No applications are due for a 5-day follow-up yet.")
        return
    lines = ["⏰ *5-Day Follow-Up Nudges:*\n"]
    for comp, email, role, sent_at in rows:
        lines.append(f"• *{comp}* (`{email}`) — {role} _(sent {str(sent_at)[:10]})_")
    await update.message.reply_text("\n".join(lines), parse_mode="Markdown")

async def export_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ALLOWED_USER_ID:
        return
    import csv, io, sqlite3
    db_path = tracker.DB_PATH
    if not db_path.exists():
        await update.message.reply_text("No applications logged yet.")
        return
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT id, company, recipient_email, role, subject, sent_at FROM applications ORDER BY sent_at DESC")
    rows = c.fetchall()
    conn.close()
    if not rows:
        await update.message.reply_text("No applications logged yet.")
        return
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(["id", "company", "recipient_email", "role", "subject", "sent_at"])
    writer.writerows(rows)
    data = io.BytesIO(buf.getvalue().encode("utf-8"))
    data.name = "applications_export.csv"
    await update.message.reply_document(document=data, caption=f"📊 Exported {len(rows)} applications.")

async def hr_outreach_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ALLOWED_USER_ID:
        return
    from apify_hr_outreach.hr_outreach import fetch_apify_hr_leads
    try:
        leads = await asyncio.to_thread(fetch_apify_hr_leads, 10)
    except Exception as e:
        await update.message.reply_text(f"Apify HR outreach error: `{e}`", parse_mode="Markdown")
        return
    if not leads:
        await update.message.reply_text(
            "Set `APIFY_API_TOKEN` and `APIFY_HR_DATASET_ID` in `.env` / Render to pull Apify HR leads.",
            parse_mode="Markdown"
        )
        return
    lines = ["👥 *Apify HR Outreach Leads:*\n"]
    for item in leads[:10]:
        title = item.get("title") or item.get("positionName") or "HR / Talent Role"
        company = item.get("company") or item.get("companyName") or "Company"
        lines.append(f"• *{company}* — {title}")
    await update.message.reply_text("\n".join(lines), parse_mode="Markdown")

async def autoapply_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ALLOWED_USER_ID:
        return
    if not context.args:
        await update.message.reply_text("Usage: `/autoapply <job_url> [--hr]`", parse_mode="Markdown")
        return
    url = context.args[0]
    hr_flag = "--hr" if "--hr" in context.args else ""
    try:
        import playwright  # noqa: F401
        import subprocess
        cmd = [sys.executable, str(Path(__file__).parent / "auto_apply_playwright.py"), url]
        if hr_flag:
            cmd.append(hr_flag)
        subprocess.Popen(cmd)
        await update.message.reply_text(f"🚀 Launched local Playwright auto-filler for `{url}`", parse_mode="Markdown")
    except ImportError:
        await update.message.reply_text(
            f"Playwright isn't available on this server (Render free tier). Run this locally:\n`python auto_apply_playwright.py {url} {hr_flag}`".strip(),
            parse_mode="Markdown"
        )

async def process_job_text(text: str, update: Update):
    to_email, role, role_title, company = extract_job_info(text)

    if not to_email:
        # Route through Jim Bob Brain (Groq LLM → pattern fallback)
        intelligent_reply = jim_bob_brain.ask_jim_bob(text, tracker)

        # If user asked about resumes or profiles, include fast track selector buttons
        casual_lower = text.lower().strip()
        if any(q in casual_lower for q in ["resume", "resumes", "cv", "portfolio"]) and any(q in casual_lower for q in ["have", "access", "all", "what", "which", "show", "can you", "list"]):
            buttons = [
                [
                    InlineKeyboardButton("💻 Frontend", callback_data="filter_leads_react"),
                    InlineKeyboardButton("🎨 UI/UX", callback_data="filter_leads_uiux"),
                ],
                [
                    InlineKeyboardButton("🤖 FDE / Full-Stack", callback_data="filter_leads_email"),
                    InlineKeyboardButton("🧠 AI Trainer", callback_data="filter_leads_email"),
                ],
                [
                    InlineKeyboardButton("👥 HR / Talent", callback_data="filter_leads_email"),
                    InlineKeyboardButton("📈 Growth / Sales", callback_data="filter_leads_email"),
                ]
            ]
            await update.message.reply_text(intelligent_reply, reply_markup=InlineKeyboardMarkup(buttons), parse_mode="Markdown")
            return

        await update.message.reply_text(intelligent_reply, parse_mode="Markdown")
        return

    applied_emails, applied_companies = get_applied_records()
    dup_warning = ""
    if (to_email and to_email.lower() in applied_emails) or (company and company.lower() != "your team" and company.lower() in applied_companies):
        dup_warning = f"⚠️ *Heads up:* You already have an application logged for `{company}` / `{to_email}`.\n\n"

    subject, plain_body, html_body = generate_email_content(role, role_title, company)
    try:
        hook = await asyncio.to_thread(_generate_groq_hook, text, company, role_title)
        if hook:
            plain_body = f"{hook}\n\n{plain_body}"
            html_body = html_body.replace("<body>", f"<body><p>{html_lib.escape(hook)}</p>", 1)
    except Exception:
        pass

    DRAFTS[ALLOWED_USER_ID] = {
        "to": to_email,
        "subject": subject,
        "plain": plain_body,
        "html": html_body,
        "role": role,
        "company": company
    }

    preview_msg, reply_markup = render_draft_preview(DRAFTS[ALLOWED_USER_ID])
    await update.message.reply_text(dup_warning + preview_msg, reply_markup=reply_markup, parse_mode="Markdown")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ALLOWED_USER_ID:
        return
    text = (update.message.text or "").strip()

    # Route persistent keyboard button taps & natural leads/fetch requests
    low_text = text.lower().strip()
    if text == "📬 Fresh Leads" or low_text in ["leads", "show leads", "fresh leads", "get leads", "leads please"]:
        context.args = ["email"]
        await leads_command(update, context)
        return
    elif text == "🔄 Fetch New Jobs" or low_text in ["fetch", "fetch leads", "fetch new jobs", "fetch jobs", "scrape jobs", "scrape leads", "/fetch"]:
        context.args = []
        await fetch_command(update, context)
        return
    elif text == "🐣 Junior Openings" or low_text in ["junior leads", "junior jobs", "entry level jobs"]:
        context.args = ["junior"]
        await leads_command(update, context)
        return
    elif text == "⚛️ React Jobs" or low_text in ["react jobs", "frontend jobs", "react leads"]:
        context.args = ["react"]
        await leads_command(update, context)
        return
    elif text == "🎨 UI/UX Jobs" or low_text in ["uiux jobs", "ui/ux jobs", "design jobs"]:
        context.args = ["uiux"]
        await leads_command(update, context)
        return
    elif text == "📊 Tracker Stats":
        await stats_command(update, context)
        return
    elif text == "📋 Recent Applications":
        await list_command(update, context)
        return
    elif text == "❓ Help / Commands":
        await help_command(update, context)
        return
    elif text in ["🔽 Minimize Menu", "🔽 Minimize Bottom Keyboard", "/minimize"]:
        await update.message.reply_text(
            "Keyboard minimized! 📱 To bring it back anytime, just type `/menu` or `/start`.",
            reply_markup=ReplyKeyboardRemove()
        )
        return
    elif text in ["/menu", "menu"]:
        await update.message.reply_text(
            "Here's your menu keyboard! 🚀",
            reply_markup=MAIN_MENU_KEYBOARD
        )
        return

    # Check if user sent a standalone URL (not a pasted post that happens to contain a link)
    url_match = re.search(r'https?://[^\s]+', text)
    if url_match and "@" not in text and len(text.split()) <= 2:
        url = url_match.group(0)
        if "linkedin.com" in url.lower() or "lnkd.in" in url.lower():
            await update.message.reply_text(
                "LinkedIn blocks auto-reading links. Paste the post/job text directly or send a screenshot!"
            )
            return
        status_msg = await update.message.reply_text(f"🌐 Fetching job posting from `{url[:45]}...`", parse_mode="Markdown")
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            def fetch_url():
                with urllib.request.urlopen(req, timeout=10) as resp:
                    return resp.read().decode('utf-8', errors='ignore')
            raw_html = await asyncio.to_thread(fetch_url)
            text_extracted = fetch_all_sources.clean_html(raw_html)
            await status_msg.delete()
            await process_job_text(text_extracted[:2000], update)
            return
        except Exception as e:
            await status_msg.edit_text(f"Couldn't auto-read URL (`{e}`). Paste the job text directly bro!")
            return

    await process_job_text(text, update)

def _extract_text_with_groq_vision(img_path: Path) -> str | None:
    """Use Groq Vision to accurately extract job text, company, role, and email from a screenshot."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return None
    import base64
    with open(img_path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("utf-8")
    payload = json.dumps({
        "model": "meta-llama/llama-4-scout-17b-16e-instruct",
        "messages": [{
            "role": "user",
            "content": [
                {"type": "text", "text": "Extract all text from this job posting screenshot accurately, especially any email addresses, company name, and job role/title. Return plain text only."},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}},
            ],
        }],
        "temperature": 0.1,
        "max_tokens": 1024,
    }).encode("utf-8")
    req = urllib.request.Request(
        "https://api.groq.com/openai/v1/chat/completions",
        data=payload,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return data["choices"][0]["message"]["content"].strip()

async def handle_photo_or_doc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ALLOWED_USER_ID:
        return

    msg = await update.message.reply_text("👀 Reading your screenshot right now bro, give me a few seconds...")

    try:
        if update.message.photo:
            file_obj = update.message.photo[-1]
        elif update.message.document and update.message.document.mime_type.startswith("image/"):
            file_obj = update.message.document
        else:
            await msg.edit_text("That file doesn't look like an image bro! Send a photo or screenshot.")
            return

        file = await file_obj.get_file()
        
        save_dir = Path(__file__).parent / "temp_photos"
        save_dir.mkdir(exist_ok=True)
        img_path = save_dir / f"{file_obj.file_id}.jpg"
        await file.download_to_drive(str(img_path))

        extracted_text = None
        try:
            extracted_text = await asyncio.to_thread(_extract_text_with_groq_vision, img_path)
        except Exception:
            extracted_text = None

        if not extracted_text:
            reader = get_ocr_reader()
            results = await asyncio.to_thread(reader.readtext, str(img_path))
            extracted_text = " ".join([res[1] for res in results])

        caption = update.message.caption or ""
        combined_text = f"{caption} {extracted_text}".strip()

        try:
            os.remove(img_path)
        except Exception:
            pass

        await msg.delete()
        await process_job_text(combined_text, update)

    except Exception as e:
        await msg.edit_text(f"Damn bro, had trouble reading that image: `{e}`. Try sending the text directly or a cleaner shot!", parse_mode="Markdown")

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.from_user.id != ALLOWED_USER_ID:
        return

    data = query.data

    if data == "noop":
        return

    if data == "hide_keyboard":
        await query.message.reply_text(
            "Keyboard minimized! 📱 To bring it back anytime, just send `/menu`.",
            reply_markup=ReplyKeyboardRemove()
        )
        return

    # Trigger fresh fetch from button
    if data == "trigger_fetch":
        await query.edit_message_text("🔄 Initiating fresh live scrape...")
        await fetch_command(query, context)
        return

    # Switch leads filter
    if data.startswith("filter_leads_"):
        new_filter = data.replace("filter_leads_", "")
        leads = load_filtered_leads(new_filter)
        LEADS_CACHE[ALLOWED_USER_ID] = {
            "leads": leads,
            "filter": new_filter,
            "page": 0
        }
        msg, markup = build_leads_page_payload(ALLOWED_USER_ID, 0)
        await query.edit_message_text(msg, reply_markup=markup, parse_mode="HTML", disable_web_page_preview=True)
        return

    # Pagination in leads
    if data.startswith("lead_page_"):
        target_page = int(data.replace("lead_page_", ""))
        msg, markup = build_leads_page_payload(ALLOWED_USER_ID, target_page)
        await query.edit_message_text(msg, reply_markup=markup, parse_mode="HTML", disable_web_page_preview=True)
        return

    # One-click pitch lead from leads browser
    if data.startswith("apply_lead_"):
        lead_idx = int(data.replace("apply_lead_", ""))
        cache = LEADS_CACHE.get(ALLOWED_USER_ID, {})
        leads = cache.get("leads", [])
        if lead_idx >= len(leads):
            await query.message.reply_text("Lead index expired bro, try refreshing `/leads`!")
            return

        target_lead = leads[lead_idx]
        emails = target_lead.get("fresh_emails") or target_lead.get("emails") or []
        if not emails:
            await query.message.reply_text("No direct email detected on this posting bro!")
            return

        to_email = emails[0]
        company = target_lead.get("company", "Company")
        cat = target_lead.get("category", "")
        title = target_lead.get("title", "")

        if cat == "UI/UX Designer" or "design" in title.lower():
            role = "uiux"
            role_title = "UI/UX Designer & Product Designer"
        elif cat in ["React Developer", "Frontend Developer"] or any(k in title.lower() for k in ["react", "frontend", "web"]):
            role = "frontend"
            role_title = "Frontend Developer (React / TypeScript)"
        else:
            role = "fde"
            role_title = "Forward Deployed Engineer / Full-Stack Developer"

        subject, plain, html = generate_email_content(role, role_title, company)
        DRAFTS[ALLOWED_USER_ID] = {
            "to": to_email,
            "subject": subject,
            "plain": plain,
            "html": html,
            "role": role,
            "company": company
        }

        preview_msg, reply_markup = render_draft_preview(DRAFTS[ALLOWED_USER_ID])
        await query.message.reply_text(
            f"⚡ *Loaded lead for {company}!* Check out the tailored draft:\n\n" + preview_msg,
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
        return

    draft = DRAFTS.get(ALLOWED_USER_ID)
    if not draft:
        await query.edit_message_text("Yo, that draft expired or already got handled bro! Drop a new one anytime. ⚡")
        return

    if data == "cancel":
        DRAFTS.pop(ALLOWED_USER_ID, None)
        await query.edit_message_text("Scrapped it! No worries, onto the next one. 🗑️👌")
        return

    if data in ["set_uiux", "set_frontend", "set_fde", "set_ai", "set_hr", "set_sales"]:
        new_role = data.replace("set_", "")
        role_titles = {
            "uiux": "UI/UX Designer & Product Designer",
            "frontend": "Frontend Developer (React / TypeScript)",
            "fde": "Forward Deployed Engineer / Full-Stack Developer",
            "ai": "AI Trainer & LLM Evaluation Specialist",
            "hr": "Talent Acquisition & Creator Sourcing Associate",
            "sales": "Content Strategist & Growth Marketer"
        }
        subject, plain, html = generate_email_content(new_role, role_titles[new_role], draft["company"])
        draft["role"] = new_role
        draft["subject"] = subject
        draft["plain"] = plain
        draft["html"] = html

        preview_msg, reply_markup = render_draft_preview(draft)
        await query.edit_message_text(
            f"Gotchu bro! Switched over to the *{new_role.upper()}* track. 🔄\n\n" + preview_msg,
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
        return

    if data == "send_now":
        await query.edit_message_text(f"🚀 Firing off the application to `{draft['to']}` right now bro, hold tight...", parse_mode="Markdown")
        try:
            send_application.send_application_email(
                to_email=draft["to"],
                subject=draft["subject"],
                body_plain=draft["plain"],
                body_html=draft["html"],
                role_type=draft["role"],
                company_name=draft["company"]
            )
            await query.message.reply_text(
                f"BOOM! 💥 Successfully delivered to `{draft['to']}`!\n\n"
                f"• *Subject:* `{draft['subject']}`\n"
                f"• *Attached:* `{draft['role'].upper()} Resume (PDF)`\n"
                f"• *Status:* Logged in database tracker ✅\n\n"
                f"Keep 'em coming bro, let's get those interviews booked! 🥂🔥",
                parse_mode="Markdown"
            )
            DRAFTS.pop(ALLOWED_USER_ID, None)
        except Exception as e:
            await query.message.reply_text(f"Damn bro, hit a snag sending that: `{e}`. Check your internet or SMTP and try again!", parse_mode="Markdown")

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logging.getLogger("telegram_bot").warning(f"Update caused network/internal error: {context.error}")

# ─── Jim Bob Executive Commands ──────────────────────────────────────────────

async def do_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    /do <anything> — Jim Bob's master task executor.
    Examples:
      /do push flatzy to github with message 'hotfix nav'
      /do check git status of medirag
      /do draft a client update for flatzy
      /do what time is it in Tokyo
    """
    if update.effective_user.id != ALLOWED_USER_ID:
        return

    task = " ".join(context.args).strip() if context.args else ""
    if not task:
        await update.message.reply_text(
            "🤠 *Jim Bob standing by!*\n\n"
            "Tell me what to do:\n"
            "• `/do push flatzy to github`\n"
            "• `/do git status medirag`\n"
            "• `/do deploy flatzy on vercel`\n"
            "• `/do draft client update for john`\n"
            "• `/do run dir C:\\Projects`\n"
            "• or just type anything in plain English!",
            parse_mode="Markdown"
        )
        return

    await update.message.reply_text(f"⚡ Jim Bob is on it: *{task}*...", parse_mode="Markdown")
    reply = jim_bob_brain.ask_jim_bob(task, tracker)
    await update.message.reply_text(reply, parse_mode="Markdown")


async def mind_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """/mind — View Jim Bob's conscious mental state, thoughts, and memories"""
    if update.effective_user.id != ALLOWED_USER_ID:
        return
    import jim_bob_consciousness
    status = jim_bob_consciousness.consciousness.get_mind_status()
    await update.message.reply_text(status, parse_mode="Markdown")


async def git_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    /git status <repo>  — check repo status
    /git push <repo> <msg>  — commit and push
    """
    if update.effective_user.id != ALLOWED_USER_ID:
        return

    args = context.args or []
    if not args:
        await update.message.reply_text(
            "Usage:\n• `/git status flatzy`\n• `/git push flatzy 'fixed nav bug'`",
            parse_mode="Markdown"
        )
        return

    sub = args[0].lower()
    if sub == "status":
        repo_name = " ".join(args[1:]).strip() if len(args) > 1 else ""
        repo_path = jim_bob_brain.find_repo(repo_name)
        if not repo_path:
            paths = ", ".join(jim_bob_brain.KNOWN_REPOS.keys())
            await update.message.reply_text(f"⚠️ Can't find repo `{repo_name}`.\nKnown repos: `{paths}`", parse_mode="Markdown")
            return
        await update.message.reply_text(jim_bob_brain.git_status(repo_path), parse_mode="Markdown")

    elif sub == "push":
        repo_name = args[1] if len(args) > 1 else ""
        commit_msg = " ".join(args[2:]).strip() if len(args) > 2 else f"Jim Bob auto-commit"
        repo_path = jim_bob_brain.find_repo(repo_name)
        if not repo_path:
            await update.message.reply_text(f"⚠️ Repo `{repo_name}` not found.", parse_mode="Markdown")
            return
        await update.message.reply_text("⏳ Staging, committing, pushing...", parse_mode="Markdown")
        result = jim_bob_brain.git_push(repo_path, commit_msg)
        await update.message.reply_text(result, parse_mode="Markdown")
    else:
        await update.message.reply_text("Unknown git subcommand. Use `status` or `push`.", parse_mode="Markdown")


async def deploy_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """/deploy <project> — trigger Vercel deploy"""
    if update.effective_user.id != ALLOWED_USER_ID:
        return
    project = " ".join(context.args).strip() if context.args else ""
    if not project:
        await update.message.reply_text("Usage: `/deploy flatzy`", parse_mode="Markdown")
        return
    result = jim_bob_brain.trigger_vercel_deploy(project)
    await update.message.reply_text(result, parse_mode="Markdown")


async def update_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """/update <project> [client <name>] — draft a client update"""
    if update.effective_user.id != ALLOWED_USER_ID:
        return
    args = context.args or []
    project = args[0].capitalize() if args else "Flatzy"
    client = "Client"
    if "client" in [a.lower() for a in args]:
        idx = [a.lower() for a in args].index("client")
        if idx + 1 < len(args):
            client = args[idx + 1].capitalize()
    result = jim_bob_brain.generate_client_update(client, project)
    await update.message.reply_text(result, parse_mode="Markdown")


async def shell_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """/shell <command> — run a shell command"""
    if update.effective_user.id != ALLOWED_USER_ID:
        return
    cmd = " ".join(context.args).strip() if context.args else ""
    if not cmd:
        await update.message.reply_text("Usage: `/shell dir C:\\Projects`", parse_mode="Markdown")
        return
    await update.message.reply_text(f"⚡ Running: `{cmd}`...", parse_mode="Markdown")
    result = jim_bob_brain.run_shell(cmd)
    await update.message.reply_text(result, parse_mode="Markdown")


def main():
    app = (
        ApplicationBuilder()
        .token(BOT_TOKEN)
        .post_init(post_init)
        .connect_timeout(30.0)
        .read_timeout(30.0)
        .write_timeout(30.0)
        .get_updates_read_timeout(30.0)
        .build()
    )
    # Commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("leads", leads_command))
    app.add_handler(CommandHandler("fetch", fetch_command))
    app.add_handler(CommandHandler("apply", apply_command))
    app.add_handler(CommandHandler("check", check_command))
    app.add_handler(CommandHandler("company", company_command))
    app.add_handler(CommandHandler("subject", subject_command))
    app.add_handler(CommandHandler("stats", stats_command))
    app.add_handler(CommandHandler("list", list_command))
    app.add_handler(CommandHandler("followups", followups_command))
    app.add_handler(CommandHandler("autoapply", autoapply_command))
    app.add_handler(CommandHandler("hr_outreach", hr_outreach_command))
    app.add_handler(CommandHandler("export", export_command))
    app.add_handler(CommandHandler("menu", lambda u, c: u.message.reply_text("Here's your menu keyboard! 🚀", reply_markup=MAIN_MENU_KEYBOARD)))
    app.add_handler(CommandHandler("minimize", lambda u, c: u.message.reply_text("Keyboard minimized! 📱 Send /menu to reopen.", reply_markup=ReplyKeyboardRemove())))

    # Jim Bob Executive Commands
    app.add_handler(CommandHandler("do", do_command))
    app.add_handler(CommandHandler("mind", mind_command))
    app.add_handler(CommandHandler("git", git_command))
    app.add_handler(CommandHandler("deploy", deploy_command))
    app.add_handler(CommandHandler("update", update_command))
    app.add_handler(CommandHandler("shell", shell_command))

    # Media & Text
    app.add_handler(MessageHandler(filters.PHOTO | (filters.Document.IMAGE), handle_photo_or_doc))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(button_callback))
    app.add_error_handler(error_handler)

    # Start lightweight HTTP health-check server for Render / uptime pingers
    import threading
    from http.server import BaseHTTPRequestHandler, HTTPServer

    class _HealthHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"OK")
        def log_message(self, format, *args):
            pass

    port = int(os.environ.get("PORT", 10000))
    threading.Thread(
        target=lambda: HTTPServer(("0.0.0.0", port), _HealthHandler).serve_forever(),
        daemon=True,
    ).start()
    print(f"Health-check server listening on port {port}")

    print("Supercharged Telegram Job Bot running with clean single-instance polling...")
    app.run_polling(
        drop_pending_updates=True,
        bootstrap_retries=-1,
        poll_interval=1.0,
        timeout=30
    )

if __name__ == "__main__":
    main()
