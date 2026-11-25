import send_application

subject = "Application: UI/UX Designer & Product Designer – Joydeep Das"

body_plain = """Hi Hiring Team,

I came across your opening for a UI/UX Designer and wanted to reach out. As a Product & UI/UX Designer with a strong design-to-code background (Figma, design systems, and frontend implementation), I would love to be considered for the role.

What I bring to the team:
- End-to-End Product Design: 2+ years designing responsive web and mobile products, scalable design systems, and interactive prototypes across travel, fintech, real estate, and consumer apps.
- Proven User Impact: Designed Pandalé Kolkata from scratch—driving 7,000+ unique visitors and 31,000+ page views in its first week with an intuitive mobile-first interface.
- Shipped Products on App Stores: Designed the high-fidelity mobile UX and design system for 2GatherApp (live on Google Play), improving user onboarding and event discovery.
- Design Systems & Developer Handoff: Led UI/UX at GEETBIH Labs, authoring full component libraries, design tokens, and collaborating seamlessly with engineers using React and Tailwind CSS.

Portfolio & Work:
- Live Portfolio: https://joydeepdas-portfolio.vercel.app
- LinkedIn: https://linkedin.com/in/joydeep-das-78123522a
- GitHub: https://github.com/JoyTheSloth

I have attached my UI/UX CV (Joydeep_Das_UIUX_CV.docx) for your review. Thank you for your time and consideration—I look forward to hearing from you.

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

  <p style="margin-top: 0; margin-bottom: 16px;">Hi Hiring Team,</p>

  <p style="margin-bottom: 18px;">
    I came across your opening for a <strong>UI/UX Designer / Product Designer</strong> and wanted to reach out. As a product designer with a strong design-to-code foundation (Figma, scalable design systems, and interactive prototyping), I would love to be considered for the role.
  </p>

  <p style="font-weight: 600; margin-bottom: 8px; color: #0f172a;">What I bring to the team:</p>
  <ul style="padding-left: 20px; margin-top: 0; margin-bottom: 20px;">
    <li style="margin-bottom: 8px;">
      <strong>End-to-End Product Design:</strong> 2+ years designing responsive web and mobile products, user flows, and interactive prototypes across travel, fintech, real estate, and consumer tech.
    </li>
    <li style="margin-bottom: 8px;">
      <strong>Proven User Impact:</strong> Designed and launched <em>Pandalé Kolkata</em>—driving 7,000+ unique visitors and 31,000+ page views in its first week with an intuitive, mobile-first UX.
    </li>
    <li style="margin-bottom: 8px;">
      <strong>Shipped Mobile &amp; Web Products:</strong> Designed the complete visual identity, UX flows, and design system for <em>2GatherApp</em> (live on Google Play) and financial dashboards for <em>ValueAxis Wealth</em>.
    </li>
    <li style="margin-bottom: 8px;">
      <strong>Design Systems &amp; Developer Handoff:</strong> Led UI/UX at GEETBIH Labs, establishing token-based design systems, reusable Figma component kits, and ensuring seamless handoff to frontend engineers.
    </li>
  </ul>

  <p style="font-weight: 600; margin-bottom: 8px; color: #0f172a;">Portfolio &amp; Work:</p>
  <p style="margin-top: 0; margin-bottom: 20px; font-size: 14px;">
    🎨 <a href="https://joydeepdas-portfolio.vercel.app" style="color: #2563eb; text-decoration: none; font-weight: 500;">Live Portfolio</a> &nbsp;&bull;&nbsp; 
    💼 <a href="https://linkedin.com/in/joydeep-das-78123522a" style="color: #2563eb; text-decoration: none; font-weight: 500;">LinkedIn</a> &nbsp;&bull;&nbsp; 
    💻 <a href="https://github.com/JoyTheSloth" style="color: #2563eb; text-decoration: none; font-weight: 500;">GitHub</a>
  </p>

  <p style="margin-bottom: 24px;">
    I have attached my <strong>UI/UX CV</strong> for your review. Thank you for your time and consideration—I would welcome the opportunity to discuss how my design background aligns with your team's goals.
  </p>

  <div style="margin-top: 24px; padding-top: 16px; border-top: 1px solid #e2e8f0; font-size: 14px; color: #475569;">
    <p style="margin: 0; font-weight: 600; color: #0f172a; font-size: 15px;">Joydeep Das</p>
    <p style="margin: 3px 0; color: #64748b;">UI/UX Designer &bull; Product Designer</p>
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
        role_type="uiux"
    )
