"""Local Playwright helper to extract hidden emails and auto-fill job application forms.

Run locally (not on Render free tier):
    python auto_apply_playwright.py <job_url> [--hr]
"""
import re
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

PROFILE = {
    "name": "Joydeep Das",
    "email": "joy.thesloth@gmail.com",
    "phone": "+91-7085917058",
    "linkedin": "https://linkedin.com/in/joydeep-das-78123522a",
    "github": "https://github.com/JoyTheSloth",
    "portfolio": "https://joydeepdas-portfolio.vercel.app",
}

def main():
    if len(sys.argv) < 2:
        print("Usage: python auto_apply_playwright.py <job_url> [--hr]")
        sys.exit(1)

    url = sys.argv[1]
    use_hr = "--hr" in sys.argv
    resume_name = "Joydeep_Das_Resume_HR.pdf" if use_hr else "Joydeep_Das_Full_Stack_AI_Engineer_Resume.pdf"
    resume_path = Path(__file__).parent / "resumes_pdf" / resume_name

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(url, wait_until="domcontentloaded", timeout=30000)

        # Extract any visible or mailto emails
        html = page.content()
        emails = sorted(set(re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", html)))
        if emails:
            print("Found emails:", ", ".join(emails[:5]))

        # Best-effort form auto-fill
        field_map = {
            "name": PROFILE["name"],
            "email": PROFILE["email"],
            "phone": PROFILE["phone"],
            "linkedin": PROFILE["linkedin"],
            "github": PROFILE["github"],
            "portfolio": PROFILE["portfolio"],
            "website": PROFILE["portfolio"],
        }
        for key, val in field_map.items():
            for sel in [f"input[name*='{key}' i]", f"input[id*='{key}' i]", f"input[placeholder*='{key}' i]"]:
                loc = page.locator(sel).first
                if loc.count() > 0 and loc.is_visible():
                    loc.fill(val)
                    break

        if resume_path.exists():
            file_input = page.locator("input[type='file']").first
            if file_input.count() > 0:
                file_input.set_input_files(str(resume_path))
                print(f"Attached {resume_name}")

        input("Review the form in the browser and press Enter to close...")
        browser.close()

if __name__ == "__main__":
    main()
