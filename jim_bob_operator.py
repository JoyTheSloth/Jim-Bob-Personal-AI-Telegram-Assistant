"""
Autonomous Operator Engine: Jim Bob Personal Executive Assistant.
Handles tasks across:
1. Git & GitHub Operations (status, stage, commit, push, branch verification)
2. Client Communications & Updates (Flatzy client reports, release notes, progress alerts)
3. Job Application Outbound & Recruiter Outreach (multi-track resumes, automated dispatch)
4. System & Workspace Automation (file checks, command execution, reporting)
"""

import os
import subprocess
import json
from pathlib import Path
from datetime import datetime

class JimBobOperator:
    def __init__(self):
        self.name = "Jim Bob"
        self.role = "Autonomous Executive AI Assistant & Operator"

    # --- 1. Git & GitHub Operations ---
    def git_status(self, repo_path: str = None) -> dict:
        """Inspects git status of a local repository."""
        target = Path(repo_path) if repo_path else Path.cwd()
        if not (target / ".git").exists():
            return {"success": False, "error": f"No git repository found at {target}"}

        res = subprocess.run(["git", "-C", str(target), "status", "--short"], capture_output=True, text=True)
        branch = subprocess.run(["git", "-C", str(target), "branch", "--show-current"], capture_output=True, text=True)
        return {
            "success": True,
            "branch": branch.stdout.strip(),
            "changes": res.stdout.strip() or "Working tree clean."
        }

    def git_commit_and_push(self, repo_path: str, message: str, branch: str = "main") -> dict:
        """Stages all changes, creates a commit, and pushes to remote."""
        target = Path(repo_path)
        if not (target / ".git").exists():
            return {"success": False, "error": f"No git repository found at {target}"}

        add_res = subprocess.run(["git", "-C", str(target), "add", "."], capture_output=True, text=True)
        commit_res = subprocess.run(["git", "-C", str(target), "commit", "-m", message], capture_output=True, text=True)
        push_res = subprocess.run(["git", "-C", str(target), "push", "origin", branch], capture_output=True, text=True)

        return {
            "success": push_res.returncode == 0,
            "commit_output": commit_res.stdout.strip(),
            "push_output": push_res.stdout.strip() or push_res.stderr.strip()
        }

    # --- 2. Client & Flatzy Updates ---
    def generate_client_update(self, client_name: str, project_name: str = "Flatzy", deliverables: list = None, next_steps: list = None) -> str:
        """Crafts an executive, professional client update ready to send via WhatsApp, Email, or Slack."""
        deliv_str = "\n".join([f"  ✅ {d}" for d in (deliverables or ["Deployed live UI updates and responsive property grids", "Optimized mobile route navigation and filter caching"])])
        next_str = "\n".join([f"  🔜 {n}" for n in (next_steps or ["Finalizing property manager onboarding workflows", "End-to-end user acceptance testing"])])
        date_str = datetime.now().strftime("%B %d, %Y")

        update_msg = (
            f"Subject: Project Update: {project_name} Progress & Deployment ({date_str})\n\n"
            f"Hi {client_name},\n\n"
            f"Here is a quick snapshot of what we've shipped and deployed on {project_name}:\n\n"
            f"**Completed & Shipped:**\n{deliv_str}\n\n"
            f"**Next in Queue:**\n{next_str}\n\n"
            f"Everything is running smoothly on staging/production. Let me know if you'd like to review any specific component together!\n\n"
            f"Best regards,\nJoydeep Das"
        )
        return update_msg

    # --- 3. Command Dispatch & Task Routing ---
    def handle_intent(self, text: str) -> dict:
        """Routes natural user commands to actions."""
        low = text.lower().strip()

        if "git push" in low or "push to github" in low or "commit and push" in low:
            return {
                "action": "git_push",
                "message": "Jim Bob can stage, commit, and push your repositories directly. Specify the repo path and commit message!"
            }
        elif "client update" in low or "flatzy update" in low:
            draft = self.generate_client_update(client_name="Team / Client", project_name="Flatzy")
            return {
                "action": "client_update",
                "draft": draft,
                "message": "Drafted an executive Flatzy client progress update!"
            }
        return {"action": "chat", "message": "Jim Bob is standing by for your directive."}

operator = JimBobOperator()
