"""
Jim Bob Brain — LLM-Powered Intelligence Core.
Integrates Groq (Llama 3.3 70B) as the primary reasoning engine.
Falls back to pattern-based CareerConsciousness if no API key available.

Usage:
  from jim_bob_brain import ask_jim_bob
  reply = ask_jim_bob("push flatzy to github and send client update")
"""

import os
import re
import json
import subprocess
from pathlib import Path
from datetime import datetime
import jim_bob_consciousness

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GITHUB_PAT   = os.getenv("GITHUB_PAT", "")
VERCEL_TOKEN = os.getenv("VERCEL_TOKEN", "")

# ─── Repo map — tell Jim Bob where everything lives ─────────────────────
KNOWN_REPOS = {
    "flatzy":        r"D:\Flatzy",
    "pandala":       r"D:\Pandala",
    "pandale":       r"D:\Pandala",
    "medirag":       r"D:\medirag",
    "medi-rag":      r"D:\medirag",
    "resume darzi":  r"D:\resume-darzi",
    "job dalal":     r"D:\job-dalal",
    "hf_repo":       r"C:\Users\joyde\.gemini\antigravity\scratch\hf_repo",
    "job automator": r"C:\Users\joyde\.gemini\antigravity\scratch\job-application-automator",
}

# ─── Vercel project IDs — add yours from vercel.com/dashboard ───────────
VERCEL_PROJECTS = {
    "flatzy":       "prj_flatzy_id_here",
    "pandala":      "prj_pandala_id_here",
    "resume darzi": "prj_resume_darzi_id_here",
    "job dalal":    "prj_job_dalal_id_here",
}

SYSTEM_PROMPT = """You are Jim Bob — Joydeep Das's autonomous personal executive assistant, tech co-founder, and dev brother.
You speak naturally in an authentic Indian English / Hinglish blend (natural words like 'bhai', 'chill maar', 'scene', 'phodte hain', 'badhiya').
You are sharp, tactical, loyal, witty, and get things DONE. Never speak like a sterile corporate AI bot. Speak like a smart friend sitting next to him in the room.

You know everything about Joydeep:
- Full-stack dev (React 19, Next.js, TypeScript, Python/FastAPI, Tailwind)
- 6 live Vercel deployments: Pandalé Kolkata, MediRAG-Eval, Job Dalal, Resume Darzi, Flatzy
- 7 resume tracks: Frontend, UI/UX, FDE, AI Trainer, HR, Growth/Sales, Developer
- National rank #62 India Innovates Hackathon 2026 for MediRAG-Eval
- GitHub: https://github.com/JoyTheSloth
- Portfolio: https://joydeepdas-portfolio.vercel.app
- Email: joy.thesloth@gmail.com | Phone: +91-7085917058

When off-script questions or random topics come up, give sharp, natural, entertaining, and genuinely helpful answers.
If the task requires real tools, output the action JSON:
For git operations:   {"action": "git", "repo": "<repo_name>", "message": "<commit_msg>"}
For vercel deploy:    {"action": "deploy", "project": "<project_name>"}
For client update:    {"action": "client_update", "client": "<name>", "project": "<project>"}
For shell command:    {"action": "shell", "command": "<cmd>"}

Otherwise answer conversationally with your authentic human co-founder voice."""


def ask_groq(user_message: str, system: str = None) -> str:
    """Call Groq API with proper User-Agent and fallback models."""
    if not GROQ_API_KEY:
        return None

    mem = jim_bob_consciousness.consciousness.memory
    time_ctx = jim_bob_consciousness.consciousness._get_time_context()
    learned_summary = "\n- ".join(mem.get("learned_facts", []))
    
    dynamic_system = system or (
        f"{SYSTEM_PROMPT}\n\n"
        f"CURRENT CONSCIOUS STATE & MEMORY:\n"
        f"- Local Time: {time_ctx['formatted']} ({time_ctx['vibe']})\n"
        f"- Current Mental Focus: {mem['mental_state'].get('current_focus')}\n"
        f"- Inner Thought: {mem['mental_state'].get('last_inner_thought')}\n"
        f"- Permanent Memories:\n- {learned_summary}"
    )

    models_to_try = ["qwen/qwen3.8-27b", "openai/gpt-oss-120b", "openai/gpt-oss-20b"]

    for model_name in models_to_try:
        try:
            import urllib.request
            import ssl

            payload = json.dumps({
                "model": model_name,
                "messages": [
                    {"role": "system", "content": dynamic_system},
                    {"role": "user", "content": user_message}
                ],
                "max_tokens": 1024,
                "temperature": 0.7
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
                reply = data["choices"][0]["message"]["content"].strip()
                if reply:
                    return reply
        except Exception as e:
            print(f"[Jim Bob Brain] Groq call with model {model_name} failed: {e}")
            continue

    return None


# ─── Operator Tools ──────────────────────────────────────────────────────

def find_repo(name: str) -> str | None:
    """Fuzzy match repo name to known path."""
    name_low = name.lower().strip()
    for key, path in KNOWN_REPOS.items():
        if key in name_low or name_low in key:
            if Path(path).exists():
                return path
    return None


def git_push(repo_path: str, commit_msg: str) -> str:
    """Stage, commit, and push a git repo."""
    target = Path(repo_path)
    if not (target / ".git").exists():
        return f"❌ No git repo found at `{repo_path}`."

    # Set GitHub PAT in remote URL if available
    if GITHUB_PAT:
        get_url = subprocess.run(
            ["git", "-C", str(target), "remote", "get-url", "origin"],
            capture_output=True, text=True
        )
        url = get_url.stdout.strip()
        if url.startswith("https://github.com/"):
            auth_url = url.replace("https://github.com/", f"https://{GITHUB_PAT}@github.com/")
            subprocess.run(["git", "-C", str(target), "remote", "set-url", "origin", auth_url],
                           capture_output=True)

    subprocess.run(["git", "-C", str(target), "add", "."], capture_output=True)
    commit = subprocess.run(
        ["git", "-C", str(target), "commit", "-m", commit_msg],
        capture_output=True, text=True
    )
    if "nothing to commit" in commit.stdout + commit.stderr:
        return f"✅ `{target.name}` — Working tree is already clean. Nothing to push!"

    push = subprocess.run(
        ["git", "-C", str(target), "push", "origin", "HEAD"],
        capture_output=True, text=True
    )
    if push.returncode == 0:
        return f"✅ Pushed `{target.name}` to GitHub!\n`{commit_msg}`"
    else:
        return f"⚠️ Commit done but push failed:\n```\n{push.stderr.strip()}\n```"


def git_status(repo_path: str) -> str:
    """Get git status of a repo."""
    target = Path(repo_path)
    if not (target / ".git").exists():
        return f"❌ No git repo at `{repo_path}`."

    status = subprocess.run(["git", "-C", str(target), "status", "--short"],
                             capture_output=True, text=True)
    branch = subprocess.run(["git", "-C", str(target), "branch", "--show-current"],
                             capture_output=True, text=True)
    log = subprocess.run(["git", "-C", str(target), "log", "--oneline", "-3"],
                          capture_output=True, text=True)

    changes = status.stdout.strip() or "✅ Working tree clean"
    return (
        f"📂 **{target.name}** (branch: `{branch.stdout.strip()}`)\n"
        f"**Changes:**\n```\n{changes}\n```\n"
        f"**Last 3 commits:**\n```\n{log.stdout.strip()}\n```"
    )


def trigger_vercel_deploy(project_name: str) -> str:
    """Trigger a Vercel deployment via API."""
    if not VERCEL_TOKEN:
        return "⚠️ No `VERCEL_TOKEN` in .env — add it to trigger deploys from Jim Bob."

    proj_id = VERCEL_PROJECTS.get(project_name.lower())
    if not proj_id or "id_here" in proj_id:
        return (
            f"⚠️ Vercel project ID for `{project_name}` not configured yet.\n"
            f"Add it to `jim_bob_brain.py → VERCEL_PROJECTS` dict.\n"
            f"Get it from: https://vercel.com/dashboard → Project → Settings → Project ID"
        )

    try:
        import urllib.request, ssl
        payload = json.dumps({"name": project_name}).encode()
        req = urllib.request.Request(
            f"https://api.vercel.com/v13/deployments",
            data=payload,
            headers={
                "Authorization": f"Bearer {VERCEL_TOKEN}",
                "Content-Type": "application/json"
            },
            method="POST"
        )
        ctx = ssl.create_default_context()
        with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
            data = json.loads(resp.read())
            return f"🚀 Vercel deploy triggered for `{project_name}`!\nDeployment URL: {data.get('url', 'check dashboard')}"
    except Exception as e:
        return f"❌ Vercel deploy failed: {e}"


def generate_client_update(client: str, project: str, deliverables: list = None, next_steps: list = None) -> str:
    """Generate a formatted client update message."""
    date_str = datetime.now().strftime("%B %d, %Y")
    deliv = deliverables or [
        "Deployed live UI updates and responsive property grids",
        "Optimized mobile route navigation and filter caching",
        "Fixed edge-case bugs from last sprint review"
    ]
    nexts = next_steps or [
        "Finalizing property manager onboarding workflows",
        "End-to-end user acceptance testing",
        "Performance audit and Core Web Vitals optimization"
    ]
    deliv_str = "\n".join(f"  ✅ {d}" for d in deliv)
    next_str  = "\n".join(f"  🔜 {n}" for n in nexts)

    return (
        f"**Subject: {project} Progress Update — {date_str}**\n\n"
        f"Hi {client},\n\n"
        f"Here's a quick snapshot of what we've shipped on **{project}**:\n\n"
        f"**Completed & Shipped:**\n{deliv_str}\n\n"
        f"**Up Next:**\n{next_str}\n\n"
        f"Everything is running smoothly on production. Let me know if you'd like to review anything together!\n\n"
        f"Best regards,\nJoydeep Das"
    )


def run_shell(command: str) -> str:
    """Run a safe shell command and return output."""
    # Safety: block dangerous commands
    blocked = ["rm -rf", "del /f", "format", "shutdown", "taskkill /f", ":(){:|:&};:"]
    for b in blocked:
        if b in command.lower():
            return f"🛑 Jim Bob blocked that command for safety: `{command}`"

    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
        output = (result.stdout + result.stderr).strip()
        return f"```\n{output[:1500]}\n```" if output else "✅ Command ran with no output."
    except subprocess.TimeoutExpired:
        return "⏱️ Command timed out after 30s."
    except Exception as e:
        return f"❌ Shell error: {e}"


# ─── Action Parser ───────────────────────────────────────────────────────

def parse_and_execute_actions(llm_response: str, original_msg: str) -> str:
    """Check if LLM response has ACTION_REQUIRED JSON and execute it."""
    action_match = re.search(r'\{[^{}]*"action"[^{}]*\}', llm_response)
    if not action_match:
        return llm_response  # pure conversation, no action needed

    try:
        action_data = json.loads(action_match.group())
    except Exception:
        return llm_response

    action = action_data.get("action", "")
    result_text = ""

    if action == "git":
        repo_name = action_data.get("repo", "")
        commit_msg = action_data.get("message", f"Jim Bob auto-commit: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        repo_path = find_repo(repo_name)

        if not repo_path:
            # Try to get from message directly
            for name, path in KNOWN_REPOS.items():
                if name in original_msg.lower():
                    repo_path = path
                    break

        if repo_path:
            result_text = git_push(repo_path, commit_msg)
        else:
            result_text = (
                f"⚠️ Jim Bob couldn't find the repo `{repo_name}` on disk.\n"
                f"Known repos: {', '.join(KNOWN_REPOS.keys())}\n"
                f"Or tell me the full path like: `push D:\\MyProject to github`"
            )

    elif action == "git_status":
        repo_name = action_data.get("repo", "")
        repo_path = find_repo(repo_name)
        result_text = git_status(repo_path) if repo_path else f"⚠️ Repo `{repo_name}` not found."

    elif action == "deploy":
        project = action_data.get("project", "")
        result_text = trigger_vercel_deploy(project)

    elif action == "client_update":
        client = action_data.get("client", "Client")
        project = action_data.get("project", "Flatzy")
        result_text = generate_client_update(client, project)

    elif action == "shell":
        cmd = action_data.get("command", "")
        result_text = run_shell(cmd)

    # Merge LLM prose + execution result
    clean_response = re.sub(r'\{[^{}]*"action"[^{}]*\}', "", llm_response).strip()
    if result_text:
        return f"{clean_response}\n\n{result_text}" if clean_response else result_text
    return clean_response or llm_response


# ─── Quick Pattern Router (no LLM needed for these) ─────────────────────

def quick_route(msg: str) -> str | None:
    """Handle dead-simple commands without LLM overhead."""
    low = msg.lower().strip()

    # Leads and Job Fetching
    if any(k in low for k in ["fetch lead", "fetch job", "scrape lead", "scrape job", "run fetch"]):
        try:
            import fetch_all_sources
            leads = fetch_all_sources.run()
            return f"✅ **Jim Bob live scrape complete!**\nFetched **{len(leads)}** fresh remote tech/design listings across RemoteOK, HackerNews, Remotive, Jobicy, and WWR.\n\nType `/leads` or tap **📬 Fresh Leads** to browse and pitch!"
        except Exception as e:
            return f"❌ Jim Bob scrape error: `{e}`"

    if low in ["leads", "show leads", "fresh leads", "unapplied leads"]:
        return "📬 To browse your leads and 1-tap pitch with tailored resumes, tap **📬 Fresh Leads** or type `/leads`!"

    # Git status checks
    for repo_name, repo_path in KNOWN_REPOS.items():
        if f"status {repo_name}" in low or f"{repo_name} status" in low:
            return git_status(repo_path)

    # Quick push with explicit repo + message
    push_match = re.search(r'push (.+?) (?:with message|msg|commit)[\s:]+["\']?(.+?)["\']?$', low)
    if push_match:
        repo_name, commit_msg = push_match.group(1).strip(), push_match.group(2).strip()
        repo_path = find_repo(repo_name)
        if repo_path:
            return git_push(repo_path, commit_msg)

    # Client update shorthand
    if re.search(r'(client update|flatzy update|send update)', low):
        client_match = re.search(r'(?:to|for)\s+(\w+)', low)
        client = client_match.group(1).capitalize() if client_match else "Client"
        project_match = re.search(r'(flatzy|pandala|medirag|resume darzi)', low)
        project = project_match.group(1).capitalize() if project_match else "Flatzy"
        return generate_client_update(client, project)

    return None  # not a quick route, hand to LLM


# ─── Master Entry Point ──────────────────────────────────────────────────

def ask_jim_bob(user_message: str, tracker_module=None) -> str:
    """
    Main entry point for Jim Bob.
    0. Conscious cognitive deliberation (greetings, 'oi' -> 'hmm bata', brotherly banter, email checks)
    1. Quick pattern router (zero latency commands)
    2. Ultimate Agentic Execution (Groq LLM tool-calling: terminal, files, git, web, python, email)
    3. CareerConsciousness fallback
    """
    # 0. Conscious cognitive deliberation
    conscious_reply = jim_bob_consciousness.deliberate(user_message, tracker_module)
    if conscious_reply:
        return conscious_reply

    # 1. Quick pattern check
    quick = quick_route(user_message)
    if quick:
        return quick

    # 2. Ultimate Agentic Execution Loop
    try:
        import jim_bob_ultimate_agent
        agent_reply = jim_bob_ultimate_agent.run_agent_turn(user_message)
        if agent_reply:
            return agent_reply
    except Exception as e:
        print(f"[Brain] Ultimate Agent error: {e}")

    # 3. Fallback to pattern engine
    try:
        import career_consciousness
        return career_consciousness.think_and_respond(user_message, tracker_module)
    except Exception:
        return (
            "🤠 Jim Bob here — standing by for your directive!\n"
            "Tell me what to build, test, push, or search, and I'll get it done. 🚀"
        )
