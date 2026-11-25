import send_application

subject = "Application: Full-Stack Developer – Joydeep Das"

body_plain = """Hi Fluence Hiring Team,

I came across your opening for the Full-Stack Developer position at Fluence International and wanted to reach out. As a developer with hands-on experience building secure, scalable web platforms using React/Next.js frontends, Python/Node.js backends, and modular component systems, I would love to contribute to Fluence's digital learning and B2B products.

Why I am a strong fit for Fluence:
- Frontend & UI Excellence: Proven experience building responsive, accessible web interfaces in React and Next.js with clean state management, modular component kits, and REST API integrations.
- Full-Stack & API Discipline: Experienced building and securing RESTful APIs, handling asynchronous jobs, and managing PostgreSQL/MongoDB data models with disciplined validation and security practices.
- Real-World Delivery & User Impact: Shipped Pandalé Kolkata (handling 7,000+ unique visitors and 31,000+ page views in week 1 with optimized caching and mobile responsiveness) and multiple client platforms.
- Autonomous Remote Discipline: Fully equipped with a dedicated workstation, Git/GitHub version control workflows, and transparent asynchronous communication.

Portfolio & Work:
- Live Portfolio: https://joydeepdas-portfolio.vercel.app
- GitHub: https://github.com/JoyTheSloth
- LinkedIn: https://linkedin.com/in/joydeep-das-78123522a

I have attached my Frontend/Full-Stack Resume (Joydeep_Das_Frontend_CV.pdf) for your review. Thank you for your time and consideration—I look forward to discussing how my skills can support Fluence's mission.

Best regards,

Joydeep Das
Frontend & Full-Stack Developer
Phone: +91-7085917058
Email: joy.thesloth@gmail.com
"""

body_html = """<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
</head>
<body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; font-size: 15px; line-height: 1.65; color: #1e293b; max-width: 620px; margin: 0 auto; padding: 20px 0;">

  <p style="margin-top: 0; margin-bottom: 16px;">Hi Fluence Hiring Team,</p>

  <p style="margin-bottom: 18px;">
    I came across your opening for the <strong>Full-Stack Developer</strong> position at <strong>Fluence International</strong> and wanted to reach out. As a developer with hands-on experience building reliable, scalable web platforms using React/Next.js frontends, Python/Node.js backends, and modular component architectures, I would love to contribute to your digital products.
  </p>

  <p style="font-weight: 600; margin-bottom: 8px; color: #0f172a;">Why I'm a strong match for Fluence:</p>
  <ul style="padding-left: 20px; margin-top: 0; margin-bottom: 20px;">
    <li style="margin-bottom: 8px;">
      <strong>Frontend &amp; Component Precision:</strong> Deep hands-on experience in React, Next.js, and TypeScript, crafting responsive, accessible user interfaces with clean state management.
    </li>
    <li style="margin-bottom: 8px;">
      <strong>Backend &amp; API Integration:</strong> Experienced in developing RESTful endpoints, async data pipelines, and secure database interactions (PostgreSQL, MongoDB).
    </li>
    <li style="margin-bottom: 8px;">
      <strong>Production Track Record:</strong> Shipped <em>Pandalé Kolkata</em> from scratch—handling <strong>7,000+ unique visitors and 31,000+ page views in week 1</strong> with optimized CDN delivery and mobile-first design.
    </li>
    <li style="margin-bottom: 8px;">
      <strong>Remote Discipline:</strong> Self-driven, collaborative, and equipped with a dedicated high-speed setup and asynchronous communication discipline.
    </li>
  </ul>

  <p style="font-weight: 600; margin-bottom: 8px; color: #0f172a;">Portfolio &amp; Work:</p>
  <p style="margin-top: 0; margin-bottom: 20px; font-size: 14px;">
    🌐 <a href="https://joydeepdas-portfolio.vercel.app" style="color: #2563eb; text-decoration: none; font-weight: 500;">Live Portfolio</a> &nbsp;&bull;&nbsp; 
    💻 <a href="https://github.com/JoyTheSloth" style="color: #2563eb; text-decoration: none; font-weight: 500;">GitHub</a> &nbsp;&bull;&nbsp; 
    💼 <a href="https://linkedin.com/in/joydeep-das-78123522a" style="color: #2563eb; text-decoration: none; font-weight: 500;">LinkedIn</a>
  </p>

  <p style="margin-bottom: 24px;">
    I have attached my <strong>Resume (PDF)</strong> for your review. Thank you for your time and consideration—I would love the opportunity to discuss how my technical skills can support Fluence.
  </p>

  <div style="margin-top: 24px; padding-top: 16px; border-top: 1px solid #e2e8f0; font-size: 14px; color: #475569;">
    <p style="margin: 0; font-weight: 600; color: #0f172a; font-size: 15px;">Joydeep Das</p>
    <p style="margin: 3px 0; color: #64748b;">Frontend &amp; Full-Stack Developer</p>
    <p style="margin: 3px 0;">📞 +91-7085917058 &nbsp;&bull;&nbsp; ✉️ <a href="mailto:joy.thesloth@gmail.com" style="color: #2563eb; text-decoration: none;">joy.thesloth@gmail.com</a></p>
  </div>

</body>
</html>
"""

def preview():
    send_application.send_application_email(
        to_email="techjobs@fluencetraining.com",
        subject=subject,
        body_plain=body_plain,
        body_html=body_html,
        role_type="frontend",
        company_name="Fluence International",
        preview_only=True
    )

def dispatch():
    send_application.send_application_email(
        to_email="techjobs@fluencetraining.com",
        subject=subject,
        body_plain=body_plain,
        body_html=body_html,
        role_type="frontend",
        company_name="Fluence International",
        preview_only=False
    )

if __name__ == "__main__":
    preview()
