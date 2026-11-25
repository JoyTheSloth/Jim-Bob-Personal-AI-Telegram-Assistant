import os
import argparse
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path
import tracker

ENV_PATH = Path(__file__).parent / ".env"

def load_env():
    env = {}
    if ENV_PATH.exists():
        with open(ENV_PATH, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    env[k.strip()] = v.strip()
    return env

CONFIG = load_env()

# Directory precedence: First check user OneDrive Res folder, then Resume folder, then local resumes_pdf
ONEDRIVE_RES_DIR = Path(r"C:\Users\joyde\OneDrive\Documents\3-Personal\Res")
ONEDRIVE_RESUME_DIR = Path(r"C:\Users\joyde\OneDrive\Documents\3-Personal\Resume")
LOCAL_RES_DIR = Path(__file__).parent / "resumes_pdf"

def get_resume_path(filename: str, fallback_docx: str = "") -> str:
    od_path = ONEDRIVE_RES_DIR / filename
    if od_path.exists():
        return str(od_path)
    od_res_path = ONEDRIVE_RESUME_DIR / filename
    if od_res_path.exists():
        return str(od_res_path)
    local_path = LOCAL_RES_DIR / filename
    if local_path.exists():
        return str(local_path)
    return fallback_docx

RESUME_MAP = {
    "fde": get_resume_path("Joydeep_Das_FDE_Resume.pdf", CONFIG.get("RESUME_FDE", r"C:\Users\joyde\OneDrive\Documents\3-Personal\Joydeep_Das_FDE_Resume.docx")),
    "frontend": get_resume_path("Joydeep_Das_Frontend_CV.pdf", CONFIG.get("RESUME_FRONTEND", r"C:\Users\joyde\OneDrive\Documents\3-Personal\Joydeep_Das_Frontend_CV.docx")),
    "uiux": get_resume_path("Joydeep_Das_UIUX_CV.pdf", CONFIG.get("RESUME_UIUX", r"C:\Users\joyde\OneDrive\Documents\3-Personal\Joydeep_Das_UIUX_CV.docx")),
    "ai": get_resume_path("Joydeep_Das_AI.pdf", str(LOCAL_RES_DIR / "Joydeep_Das_AI.pdf")),
    "hr": get_resume_path("Joydeep_Das_Resume_HR.pdf", str(LOCAL_RES_DIR / "Joydeep_Das_Resume_HR.pdf")),
    "sales": get_resume_path("ContenNSales.pdf", str(LOCAL_RES_DIR / "ContenNSales.pdf")),
    "developer": get_resume_path("Joydeep_Das_Developer_CV.pdf", str(LOCAL_RES_DIR / "Joydeep_Das_Developer_CV.pdf")),
}

def send_application_email(
    to_email: str,
    subject: str,
    body_plain: str,
    body_html: str = None,
    role_type: str = "fde",
    company_name: str = "Unknown",
    preview_only: bool = False
):
    sender_email = CONFIG.get("GMAIL_USER", "joy.thesloth@gmail.com")
    app_pwd = CONFIG.get("GMAIL_APP_PASSWORD", "").replace(" ", "")
    resume_path = RESUME_MAP.get(role_type.lower(), RESUME_MAP["fde"])

    print("=" * 60)
    print(f"TO: {to_email}")
    print(f"FROM: Joydeep Das <{sender_email}>")
    print(f"SUBJECT: {subject}")
    print(f"ATTACHMENT: {resume_path} (Exists: {os.path.exists(resume_path)})")
    print("-" * 60)
    print(body_plain)
    print("=" * 60)

    if preview_only:
        print("\n[Preview Mode] Email not sent.")
        return

    msg = MIMEMultipart("mixed")
    msg["From"] = f"Joydeep Das <{sender_email}>"
    msg["To"] = to_email
    msg["Subject"] = subject

    alt_part = MIMEMultipart("alternative")
    alt_part.attach(MIMEText(body_plain, "plain", "utf-8"))
    if body_html:
        alt_part.attach(MIMEText(body_html, "html", "utf-8"))
    
    msg.attach(alt_part)

    # Attach PDF resume
    if os.path.exists(resume_path):
        filename = os.path.basename(resume_path)
        with open(resume_path, "rb") as f:
            part = MIMEBase("application", "pdf" if filename.endswith(".pdf") else "octet-stream")
            part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename=\"{filename}\"")
        msg.attach(part)
    else:
        print(f"Warning: Resume file not found at {resume_path}")

    print("Connecting to Gmail SMTP...")
    server = smtplib.SMTP("smtp.gmail.com", 587, timeout=20)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(sender_email, app_pwd)
    server.sendmail(sender_email, to_email, msg.as_string())
    server.quit()
    print(f"\n[SUCCESS] Application email successfully sent to {to_email}!")

    # Log to persistent SQLite tracker
    try:
        tracker.log_application(
            company=company_name,
            recipient_email=to_email,
            role_type=role_type,
            subject=subject,
            resume_file=os.path.basename(resume_path),
            status="Sent"
        )
        print("Logged application to tracking database.")
    except Exception as e:
        print(f"Error logging to tracker: {e}")

def generate_default_bodies(role_type: str, company_name: str, recipient_name: str = "", job_ref: str = ""):
    first_name = recipient_name.strip() if recipient_name else ""
    salutation = f"Hi {first_name}," if first_name else f"Hi {company_name} Team,"
    job_spec = f"for {job_ref}" if job_ref else "on your engineering team"
    github_link = CONFIG.get("GITHUB", "https://github.com/JoyTheSloth")
    portfolio_link = CONFIG.get("PORTFOLIO", "https://joydeepdas-portfolio.vercel.app")
    linkedin_link = CONFIG.get("LINKEDIN", "https://linkedin.com/in/joydeep-das-78123522a")
    resume_link = "Joydeep_Das_Frontend_CV.pdf (attached)"

    if role_type == "uiux":
        plain = f"""{salutation}

Hope your week is going well!

I saw your opening {job_spec} at {company_name}. Given your team's focus on scalable digital experiences and design systems, I wanted to reach out directly.

A quick snapshot of my background:
• Stack: Figma, Design Systems, Typography/Token Scales, User Research, UI/UX Prototyping.
• Impact: Designed Pandalé Kolkata from scratch—driving 7,000+ unique visitors and 31,000+ views in week 1 with an intuitive mobile-first interface.
• Proof: Live production UX for 2GatherApp (Google Play) and interactive Figma libraries: {portfolio_link}.

Resume: Joydeep_Das_UIUX_CV.pdf (attached)
Portfolio: {portfolio_link}

If you feel my profile is a solid match, would you be open to submitting an internal referral or chatting for 10 minutes?

Best regards,
Joydeep Das
UI/UX & Product Designer
Phone: +91-7085917058
Portfolio: {portfolio_link} | LinkedIn: {linkedin_link}
"""
        html = f"""<!DOCTYPE html>
<html>
<body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; font-size: 15px; line-height: 1.65; color: #1e293b; max-width: 600px; margin: 0 auto; padding: 20px 0;">
  <p>{salutation}</p>
  <p>Hope your week is going well!</p>
  <p>I saw your opening {job_spec} at <strong>{company_name}</strong>. Given your team's focus on scalable digital experiences and design systems, I wanted to reach out directly.</p>
  <p style="margin-bottom: 6px;"><strong>A quick snapshot of my background:</strong></p>
  <ul style="padding-left: 20px; margin-top: 0; margin-bottom: 18px;">
    <li style="margin-bottom: 6px;"><strong>Stack:</strong> Figma, Design Systems, Typography/Token Scales, User Research, UI/UX Prototyping.</li>
    <li style="margin-bottom: 6px;"><strong>Impact:</strong> Designed Pandalé Kolkata from scratch—driving 7,000+ unique visitors and 31,000+ views in week 1 with an intuitive mobile-first interface.</li>
    <li style="margin-bottom: 6px;"><strong>Proof:</strong> Live production UX for 2GatherApp (Google Play) and interactive Figma libraries on my <a href="{portfolio_link}" style="color: #2563eb; text-decoration: none;">Portfolio</a>.</li>
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
    elif role_type == "frontend":
        plain = f"""{salutation}

Hope your week is going well!

I saw your opening {job_spec} at {company_name}. Given your team's focus on scalable user experience and high-performance frontends, I wanted to reach out directly.

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
        html = f"""<!DOCTYPE html>
<html>
<body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; font-size: 15px; line-height: 1.65; color: #1e293b; max-width: 600px; margin: 0 auto; padding: 20px 0;">
  <p>{salutation}</p>
  <p>Hope your week is going well!</p>
  <p>I saw your opening {job_spec} at <strong>{company_name}</strong>. Given your team's focus on scalable user experience and high-performance frontends, I wanted to reach out directly.</p>
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
    else:  # FDE / Full-Stack
        plain = f"""{salutation}

Hope your week is going well!

I saw your opening {job_spec} at {company_name}. Given your team's focus on rapid customer-facing delivery and robust AI systems, I wanted to reach out directly.

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
        html = f"""<!DOCTYPE html>
<html>
<body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; font-size: 15px; line-height: 1.65; color: #1e293b; max-width: 600px; margin: 0 auto; padding: 20px 0;">
  <p>{salutation}</p>
  <p>Hope your week is going well!</p>
  <p>I saw your opening {job_spec} at <strong>{company_name}</strong>. Given your team's focus on rapid customer-facing delivery and robust AI systems, I wanted to reach out directly.</p>
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
    return plain, html

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Send customized job application email with resume attachment.")
    parser.add_argument("--to", required=True, help="Recipient email address")
    parser.add_argument("--subject", required=True, help="Email subject line")
    parser.add_argument("--role", default="fde", choices=["fde", "frontend", "uiux"], help="Role type (fde, frontend, uiux)")
    parser.add_argument("--company", default="Company", help="Company Name")
    parser.add_argument("--body-file", help="Path to text or html body file")
    parser.add_argument("--preview", action="store_true", help="Print preview without sending")
    args = parser.parse_args()

    plain_body, html_body = generate_default_bodies(args.role, args.company)
    if args.body_file and os.path.exists(args.body_file):
        with open(args.body_file, "r", encoding="utf-8") as f:
            plain_body = f.read()
            html_body = None

    send_application_email(
        to_email=args.to,
        subject=args.subject,
        body_plain=plain_body,
        body_html=html_body,
        role_type=args.role,
        company_name=args.company,
        preview_only=args.preview
    )
