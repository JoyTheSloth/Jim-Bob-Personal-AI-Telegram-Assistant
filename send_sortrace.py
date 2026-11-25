import send_application

subject = "Application: Junior Frontend Engineer – Joydeep Das"

body_plain = """Hi Sortrace Hiring Team,

I saw your posting on Hacker News for the Junior Frontend Engineer role and wanted to reach out. As an early-career frontend developer who builds with TypeScript, React, Tailwind CSS, and Radix/shadcn UI—and who uses AI coding agents daily in my development workflow—I would love to contribute to Sortrace's customer-facing web platform.

What I've Built & How I Made It:
1. Pandalé Kolkata (https://joydeepdas-portfolio.vercel.app):
   - A high-traffic cultural discovery web platform built with React, Tailwind CSS, and modular UI components.
   - Handled 7,000+ unique visitors and 31,000+ page views in week 1. Optimized asset delivery, mobile-first responsiveness, and smooth client-side filtering.
2. Resume Darzi:
   - An interactive, real-time AI resume optimizer built with Next.js/React and Tailwind CSS.
   - Consumes streaming LLM responses via NDJSON with instant visual diff highlighting and modular component breakdown.
3. Job Dalal:
   - An automated job pipeline frontend featuring dynamic multi-parameter filtering, interactive tables, and clean CSV/export tooling.

Why I'm a Strong Fit for Sortrace:
- Modern Component Architecture: Extensive hands-on experience building clean, accessible, modular UI systems using React, TypeScript, Tailwind CSS, and Radix/shadcn-style primitives.
- Agentic & AI Coding Workflow: I actively leverage AI coding agents (Claude, Cursor, Antigravity) in my day-to-day development for rapid prototyping, comprehensive test coverage, and disciplined refactoring.
- Small Team & High Ownership: Experienced with fast-paced iteration, Git discipline, and shipping real-world user-facing features on short decision paths.

Portfolio & Links:
- Live Portfolio: https://joydeepdas-portfolio.vercel.app
- GitHub: https://github.com/JoyTheSloth
- LinkedIn: https://linkedin.com/in/joydeep-das-78123522a

I have attached my Frontend Resume (Joydeep_Das_Frontend_CV.pdf) for your review. I would welcome the chance to discuss how I can contribute to Sortrace's platform.

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

  <p style="margin-top: 0; margin-bottom: 16px;">Hi Sortrace Hiring Team,</p>

  <p style="margin-bottom: 18px;">
    I came across your posting for the <strong>Junior Frontend Engineer</strong> role at <strong>Sortrace</strong> and wanted to reach out. As an early-career frontend engineer who builds with TypeScript, React, Tailwind CSS, and Radix/shadcn-style component architectures—and who works with AI coding agents daily—I would love to contribute to Sortrace's customer-facing platform.
  </p>

  <p style="font-weight: 600; margin-bottom: 8px; color: #0f172a;">What I've Built &amp; How I Made It:</p>
  <ul style="padding-left: 20px; margin-top: 0; margin-bottom: 20px;">
    <li style="margin-bottom: 10px;">
      <strong>Pandalé Kolkata:</strong> Built and launched a high-traffic responsive web platform using React and Tailwind CSS. Scaled to handle <strong>7,000+ unique visitors and 31,000+ page views</strong> in week 1 with optimized client-side filtering and mobile-first performance.
    </li>
    <li style="margin-bottom: 10px;">
      <strong>Resume Darzi:</strong> An interactive AI resume optimizer built on Next.js/React and Tailwind CSS. Features real-time NDJSON streaming LLM responses and modular preview components.
    </li>
    <li style="margin-bottom: 10px;">
      <strong>Job Dalal:</strong> Dynamic lead filtering and application tracking platform with real-time UI states, search facets, and data exports.
    </li>
  </ul>

  <p style="font-weight: 600; margin-bottom: 8px; color: #0f172a;">Why I'm a Great Match for Sortrace:</p>
  <ul style="padding-left: 20px; margin-top: 0; margin-bottom: 20px;">
    <li style="margin-bottom: 8px;">
      <strong>Component Architecture:</strong> Deep hands-on experience building clean, accessible, modular UI with React, TypeScript, Tailwind CSS, and Radix/shadcn primitives.
    </li>
    <li style="margin-bottom: 8px;">
      <strong>Agentic Workflow:</strong> Heavy daily user of AI coding agents (Claude, Cursor, Antigravity) for rapid iteration, clean architecture, and rapid feature delivery.
    </li>
    <li style="margin-bottom: 8px;">
      <strong>Bias for Action:</strong> Independent, proactive, and comfortable taking ownership within a small engineering team with short decision paths.
    </li>
  </ul>

  <p style="font-weight: 600; margin-bottom: 8px; color: #0f172a;">Portfolio &amp; Work:</p>
  <p style="margin-top: 0; margin-bottom: 20px; font-size: 14px;">
    🌐 <a href="https://joydeepdas-portfolio.vercel.app" style="color: #2563eb; text-decoration: none; font-weight: 500;">Live Portfolio</a> &nbsp;&bull;&nbsp; 
    💻 <a href="https://github.com/JoyTheSloth" style="color: #2563eb; text-decoration: none; font-weight: 500;">GitHub</a> &nbsp;&bull;&nbsp; 
    💼 <a href="https://linkedin.com/in/joydeep-das-78123522a" style="color: #2563eb; text-decoration: none; font-weight: 500;">LinkedIn</a>
  </p>

  <p style="margin-bottom: 24px;">
    I have attached my <strong>Frontend Resume (PDF)</strong> for your review. Thank you for your time and consideration—I look forward to discussing how I can add value to Sortrace.
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
        to_email="jobs@sortrace.com",
        subject=subject,
        body_plain=body_plain,
        body_html=body_html,
        role_type="frontend",
        company_name="Sortrace",
        preview_only=True
    )

def dispatch():
    send_application.send_application_email(
        to_email="jobs@sortrace.com",
        subject=subject,
        body_plain=body_plain,
        body_html=body_html,
        role_type="frontend",
        company_name="Sortrace",
        preview_only=False
    )

if __name__ == "__main__":
    preview()
