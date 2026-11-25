import send_application

subject = "Application: Remote Junior Front-End Developer – Joydeep Das"

body_plain = """Hi Hiring Team at PULSE (MENA),

I am writing to express my strong interest in the Remote Junior Front-End Developer position at PULSE (MENA). As an early-career frontend developer and UI/UX designer with 0-2 years of proven hands-on experience building responsive web platforms, reusable component libraries, and translating design files into production code, I am excited about the opportunity to contribute to your digital initiatives.

Why I am a strong match for this role:
- Core Front-End Proficiency: Deep hands-on experience in HTML5, CSS3/Tailwind CSS, JavaScript (ES6+), and React/Next.js. Experienced in writing clean, modular code, managing state (Context API/Redux), and integrating REST APIs and JSON data.
- UI/UX & Figma-to-Code Translation: Strong background collaborating in Figma to translate wireframes and user flows into responsive, accessible, cross-browser compatible web interfaces.
- Shipped Production Platforms: Built and launched Pandalé Kolkata from scratch (handling 7,000+ visitors and 31K+ page views in week 1 with optimized CDN caching and mobile-first design) and delivered multiple client platforms (ERP, travel, consumer tech).
- Remote-Ready & Self-Driven: Equipped with a dedicated high-speed workstation, Git workflow discipline, and strong asynchronous communication skills.

Portfolio & Profiles:
- Live Portfolio: https://joydeepdas-portfolio.vercel.app
- GitHub: https://github.com/JoyTheSloth
- LinkedIn: https://linkedin.com/in/joydeep-das-78123522a

I have attached my Frontend CV (Joydeep_Das_Frontend_CV.docx) for your review. Thank you for your time and consideration—I look forward to discussing how I can add value to the PULSE team.

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

  <p style="margin-top: 0; margin-bottom: 16px;">Hi Hiring Team at PULSE (MENA),</p>

  <p style="margin-bottom: 18px;">
    I am writing to express my strong interest in the <strong>Remote Junior Front-End Developer</strong> position at <strong>PULSE (MENA)</strong>. As an early-career frontend developer with hands-on experience building responsive web platforms, modular component systems, and translating Figma designs into production code, I would love to contribute to your digital solutions.
  </p>

  <p style="font-weight: 600; margin-bottom: 8px; color: #0f172a;">Why I am a strong match for PULSE (MENA):</p>
  <ul style="padding-left: 20px; margin-top: 0; margin-bottom: 20px;">
    <li style="margin-bottom: 8px;">
      <strong>Core Front-End Proficiency:</strong> Hands-on experience developing clean, mobile-first web pages using HTML5, CSS3, JavaScript (ES6+), and React.js/Next.js with Tailwind CSS and RESTful API integrations.
    </li>
    <li style="margin-bottom: 8px;">
      <strong>Figma-to-Code Translation:</strong> Proven track record converting UI/UX designs into pixel-perfect, accessible, and cross-browser compatible web applications with reusable component architectures.
    </li>
    <li style="margin-bottom: 8px;">
      <strong>Shipped Production Platforms:</strong> Built and launched <em>Pandalé Kolkata</em> from scratch—handling 7,000+ unique visitors and 31,000+ page views in its first week with optimized CDN caching and responsive design.
    </li>
    <li style="margin-bottom: 8px;">
      <strong>Remote-First Discipline:</strong> Independent, proactive, and equipped with a dedicated high-speed workstation, Git/GitHub version control workflows, and effective communication across remote teams.
    </li>
  </ul>

  <p style="font-weight: 600; margin-bottom: 8px; color: #0f172a;">Portfolio &amp; Work:</p>
  <p style="margin-top: 0; margin-bottom: 20px; font-size: 14px;">
    🌐 <a href="https://joydeepdas-portfolio.vercel.app" style="color: #2563eb; text-decoration: none; font-weight: 500;">Live Portfolio</a> &nbsp;&bull;&nbsp; 
    💻 <a href="https://github.com/JoyTheSloth" style="color: #2563eb; text-decoration: none; font-weight: 500;">GitHub</a> &nbsp;&bull;&nbsp; 
    💼 <a href="https://linkedin.com/in/joydeep-das-78123522a" style="color: #2563eb; text-decoration: none; font-weight: 500;">LinkedIn</a>
  </p>

  <p style="margin-bottom: 24px;">
    I have attached my <strong>Frontend CV</strong> for your review. Thank you for your time and consideration—I would love the opportunity to discuss how my technical skills and enthusiasm can support PULSE (MENA)'s mission.
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
        to_email="info@pulsemedianl.com",
        subject=subject,
        body_plain=body_plain,
        body_html=body_html,
        role_type="frontend"
    )

if __name__ == "__main__":
    dispatch()
