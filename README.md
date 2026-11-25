<div align="center">

# 🤖🤠 Jim Bob — Personal AI Telegram Assistant & Job Automator

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Telegram](https://img.shields.io/badge/Telegram-Bot-26A5E4?style=for-the-badge&logo=telegram&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-Llama%203-F55036?style=for-the-badge&logo=ai&logoColor=white)
![Render](https://img.shields.io/badge/Deploy-Render-46E3B7?style=for-the-badge&logo=render&logoColor=black)

*━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━*

> 💬 *"Back in my day, we mailed paper resumes by carrier pigeon. Now I parse LinkedIn posts over HTTP, run Llama 3 on Groq, and still judge your cover letter."*  
> — **Jim Bob**

</div>

Jim Bob is a **grumpy-but-sharp Telegram bot** built to automate job applications, scrape fresh remote leads, and handle your Git/Vercel/shell chores without complaining (much).

---

## ✨ What Jim Bob Actually Does

| Feature | Description |
| :--- | :--- |
| 📝 **Paste Anything, Get a Draft** | Paste a job description, a LinkedIn post with links, or just a recruiter's email. Extracts company, email, and role across **EN / ES / FR / DE / HI** postings and drafts a tailored email. |
| 🎯 **Smart Resume Routing** | Automatically picks the right resume based on the role (see routing table below). |
| 📸 **Screenshot OCR** | Send a screenshot of a job post—Jim Bob reads it with **EasyOCR** and drafts the application anyway. |
| 🔍 **Live Job Scraping** | Use `/fetch` and `/leads` to pull fresh remote openings and pitch with one tap. |
| ⚡ **Executive Commands** | `/do`, `/git`, `/deploy`, `/shell`, `/mind` — because apparently you can't be trusted to run `git status` yourself. |
| ☁️ **Render-Ready** | Runs a lightweight HTTP health-check server on `$PORT` alongside Telegram polling so free-tier uptime pingers keep him awake. |

---

## 📄 Smart Resume Routing

```text
Incoming Job / Role
 ├── 💼 HR / Talent Roles        ──▶  Joydeep_Das_Resume_HR.pdf
 └── 💻 Full-Stack / AI / UI-UX  ──▶  Joydeep_Das_Full_Stack_AI_Engineer_Resume.pdf
```

---

## 🚀 Quick Setup (Render + Uptime Pinger)

1. 🐙 **Push** this repo to GitHub.
2. ☁️ **Create a New Web Service** on [Render](https://dashboard.render.com) (auto-configured via `render.yaml`).
3. 🔐 **Add your `.env` variables** in Render's **Environment** tab:
   - `TELEGRAM_BOT_TOKEN`
   - `TELEGRAM_ALLOWED_USER_ID`
   - `GMAIL_USER` & `GMAIL_APP_PASSWORD`
   - `GROQ_API_KEY`
4. ⏰ **Keep him awake**: Point [UptimeRobot](https://uptimerobot.com) at `https://<your-app>.onrender.com/` every 5 minutes so Jim Bob doesn't fall asleep on the porch.

---

## 🛠️ Local Run

```bash
pip install -r requirements.txt
python telegram_bot.py
```

---

<div align="center">

*Built with ☕, ⚡, and a mild distrust of manual job boards.*

</div>
