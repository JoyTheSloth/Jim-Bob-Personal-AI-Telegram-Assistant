import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

RESUMES = {
    "fde": r"C:\Users\joyde\OneDrive\Documents\3-Personal\Joydeep_Das_FDE_Resume.docx",
    "frontend": r"C:\Users\joyde\OneDrive\Documents\3-Personal\Joydeep_Das_Frontend_CV.docx",
    "uiux": r"C:\Users\joyde\OneDrive\Documents\3-Personal\Joydeep_Das_UIUX_CV.docx"
}

def send_job_email(
    to_email: str,
    subject: str,
    body_text: str,
    role_type: str = "fde",
    sender_email: str = "joydeepdasoffical2003@gmail.com",
    app_password: str = None
):
    if not app_password:
        app_password = os.getenv("GMAIL_APP_PASSWORD")
    if not app_password:
        raise ValueError("GMAIL_APP_PASSWORD is not provided.")

    msg = MIMEMultipart()
    msg["From"] = f"Joydeep Das <{sender_email}>"
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body_text, "plain"))

    # Resolve resume attachment
    resume_path = RESUMES.get(role_type.lower(), RESUMES["fde"])
    if os.path.exists(resume_path):
        filename = os.path.basename(resume_path)
        with open(resume_path, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {filename}",
        )
        msg.attach(part)
    else:
        print(f"Warning: Resume file not found at {resume_path}")

    # Send email via Gmail SMTP
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(sender_email, app_password)
    server.sendmail(sender_email, to_email, msg.as_string())
    server.quit()
    print(f"Successfully sent email to {to_email} with attached resume: {os.path.basename(resume_path)}")

if __name__ == "__main__":
    print("Email automator module ready.")
