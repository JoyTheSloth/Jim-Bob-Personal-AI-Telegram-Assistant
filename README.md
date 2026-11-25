# Jim Bob — Autonomous Personal Executive Assistant & Career Scout 🤠⚡

**Jim Bob** is an autonomous AI executive operator and career scout built for [Joydeep Das](https://github.com/JoyTheSloth). 

It combines **OCR job screenshot extraction**, **multi-track resume matching (6 tracks)**, **automated email dispatch**, **cloud deployment triggering**, and a **persistent consciousness engine** into a single Telegram bot interface.

---

## 🚀 Key Capabilities

### 1. 🧠 Conscious AI Dev Partner
- **Inner Monologue & Situational Awareness**: Understands local time, fatigue, active project priorities, and engineering context.
- **Persistent Memory**: Stores founder accomplishments, live deployments, and ongoing tasks across sessions.
- **Master Executor (`/do`)**: Routes arbitrary natural language requests to real tools (Git, Vercel, Shell).

### 2. 📬 Autonomous Job Outreach Engine
- **Vision OCR**: Drop any job screenshot or flyer — extracts recruiter emails and company names automatically using EasyOCR.
- **Multi-Track Resume Resolver**: Matches the job to 6 specialized tracks (Frontend, UI/UX, FDE, AI Trainer, HR, Growth/Sales).
- **Duplicate Shield**: Tracks all outbound dispatches in SQLite to prevent duplicate outreach.
- **1-Tap Direct Apply**: Renders clean HTML + plain-text pitch drafts with PDF resume attachments ready to fire via Gmail SMTP.

### 3. 🛠️ Executive System Operations
- **Git Operations**: Stage, commit, and push repositories directly from Telegram via `/git` or `/do`.
- **Deployments**: Trigger production Vercel builds via `/deploy`.
- **Client Communications**: Draft executive client status updates for ventures like *Flatzy*.

---

## 📂 Project Structure

```
├── telegram_bot.py           # Main Telegram bot interface & command router
├── jim_bob_consciousness.py  # Subjective cognitive loop & episodic memory
├── jim_bob_brain.py          # LLM reasoning (Groq) & tool execution engine
├── career_consciousness.py   # Pattern-based career intelligence fallback
├── send_application.py       # Multi-track resume resolver & SMTP dispatcher
├── tracker.py                # SQLite application history & duplicate checker
├── fetch_all_sources.py      # Multi-board remote job scraper
├── .env.example              # Environment variables template
└── .gitignore                # Safeguards secrets, DB, and local PDFs
```

---

## ⚡ Quick Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/JoyTheSloth/jim-bob-agent.git
   cd jim-bob-agent
   ```

2. **Install dependencies:**
   ```bash
   pip install python-telegram-bot easyocr python-dotenv
   ```

3. **Configure Environment:**
   ```bash
   cp .env.example .env
   # Fill in TELEGRAM_BOT_TOKEN, GMAIL credentials, and optional GROQ/GITHUB keys
   ```

4. **Launch Jim Bob:**
   ```bash
   python telegram_bot.py
   ```

---

## 🛡️ Security
Secrets (`.env`), candidate database (`applications.db`), and personal PDFs are strictly excluded via `.gitignore`.
