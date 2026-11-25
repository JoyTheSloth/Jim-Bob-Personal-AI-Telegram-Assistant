import send_application

subject = "Application: Junior UI/UX Designer – Joydeep Das"

body_plain = """Hi Appsrow Team,

I saw your opening for a Junior UI/UX Designer at Appsrow and wanted to reach out. As a product and UI/UX designer with 2+ years of hands-on experience designing intuitive digital experiences, design systems, and client web platforms, I'd love to contribute to your team.

Why I would be a great fit for Appsrow:
- Agency & Client-Facing Experience: Designed web and mobile interfaces for multiple client platforms across travel, real estate, and consumer tech at mabbele.studios and GEETBIH Labs.
- End-to-End Product Design in Figma: Proficient in translating user requirements into wireframes, interactive prototypes, and production-ready design systems with tokens and reusable components.
- Bridge Between Design & Web Development: Having a strong grasp of modern web layouts, responsive design, and frontend fundamentals (HTML/CSS/React/TypeScript), I understand how to design layouts that translate seamlessly into pixel-perfect web builds.
- Shipped Products with Real Traction: Designed Pandalé Kolkata (7,000+ visitors, 31K page views in week 1) and 2GatherApp (published on Google Play).

Portfolio & Work:
- Live Portfolio: https://joydeepdas-portfolio.vercel.app
- LinkedIn: https://linkedin.com/in/joydeep-das-78123522a
- GitHub: https://github.com/JoyTheSloth

I have attached my UI/UX CV (Joydeep_Das_UIUX_CV.docx) for your review. I would love the opportunity to chat about how my design skills can help elevate Appsrow's client projects.

Best regards,

Joydeep Das
UI/UX Designer | Product Designer
Phone: +91-7085917058
Email: joy.thesloth@gmail.com
"""

body_html = """<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
</head>
<body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; font-size: 15px; line-height: 1.65; color: #1e293b; max-width: 620px; margin: 0 auto; padding: 20px 0;">

  <p style="margin-top: 0; margin-bottom: 16px;">Hi Appsrow Team,</p>

  <p style="margin-bottom: 18px;">
    I came across your hiring post for a <strong>Junior UI/UX Designer</strong> at <strong>Appsrow</strong> and wanted to reach out. As a product designer with 2+ years of hands-on experience crafting intuitive digital experiences, client web platforms, and scalable design systems, I would love to be considered for the role.
  </p>

  <p style="font-weight: 600; margin-bottom: 8px; color: #0f172a;">Why I'd be a strong fit for Appsrow:</p>
  <ul style="padding-left: 20px; margin-top: 0; margin-bottom: 20px;">
    <li style="margin-bottom: 8px;">
      <strong>Agency &amp; Client Platform Experience:</strong> Designed web and mobile interfaces for diverse client platforms across travel, fintech, real estate, and consumer tech at mabbele.studios and GEETBIH Labs.
    </li>
    <li style="margin-bottom: 8px;">
      <strong>Design Systems &amp; High-Fidelity Prototyping:</strong> Proven track record crafting complete Figma design systems—typography scales, color tokens, and responsive component kits that scale cleanly.
    </li>
    <li style="margin-bottom: 8px;">
      <strong>Design-to-Web Fluency:</strong> Having a deep understanding of modern web responsiveness and front-of-the-frontend fundamentals, I design with web constraints and interactions in mind for seamless, pixel-perfect development.
    </li>
    <li style="margin-bottom: 8px;">
      <strong>Shipped Products with Real Impact:</strong> Designed <em>Pandalé Kolkata</em> (7,000+ visitors and 31K+ page views in week 1) and the complete mobile UI/UX for <em>2GatherApp</em> (live on Google Play).
    </li>
  </ul>

  <p style="font-weight: 600; margin-bottom: 8px; color: #0f172a;">Portfolio &amp; Work:</p>
  <p style="margin-top: 0; margin-bottom: 20px; font-size: 14px;">
    🎨 <a href="https://joydeepdas-portfolio.vercel.app" style="color: #2563eb; text-decoration: none; font-weight: 500;">Live Portfolio</a> &nbsp;&bull;&nbsp; 
    💼 <a href="https://linkedin.com/in/joydeep-das-78123522a" style="color: #2563eb; text-decoration: none; font-weight: 500;">LinkedIn</a> &nbsp;&bull;&nbsp; 
    💻 <a href="https://github.com/JoyTheSloth" style="color: #2563eb; text-decoration: none; font-weight: 500;">GitHub</a>
  </p>

  <p style="margin-bottom: 24px;">
    I have attached my <strong>UI/UX CV</strong> for your review. Thank you for your time and consideration—I would love the opportunity to discuss how I can contribute to Appsrow's upcoming client projects.
  </p>

  <div style="margin-top: 24px; padding-top: 16px; border-top: 1px solid #e2e8f0; font-size: 14px; color: #475569;">
    <p style="margin: 0; font-weight: 600; color: #0f172a; font-size: 15px;">Joydeep Das</p>
    <p style="margin: 3px 0; color: #64748b;">UI/UX Designer &bull; Product Designer</p>
    <p style="margin: 3px 0;">📞 +91-7085917058 &nbsp;&bull;&nbsp; ✉️ <a href="mailto:joy.thesloth@gmail.com" style="color: #2563eb; text-decoration: none;">joy.thesloth@gmail.com</a></p>
  </div>

</body>
</html>
"""

def send_self():
    send_application.send_application_email(
        to_email="joy.thesloth@gmail.com",
        subject=subject,
        body_plain=body_plain,
        body_html=body_html,
        role_type="uiux"
    )

def send_real():
    send_application.send_application_email(
        to_email="hr@appsrow.com",
        subject=subject,
        body_plain=body_plain,
        body_html=body_html,
        role_type="uiux"
    )

if __name__ == "__main__":
    send_self()
