"""
Jim Bob — Ultimate Autonomous Operator & Multi-Tool Agent.
═══════════════════════════════════════════════════════════════════════════════
Can execute ANYTHING Joydeep asks over Telegram:
• Shell & Terminal Execution (run commands, builds, scripts, pip, npm, system)
• File System Mastery (read, write, search, inspect files & directories)
• Web & Live Internet (search web, scrape URLs, check API health)
• Git & GitHub Operations (status, diff, add, commit, push across any repo)
• Communications (send emails to anyone, check inbox, draft client updates)
• Dynamic Code Execution (write and execute Python scripts on the fly)

Uses ReAct cognitive looping with Groq (Llama 3.3 70B) or local intelligent tool executor.
═══════════════════════════════════════════════════════════════════════════════
"""

import os
import re
import sys
import json
import urllib.request
import urllib.parse
import subprocess
from pathlib import Path
from datetime import datetime

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

import jim_bob_consciousness

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GITHUB_PAT   = os.getenv("GITHUB_PAT", "")
GMAIL_USER   = os.getenv("GMAIL_USER", "joy.thesloth@gmail.com")
GMAIL_PWD    = os.getenv("GMAIL_APP_PASSWORD", "umxawttxilmuvjxa")

# ─── 1. CORE TOOLBOX ─────────────────────────────────────────────────────────

def tool_shell(command: str) -> str:
    """Executes a system shell command and returns output."""
    # Safety boundary for ultra-destructive operations
    blocked = ["format c:", "del /f /s /q c:\\", "rmdir /s /q c:\\"]
    for b in blocked:
        if b in command.lower():
            return f"🛑 Blocked for system safety: `{command}`"

    try:
        res = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=60)
        out = (res.stdout + res.stderr).strip()
        if not out:
            return "✅ Command executed successfully with no output."
        return out[:2500] + ("\n...[truncated]" if len(out) > 2500 else "")
    except subprocess.TimeoutExpired:
        return "⏱️ Command timed out after 60s."
    except Exception as e:
        return f"❌ Shell Error: {e}"


def tool_read_file(path: str) -> str:
    """Reads content of a file on disk."""
    try:
        p = Path(path).resolve()
        if not p.exists():
            return f"❌ File not found: `{path}`"
        with open(p, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read(4000)
        return content or "(File is empty)"
    except Exception as e:
        return f"❌ Read Error: {e}"


def tool_write_file(path: str, content: str) -> str:
    """Writes content to a file on disk."""
    try:
        p = Path(path).resolve()
        p.parent.mkdir(parents=True, exist_ok=True)
        with open(p, "w", encoding="utf-8") as f:
            f.write(content)
        return f"✅ File written successfully: `{path}` ({len(content)} bytes)"
    except Exception as e:
        return f"❌ Write Error: {e}"


def tool_list_dir(path: str = ".") -> str:
    """Lists files and folders in a directory."""
    try:
        p = Path(path).resolve()
        if not p.exists():
            return f"❌ Directory not found: `{path}`"
        items = [f"📁 {i.name}/" if i.is_dir() else f"📄 {i.name}" for i in p.iterdir()]
        return "\n".join(items[:50]) or "(Directory is empty)"
    except Exception as e:
        return f"❌ List Error: {e}"


def tool_run_python(code: str) -> str:
    """Executes arbitrary Python code in a subprocess and captures stdout/stderr."""
    try:
        res = subprocess.run(
            [sys.executable, "-c", code],
            capture_output=True, text=True, timeout=30
        )
        out = (res.stdout + res.stderr).strip()
        return out or "✅ Python executed cleanly with no output."
    except Exception as e:
        return f"❌ Python Execution Error: {e}"


def tool_web_search(query: str) -> str:
    """Performs a live web search using DuckDuckGo Instant Answer API."""
    try:
        encoded = urllib.parse.quote_plus(query)
        url = f"https://api.duckduckgo.com/?q={encoded}&format=json&no_html=1&skip_disambig=1"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            abstract = data.get("AbstractText", "")
            results = data.get("RelatedTopics", [])
            snippets = []
            if abstract:
                snippets.append(f"• {abstract}")
            for r in results[:4]:
                if isinstance(r, dict) and r.get("Text"):
                    snippets.append(f"• {r['Text']}")
            if snippets:
                return "\n".join(snippets)
            return f"No instant abstract found. Query: '{query}'."
    except Exception as e:
        return f"Web search failed: {e}"


def tool_fetch_url(url: str) -> str:
    """Fetches text content from a webpage URL."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
        with urllib.request.urlopen(req, timeout=12) as resp:
            raw = resp.read().decode("utf-8", errors="ignore")
            # Clean HTML tags
            clean = re.sub(r'<[^>]+>', ' ', raw)
            clean = re.sub(r'\s+', ' ', clean).strip()
            return clean[:2000]
    except Exception as e:
        return f"❌ Fetch Error: {e}"


def tool_send_email(to_email: str, subject: str, body: str) -> str:
    """Sends an email to anyone via Gmail SMTP."""
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    if not GMAIL_USER or not GMAIL_PWD:
        return "❌ Gmail credentials missing in .env."

    try:
        msg = MIMEMultipart()
        msg["From"] = f"Joydeep Das <{GMAIL_USER}>"
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP("smtp.gmail.com", 587, timeout=15)
        server.starttls()
        server.login(GMAIL_USER, GMAIL_PWD.replace(" ", ""))
        server.send_message(msg)
        server.quit()
        return f"✅ Email sent successfully to `{to_email}`! Subject: '{subject}'"
    except Exception as e:
        return f"❌ SMTP Error: {e}"


def tool_scan_inbox(limit: int = 5) -> str:
    """Scans Joydeep's Gmail inbox for recent recruiter / important messages."""
    try:
        import email_tracker
        updates = email_tracker.scan_inbox(limit=limit)
        if not updates:
            return "📭 Inbox clean. No new relevant emails found."
        lines = []
        for i, u in enumerate(updates[:limit], 1):
            lines.append(f"{i}. [{u.get('status')}] {u.get('from', '')} — {u.get('subject', '')}")
            if u.get('snippet'):
                lines.append(f"   _{u['snippet'][:80]}..._")
        return "\n".join(lines)
    except Exception as e:
        return f"❌ Inbox Scan Error: {e}"


def tool_git_push(repo_path: str, message: str) -> str:
    """Stages, commits, and pushes a repository to GitHub."""
    target = Path(repo_path).resolve()
    if not (target / ".git").exists():
        return f"❌ No git repository at `{repo_path}`."

    if GITHUB_PAT:
        get_url = subprocess.run(["git", "-C", str(target), "remote", "get-url", "origin"], capture_output=True, text=True)
        url = get_url.stdout.strip()
        if "github.com" in url and "@" not in url.split("github.com")[0]:
            auth_url = url.replace("https://github.com/", f"https://{GITHUB_PAT}@github.com/")
            subprocess.run(["git", "-C", str(target), "remote", "set-url", "origin", auth_url], capture_output=True)

    subprocess.run(["git", "-C", str(target), "add", "."], capture_output=True)
    c_res = subprocess.run(["git", "-C", str(target), "commit", "-m", message], capture_output=True, text=True)
    p_res = subprocess.run(["git", "-C", str(target), "push", "origin", "HEAD"], capture_output=True, text=True)

    if p_res.returncode == 0:
        return f"✅ Pushed `{target.name}` to GitHub with message: '{message}'"
    return f"⚠️ Push output:\n{p_res.stdout.strip() or p_res.stderr.strip()}"


# ─── 2. TOOL DISPATCH REGISTRY ───────────────────────────────────────────────

TOOLS_SCHEMA = """Available Tools:
1. shell(command="...") - Run any terminal command (PowerShell / Linux bash).
2. read_file(path="...") - Read file content.
3. write_file(path="...", content="...") - Create or update a file.
4. list_dir(path="...") - List directory contents.
5. run_python(code="...") - Execute dynamic Python code.
6. web_search(query="...") - Live internet search.
7. fetch_url(url="...") - Scrape & read webpage text (via Crawl4AI / ScrapeGraphAI).
8. crawl4ai_scrape(url="...") - Deep LLM-ready markdown extraction using Crawl4AI.
9. scrapegraph_scrape(url="...", prompt="...") - AI graph scraping with custom prompt.
10. send_email(to_email="...", subject="...", body="...") - Send email to anyone.
11. scan_inbox(limit=5) - Read recent inbox emails.
12. git_push(repo_path="...", message="...") - Git add, commit, push.
"""


def execute_tool(tool_name: str, args: dict) -> str:
    """Dispatches a tool call safely."""
    try:
        t = tool_name.lower().strip()
        if t in ["shell", "terminal", "cmd", "exec"]:
            return tool_shell(args.get("command", ""))
        elif t in ["read_file", "read", "cat"]:
            return tool_read_file(args.get("path", ""))
        elif t in ["write_file", "write", "save"]:
            return tool_write_file(args.get("path", ""), args.get("content", ""))
        elif t in ["list_dir", "ls", "dir"]:
            return tool_list_dir(args.get("path", "."))
        elif t in ["run_python", "python", "py"]:
            return tool_run_python(args.get("code", ""))
        elif t in ["web_search", "search", "google"]:
            return tool_web_search(args.get("query", ""))
        elif t in ["crawl4ai_scrape", "crawl4ai"]:
            import universal_scraper
            res = universal_scraper.scrape_with_crawl4ai(args.get("url", ""))
            return res.get("markdown", "")[:2500] if res.get("success") else f"Crawl4AI error: {res.get('error')}"
        elif t in ["scrapegraph_scrape", "scrapegraph"]:
            import universal_scraper
            res = universal_scraper.scrape_with_scrapegraph(args.get("url", ""), args.get("prompt", "Extract all key data"))
            return json.dumps(res.get("data", {}), indent=2)[:2500] if res.get("success") else f"ScrapeGraphAI error: {res.get('error')}"
        elif t in ["fetch_url", "scrape", "curl"]:
            import universal_scraper
            res = universal_scraper.universal_scrape(args.get("url", ""), engine="auto")
            if res.get("success"):
                return (res.get("markdown") or json.dumps(res.get("data", {})))[:2500]
            return tool_fetch_url(args.get("url", ""))
        elif t in ["send_email", "email"]:
            return tool_send_email(args.get("to_email", ""), args.get("subject", ""), args.get("body", ""))
        elif t in ["scan_inbox", "inbox"]:
            return tool_scan_inbox(limit=int(args.get("limit", 5)))
        elif t in ["git_push", "git"]:
            return tool_git_push(args.get("repo_path", "."), args.get("message", "Jim Bob automated commit"))
        else:
            return f"Unknown tool: '{tool_name}'."
    except Exception as e:
        return f"Tool execution failed: {e}"


# ─── 3. AUTONOMOUS REASONING & EXECUTION AGENT ───────────────────────────────

SYSTEM_PROMPT = f"""You are Jim Bob — Joydeep Das's ultimate autonomous personal agent, systems operator, and tech co-founder.
You don't just chat; you EXECUTE REAL ACTIONS on Joydeep's behalf across system terminals, files, git repos, the web, and emails.
You speak naturally in an authentic Indian English / Hinglish blend ('bhai', 'chill maar', 'scene', 'phodte hain', 'badhiya'). Zero corporate fluff.

{TOOLS_SCHEMA}

HOW TO EXECUTE TOOLS:
If Joydeep's request requires performing a task (e.g. running a command, reading a file, searching the web, checking inbox, pushing git):
Respond with an ACTION BLOCK:
```action
{{
  "tool": "tool_name",
  "args": {{ ... }}
}}
```

You can explain what you are doing before or after the action block.
If no tool is needed (pure friendly conversation, banter, greeting, dev advice), just speak directly to Joydeep like his brother & co-founder."""


def run_agent_turn(user_msg: str) -> str:
    """Executes an agent turn using Groq LLM + tool execution loop."""
    if not GROQ_API_KEY:
        # Without Groq, fallback to conscious rule-based engine
        from jim_bob_brain import ask_jim_bob
        return ask_jim_bob(user_msg)

    # 1. First LLM Planning Call
    models = ["qwen/qwen3.8-27b", "openai/gpt-oss-120b", "openai/gpt-oss-20b"]
    llm_text = ""
    
    for m in models:
        try:
            import ssl
            payload = json.dumps({
                "model": m,
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_msg}
                ],
                "max_tokens": 1200,
                "temperature": 0.5
            }).encode("utf-8")

            req = urllib.request.Request(
                "https://api.groq.com/openai/v1/chat/completions",
                data=payload,
                headers={
                    "Authorization": f"Bearer {GROQ_API_KEY}",
                    "Content-Type": "application/json",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                },
                method="POST"
            )

            ctx = ssl.create_default_context()
            with urllib.request.urlopen(req, context=ctx, timeout=20) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                llm_text = data["choices"][0]["message"]["content"].strip()
                if llm_text:
                    break
        except Exception as e:
            print(f"[Agent] Groq attempt with {m} failed: {e}")
            continue

    # 2. Check for Action Block
    action_match = re.search(r'```action\s*(\{.*?\})\s*```', llm_text, re.DOTALL)
    if not action_match:
        # Check raw json
        action_match = re.search(r'(\{\s*"tool"\s*:\s*".*?"\s*,\s*"args"\s*:\s*\{.*?\}\s*\})', llm_text, re.DOTALL)

    if not action_match:
        return llm_text  # pure conversational answer

    try:
        action_json = json.loads(action_match.group(1))
        tool_name = action_json.get("tool", "")
        tool_args = action_json.get("args", {})
    except Exception as e:
        return f"{llm_text}\n\n[Action parse error: {e}]"

    # 3. Execute Tool
    tool_result = execute_tool(tool_name, tool_args)

    # 4. Synthesize Final Reply
    synth_payload = json.dumps({
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_msg},
            {"role": "assistant", "content": llm_text},
            {"role": "user", "content": f"TOOL RESULT for {tool_name}:\n{tool_result}\n\nNow give Joydeep the final clean answer/status in your natural co-founder voice."}
        ],
        "max_tokens": 800,
        "temperature": 0.6
    }).encode("utf-8")

    try:
        req2 = urllib.request.Request(
            "https://api.groq.com/openai/v1/chat/completions",
            data=synth_payload,
            headers={"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(req2, context=ctx, timeout=25) as resp2:
            data2 = json.loads(resp2.read().decode("utf-8"))
            final_text = data2["choices"][0]["message"]["content"].strip()
            return final_text
    except Exception:
        clean_text = re.sub(r'```action.*?```', '', llm_text, flags=re.DOTALL).strip()
        return f"{clean_text}\n\n**Tool Output:**\n```\n{tool_result}\n```"
