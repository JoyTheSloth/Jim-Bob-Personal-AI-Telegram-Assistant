import send_application

subject = "Application: Frontend / React Developer – Joydeep Das"

body_plain = """Hi Hiring Team,

I came across your opening for a React Developer and wanted to reach out. As a frontend engineer who bridges Figma design systems and production React / Next.js engineering, I would love to be considered for the role.

What I bring:
- Modern React & TypeScript: Hands-on experience developing responsive web applications using React 19, Next.js, TypeScript, and Tailwind CSS.
- Production Scale & Performance: Built and launched Pandalé Kolkata from scratch—handling 7,000+ unique visitors and 31,000+ page views in its first week with optimized CDN caching and mobile-first design.
- Interactive Features & AI Integration: Shipped platforms like Resume Darzi (real-time streaming LLM responses via NDJSON) and Job Dalal (dynamic filtering, job scraping pipelines, CSV/Sheets exports).
- Design-to-Code Workflow: Led frontend design & development at GEETBIH Labs and freelance client platforms, translating Figma wireframes into reusable component libraries.

Portfolio & Work:
- Portfolio: https://joydeepdas-portfolio.vercel.app
- GitHub: https://github.com/JoyTheSloth
- LinkedIn: https://linkedin.com/in/joydeep-das-78123522a

I have attached my Frontend CV (Joydeep_Das_Frontend_CV.docx). Thank you for your time and consideration—I look forward to hearing from you.

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

  <p style="margin-top: 0; margin-bottom: 16px;">Hi Hiring Team,</p>

  <p style="margin-bottom: 18px;">
    I came across your opening for a <strong>React Developer</strong> and wanted to reach out. As a frontend engineer who bridges Figma design systems and production React / Next.js engineering, I would love to be considered for the role.
  </p>

  <p style="font-weight: 600; margin-bottom: 8px; color: #0f172a;">What I bring to the team:</p>
  <ul style="padding-left: 20px; margin-top: 0; margin-bottom: 20px;">
    <li style="margin-bottom: 8px;">
      <strong>Modern React &amp; TypeScript:</strong> Hands-on experience building performant, responsive web apps using React 19, Next.js, TypeScript, and Tailwind CSS.
    </li>
    <li style="margin-bottom: 8px;">
      <strong>Production Scale &amp; Performance:</strong> Built and launched <em>Pandalé Kolkata</em> from scratch—handling 7,000+ unique visitors and 31,000+ page views in its first week with optimized CDN caching and mobile-first design.
    </li>
    <li style="margin-bottom: 8px;">
      <strong>Interactive Frontends &amp; AI Integration:</strong> Shipped products like <em>Resume Darzi</em> (real-time streaming LLM responses via NDJSON) and <em>Job Dalal</em> (interactive filtering, dynamic tables, CSV/Sheets exports).
    </li>
    <li style="margin-bottom: 8px;">
      <strong>Design-to-Code Workflow:</strong> Led UI/UX and frontend engineering at GEETBIH Labs and client platforms, turning Figma wireframes into modular, scalable component libraries.
    </li>
  </ul>

  <p style="font-weight: 600; margin-bottom: 8px; color: #0f172a;">Portfolio &amp; Work:</p>
  <p style="margin-top: 0; margin-bottom: 20px; font-size: 14px;">
    🌐 <a href="https://joydeepdas-portfolio.vercel.app" style="color: #2563eb; text-decoration: none; font-weight: 500;">Live Portfolio</a> &nbsp;&bull;&nbsp; 
    💻 <a href="https://github.com/JoyTheSloth" style="color: #2563eb; text-decoration: none; font-weight: 500;">GitHub</a> &nbsp;&bull;&nbsp; 
    💼 <a href="https://linkedin.com/in/joydeep-das-78123522a" style="color: #2563eb; text-decoration: none; font-weight: 500;">LinkedIn</a>
  </p>

  <p style="margin-bottom: 24px;">
    I have attached my <strong>Frontend CV</strong> for your review. Thank you for your time and consideration—I would welcome the opportunity to discuss how I can contribute to your team.
  </p>

  <div style="margin-top: 24px; padding-top: 16px; border-top: 1px solid #e2e8f0; font-size: 14px; color: #475569;">
    <p style="margin: 0; font-weight: 600; color: #0f172a; font-size: 15px;">Joydeep Das</p>
    <p style="margin: 3px 0; color: #64748b;">Frontend Developer &bull; UI/UX Designer</p>
    <p style="margin: 3px 0;">📞 +91-7085917058 &nbsp;&bull;&nbsp; ✉️ <a href="mailto:joy.thesloth@gmail.com" style="color: #2563eb; text-decoration: none;">joy.thesloth@gmail.com</a></p>
  </div>

</body>
</html>
"""

if __name__ == "__main__":
    send_application.send_application_email(
        to_email="joy.thesloth@gmail.com",
        subject=subject,
        body_plain=body_plain,
        body_html=body_html,
        role_type="frontend"
    )
