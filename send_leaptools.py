import send_application

subject = "Application: Software Developer (React / Next.js) – Joydeep Das"

body_plain = """Hi Leap Tools Hiring Team,

I came across your opening on RemoteOK for the Software Developer (React / Next.js) position and wanted to reach out. As a frontend engineer with hands-on experience building high-performance web platforms using React, Next.js, TypeScript, and modern component libraries, I would love to be considered for the role.

Why I would be a great addition to Leap Tools:
- Modern React & Next.js Stack: Extensive experience developing scalable web applications using React 19, Next.js (App Router, Server Components), TypeScript, and Tailwind CSS.
- Production Scale & Performance: Built and launched Pandalé Kolkata from scratch—scaling to 7,000+ unique visitors and 31,000+ page views in its first week with optimized asset caching and mobile-first responsive architecture.
- Interactive User Experiences: Shipped platforms like Resume Darzi (real-time streaming LLM UI via NDJSON) and Job Dalal (dynamic filtering, faceted search, interactive state management).
- Design-to-Code Precision: Experienced with Figma design systems, reusable UI token systems, and building pixel-perfect, accessible component kits.

Portfolio & Work:
- Live Portfolio: https://joydeepdas-portfolio.vercel.app
- GitHub: https://github.com/JoyTheSloth
- LinkedIn: https://linkedin.com/in/joydeep-das-78123522a

I have attached my Frontend Resume (Joydeep_Das_Frontend_CV.pdf) for your review. Thank you for your time and consideration—I look forward to discussing how my frontend skills can contribute to Leap Tools' digital products.

Best regards,

Joydeep Das
Frontend Developer
Phone: +91-7085917058
Email: joy.thesloth@gmail.com
"""

body_html = """<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
</head>
<body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; font-size: 15px; line-height: 1.65; color: #1e293b; max-width: 620px; margin: 0 auto; padding: 20px 0;">

  <p style="margin-top: 0; margin-bottom: 16px;">Hi Leap Tools Hiring Team,</p>

  <p style="margin-bottom: 18px;">
    I came across your opening on RemoteOK for the <strong>Software Developer (React / Next.js)</strong> position and wanted to reach out. As a frontend engineer with hands-on experience building performant web applications using React, Next.js, TypeScript, and modern component systems, I would love to be considered for the role.
  </p>

  <p style="font-weight: 600; margin-bottom: 8px; color: #0f172a;">Why I'm a strong match for Leap Tools:</p>
  <ul style="padding-left: 20px; margin-top: 0; margin-bottom: 20px;">
    <li style="margin-bottom: 8px;">
      <strong>Modern React &amp; Next.js Stack:</strong> Hands-on experience developing performant web applications using React, Next.js, TypeScript, and Tailwind CSS with clean state architectures.
    </li>
    <li style="margin-bottom: 8px;">
      <strong>Production Scale &amp; Delivery:</strong> Built and launched <em>Pandalé Kolkata</em> from scratch—handling <strong>7,000+ unique visitors and 31,000+ page views in week 1</strong> with optimized CDN caching and responsive design.
    </li>
    <li style="margin-bottom: 8px;">
      <strong>Interactive UI Platforms:</strong> Shipped products like <em>Resume Darzi</em> (real-time streaming LLM responses via NDJSON) and <em>Job Dalal</em> (dynamic table filtering and data pipelines).
    </li>
    <li style="margin-bottom: 8px;">
      <strong>Figma-to-Code Precision:</strong> Strong bridge between design and code, turning UI designs into modular, reusable, accessible component libraries.
    </li>
  </ul>

  <p style="font-weight: 600; margin-bottom: 8px; color: #0f172a;">Portfolio &amp; Work:</p>
  <p style="margin-top: 0; margin-bottom: 20px; font-size: 14px;">
    🌐 <a href="https://joydeepdas-portfolio.vercel.app" style="color: #2563eb; text-decoration: none; font-weight: 500;">Live Portfolio</a> &nbsp;&bull;&nbsp; 
    💻 <a href="https://github.com/JoyTheSloth" style="color: #2563eb; text-decoration: none; font-weight: 500;">GitHub</a> &nbsp;&bull;&nbsp; 
    💼 <a href="https://linkedin.com/in/joydeep-das-78123522a" style="color: #2563eb; text-decoration: none; font-weight: 500;">LinkedIn</a>
  </p>

  <p style="margin-bottom: 24px;">
    I have attached my <strong>Frontend Resume (PDF)</strong> for your review. Thank you for your consideration—I look forward to discussing how my experience can support Leap Tools.
  </p>

  <div style="margin-top: 24px; padding-top: 16px; border-top: 1px solid #e2e8f0; font-size: 14px; color: #475569;">
    <p style="margin: 0; font-weight: 600; color: #0f172a; font-size: 15px;">Joydeep Das</p>
    <p style="margin: 3px 0; color: #64748b;">Frontend Developer</p>
    <p style="margin: 3px 0;">📞 +91-7085917058 &nbsp;&bull;&nbsp; ✉️ <a href="mailto:joy.thesloth@gmail.com" style="color: #2563eb; text-decoration: none;">joy.thesloth@gmail.com</a></p>
  </div>

</body>
</html>
"""

def preview():
    send_application.send_application_email(
        to_email="ta@leaptools.com",
        subject=subject,
        body_plain=body_plain,
        body_html=body_html,
        role_type="frontend",
        company_name="Leap Tools",
        preview_only=True
    )

def dispatch():
    send_application.send_application_email(
        to_email="ta@leaptools.com",
        subject=subject,
        body_plain=body_plain,
        body_html=body_html,
        role_type="frontend",
        company_name="Leap Tools",
        preview_only=False
    )

if __name__ == "__main__":
    preview()
