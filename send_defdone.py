import send_application

subject = "Application: Junior Frontend Developer (React / TypeScript) – Joydeep Das"

body_plain = """Hi defdone Team,

I am writing to express my interest in joining defdone as a Junior / Middle Frontend Developer. As a developer specializing in modern React, TypeScript, Next.js, and design-to-code execution, I would love the opportunity to contribute to your software delivery teams and client projects.

Why I would be a great fit for defdone:
- Modern React & TypeScript: Deep hands-on experience building performant, modular web interfaces using React 19, Next.js, TypeScript, and Tailwind CSS.
- Production Track Record: Designed and launched Pandalé Kolkata (handling 7,000+ unique visitors and 31K+ page views in week 1 with optimized CDN caching) and developed complex frontends like Resume Darzi (streaming LLM responses via NDJSON).
- Design Systems & Component Libraries: Strong bridge between design and code—experienced in building reusable Figma design systems and translating them cleanly into scalable React component kits.
- Agile & Collaborative: Comfortable collaborating in English-speaking remote environments, managing features via Git/GitHub, and writing clean, maintainable code.

Portfolio & Work:
- Live Portfolio: https://joydeepdas-portfolio.vercel.app
- GitHub: https://github.com/JoyTheSloth
- LinkedIn: https://linkedin.com/in/joydeep-das-78123522a

I have attached my Frontend CV (Joydeep_Das_Frontend_CV.docx) for your review. Thank you for your time and consideration—I look forward to the possibility of discussing how I can add value to defdone.

Best regards,

Joydeep Das
Frontend Developer | UI/UX Designer
Phone: +91-7085917058
Email: joy.thesloth@gmail.com
"""

body_html = """<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
</head>
<body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; font-size: 15px; line-height: 1.65; color: #1e293b; max-width: 620px; margin: 0 auto; padding: 20px 0;">

  <p style="margin-top: 0; margin-bottom: 16px;">Hi defdone Team,</p>

  <p style="margin-bottom: 18px;">
    I am writing to express my interest in joining <strong>defdone</strong> as a <strong>Frontend Developer (React / TypeScript)</strong>. As a developer specializing in modern React 19, TypeScript, Next.js, and design-to-code execution, I would love to contribute to your software engineering teams and client platforms.
  </p>

  <p style="font-weight: 600; margin-bottom: 8px; color: #0f172a;">Why I'd be a great addition to defdone:</p>
  <ul style="padding-left: 20px; margin-top: 0; margin-bottom: 20px;">
    <li style="margin-bottom: 8px;">
      <strong>Modern React &amp; TypeScript:</strong> Deep hands-on experience building responsive web interfaces using React 19, Next.js, TypeScript, and Tailwind CSS with clean state management.
    </li>
    <li style="margin-bottom: 8px;">
      <strong>Proven Production Delivery:</strong> Built and launched <em>Pandalé Kolkata</em> (7,000+ visitors, 31K+ page views in week 1 with CDN optimization) and delivered complex platforms like <em>Resume Darzi</em> (real-time NDJSON streaming).
    </li>
    <li style="margin-bottom: 8px;">
      <strong>Design Systems &amp; Clean Components:</strong> Bridges design and engineering seamlessly—converting Figma wireframes into modular, scalable component libraries with accessible interactions.
    </li>
    <li style="margin-bottom: 8px;">
      <strong>Remote Team Workflow:</strong> Experienced in asynchronous collaboration, disciplined Git/GitHub branching and review workflows, and agile sprint delivery.
    </li>
  </ul>

  <p style="font-weight: 600; margin-bottom: 8px; color: #0f172a;">Portfolio &amp; Work:</p>
  <p style="margin-top: 0; margin-bottom: 20px; font-size: 14px;">
    🌐 <a href="https://joydeepdas-portfolio.vercel.app" style="color: #2563eb; text-decoration: none; font-weight: 500;">Live Portfolio</a> &nbsp;&bull;&nbsp; 
    💻 <a href="https://github.com/JoyTheSloth" style="color: #2563eb; text-decoration: none; font-weight: 500;">GitHub</a> &nbsp;&bull;&nbsp; 
    💼 <a href="https://linkedin.com/in/joydeep-das-78123522a" style="color: #2563eb; text-decoration: none; font-weight: 500;">LinkedIn</a>
  </p>

  <p style="margin-bottom: 24px;">
    I have attached my <strong>Frontend CV</strong> for your review. Thank you for your time and consideration—I would welcome the opportunity to discuss how my skill set can support defdone's upcoming projects.
  </p>

  <div style="margin-top: 24px; padding-top: 16px; border-top: 1px solid #e2e8f0; font-size: 14px; color: #475569;">
    <p style="margin: 0; font-weight: 600; color: #0f172a; font-size: 15px;">Joydeep Das</p>
    <p style="margin: 3px 0; color: #64748b;">Frontend Developer &bull; UI/UX Designer</p>
    <p style="margin: 3px 0;">📞 +91-7085917058 &nbsp;&bull;&nbsp; ✉️ <a href="mailto:joy.thesloth@gmail.com" style="color: #2563eb; text-decoration: none;">joy.thesloth@gmail.com</a></p>
  </div>

</body>
</html>
"""

def dispatch():
    send_application.send_application_email(
        to_email="hello@defdone.com",
        subject=subject,
        body_plain=body_plain,
        body_html=body_html,
        role_type="frontend"
    )

if __name__ == "__main__":
    dispatch()
