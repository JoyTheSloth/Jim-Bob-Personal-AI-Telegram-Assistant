# Jim Bob — Personal AI Telegram Assistant & Job Automator

> *"Back in my day, we mailed paper resumes by carrier pigeon. Now I parse LinkedIn posts over HTTP, run Llama 3 on Groq, and still judge your cover letter."* — **Jim Bob**

Jim Bob is a grumpy-but-sharp Telegram bot built to automate job applications, scrape fresh remote leads, and handle your Git/Vercel/shell chores without complaining (much).

## What Jim Bob Actually Does

- **Paste Anything, Get a Draft**: Paste a job description, a LinkedIn post with links, or just a recruiter's email address. Jim Bob extracts the company, email, and role—even across English, Spanish, French, German, and Hindi HR postings—and drafts a tailored application.
- **Smart Resume Routing**:
  - **HR / Talent roles** → attaches `Joydeep_Das_Resume_HR.pdf`
  - **Full-Stack / AI / Frontend / UI-UX / Everything else** → attaches `Joydeep_Das_Full_Stack_AI_Engineer_Resume.pdf`
- **Screenshot OCR**: Send a screenshot of a job post and Jim Bob reads it with EasyOCR and drafts the email anyway.
- **Live Job Scraping (`/fetch`, `/leads`)**: Pulls fresh remote openings and lets you pitch with one tap.
- **Executive Commands**: `/do`, `/git`, `/deploy`, `/shell`, `/mind` — because apparently you can't be trusted to run `git status` yourself.
- **Render-Ready**: Runs a lightweight HTTP health-check server on `$PORT` alongside Telegram polling so free-tier uptime pingers keep him awake.

## Quick Setup (Render + Uptime Pinger)

1. Push this repo to GitHub.
2. Create a **New Web Service** on [Render](https://dashboard.render.com) (auto-configured via `render.yaml`).
3. Add your `.env` variables in Render's **Environment** tab:
   - `TELEGRAM_BOT_TOKEN`
   - `TELEGRAM_ALLOWED_USER_ID`
   - `GMAIL_USER` & `GMAIL_APP_PASSWORD`
   - `GROQ_API_KEY`
4. Point [UptimeRobot](https://uptimerobot.com) at `https://<your-app>.onrender.com/` every 5 minutes so Jim Bob doesn't fall asleep on the porch.

## Local Run

```bash
pip install -r requirements.txt
python telegram_bot.py
```
