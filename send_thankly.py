import send_application

subject = "Application: Founding Product Designer – Joydeep Das"

body_plain = """Hi Harsh,

I saw your posting on Hacker News for the Founding Product Designer role at Thankly and wanted to reach out.

The best thing I've built is Pandalé Kolkata (https://joydeepdas-portfolio.vercel.app)—a high-traffic web platform where I owned the product UX from blank canvas to production, scaling to 7,000+ unique visitors and 31,000+ page views in its first week with an intuitive, mobile-first discovery interface.

Why I would love to shape AI conversational shopping UX at Thankly:
- Bridging Conversational AI & Interface Design: Built products like Resume Darzi and MediRAG-Eval that integrate real-time LLM interaction flows, natural language prompts, and contextual UI states into frictionless user experiences.
- Full Design System Ownership: Proven track record creating end-to-end Figma design systems—foundational typography scales, spacing tokens, and component kits that bridge seamlessly into frontend code.
- Shipped Products with Real Users: Designed the complete mobile UX and interactive prototypes for 2GatherApp (live on Google Play) and client web platforms at mabbele.studios and GEETBIH Labs.
- High Design-to-Code Fluency: Having a strong technical foundation in modern React, Tailwind CSS, and frontend architectures, I design conversational interfaces with a realistic understanding of state transitions, streaming latency, and responsive constraints.

Portfolio & Links:
- Live Portfolio: https://joydeepdas-portfolio.vercel.app
- LinkedIn: https://linkedin.com/in/joydeep-das-78123522a
- GitHub: https://github.com/JoyTheSloth

I have attached my UI/UX CV (Joydeep_Das_UIUX_CV.pdf) for your review. I would love to chat about setting the design standards for how commerce happens inside AI conversations at Thankly.

Best regards,

Joydeep Das
Product & UI/UX Designer
Phone: +91-7085917058
Email: joy.thesloth@gmail.com
"""

body_html = """<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
</head>
<body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; font-size: 15px; line-height: 1.65; color: #1e293b; max-width: 620px; margin: 0 auto; padding: 20px 0;">

  <p style="margin-top: 0; margin-bottom: 16px;">Hi Harsh,</p>

  <p style="margin-bottom: 18px;">
    I came across your posting on Hacker News for the <strong>Founding Product Designer</strong> role at <strong>Thankly</strong> and wanted to reach out.
  </p>

  <p style="margin-bottom: 18px; background-color: #f8fafc; border-left: 3px solid #2563eb; padding: 12px 16px; font-size: 14.5px;">
    <strong>The best thing I've built:</strong> <em>Pandalé Kolkata</em> (<a href="https://joydeepdas-portfolio.vercel.app" style="color: #2563eb; text-decoration: none;">Portfolio Demo</a>)—a high-traffic discovery web platform where I owned the product UX from blank canvas to production, scaling to <strong>7,000+ unique visitors and 31,000+ page views in week 1</strong> with an intuitive mobile-first experience.
  </p>

  <p style="font-weight: 600; margin-bottom: 8px; color: #0f172a;">Why I'd love to shape AI shopping UX at Thankly:</p>
  <ul style="padding-left: 20px; margin-top: 0; margin-bottom: 20px;">
    <li style="margin-bottom: 8px;">
      <strong>Designing for Conversational &amp; Agentic AI:</strong> Designed and shipped products like <em>Resume Darzi</em> and <em>MediRAG-Eval</em>, solving the UX challenges of streaming LLM outputs, contextual chat prompts, and micro-actions.
    </li>
    <li style="margin-bottom: 8px;">
      <strong>End-to-End Design Systems:</strong> Crafted comprehensive Figma component kits, typography hierarchies, and interaction token systems for consumer web and mobile applications.
    </li>
    <li style="margin-bottom: 8px;">
      <strong>Shipped Products on App Stores:</strong> Designed the complete mobile UI/UX and user flows for <em>2GatherApp</em> (published on Google Play).
    </li>
    <li style="margin-bottom: 8px;">
      <strong>Design-to-Code Fluency:</strong> Strong frontend literacy in React, Tailwind, and component lifecycles, enabling rapid prototyping and seamless collaboration with engineers.
    </li>
  </ul>

  <p style="font-weight: 600; margin-bottom: 8px; color: #0f172a;">Portfolio &amp; Work:</p>
  <p style="margin-top: 0; margin-bottom: 20px; font-size: 14px;">
    🎨 <a href="https://joydeepdas-portfolio.vercel.app" style="color: #2563eb; text-decoration: none; font-weight: 500;">Live Portfolio</a> &nbsp;&bull;&nbsp; 
    💼 <a href="https://linkedin.com/in/joydeep-das-78123522a" style="color: #2563eb; text-decoration: none; font-weight: 500;">LinkedIn</a> &nbsp;&bull;&nbsp; 
    💻 <a href="https://github.com/JoyTheSloth" style="color: #2563eb; text-decoration: none; font-weight: 500;">GitHub</a>
  </p>

  <p style="margin-bottom: 24px;">
    I have attached my <strong>UI/UX CV (PDF)</strong> for your review. Thank you for your time—I would love the opportunity to discuss how we can build the future of in-chat shopping experiences.
  </p>

  <div style="margin-top: 24px; padding-top: 16px; border-top: 1px solid #e2e8f0; font-size: 14px; color: #475569;">
    <p style="margin: 0; font-weight: 600; color: #0f172a; font-size: 15px;">Joydeep Das</p>
    <p style="margin: 3px 0; color: #64748b;">Product &amp; UI/UX Designer</p>
    <p style="margin: 3px 0;">📞 +91-7085917058 &nbsp;&bull;&nbsp; ✉️ <a href="mailto:joy.thesloth@gmail.com" style="color: #2563eb; text-decoration: none;">joy.thesloth@gmail.com</a></p>
  </div>

</body>
</html>
"""

def preview():
    send_application.send_application_email(
        to_email="harsh@thankly.ai",
        subject=subject,
        body_plain=body_plain,
        body_html=body_html,
        role_type="uiux",
        company_name="Thankly",
        preview_only=True
    )

def dispatch():
    send_application.send_application_email(
        to_email="harsh@thankly.ai",
        subject=subject,
        body_plain=body_plain,
        body_html=body_html,
        role_type="uiux",
        company_name="Thankly",
        preview_only=False
    )

if __name__ == "__main__":
    preview()
