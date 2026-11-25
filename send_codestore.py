import send_application

subject = "Application: Trainee Software Engineer – Joydeep Das"

body_plain = """Hi HR Team at CodeStore Technologies,

I am writing to express my strong interest in the Trainee Software Engineer position at CodeStore. As a 2026 B.Tech Computer Science graduate from Amity University with hands-on experience in full-stack web development, Python, JavaScript, React, and SQL, I am excited about the opportunity to kickstart my engineering career with your team.

Key Qualifications & Practical Experience:
- Programming & OOP Fundamentals: Strong foundation in Object-Oriented Programming, data structures, and algorithms, with hands-on development in Python, JavaScript/TypeScript, and React.
- Web & Database Development: Built and deployed production web applications integrated with relational databases (PostgreSQL/SQL), RESTful APIs, and responsive frontends (HTML5, CSS3, Tailwind CSS).
- Shipped Real-World Projects: Shipped 6+ live projects including Pandalé Kolkata (7,000+ visitors, 31K page views in week 1) and MediRAG-Eval (Rank 62 nationally in India Innovates 2026).
- Version Control & Development Practices: Well-versed in Git/GitHub workflows, agile sprint execution, and clean documentation.

Portfolio & Profiles:
- Live Portfolio: https://joydeepdas-portfolio.vercel.app
- GitHub: https://github.com/JoyTheSloth
- LinkedIn: https://linkedin.com/in/joydeep-das-78123522a

I have attached my Forward Deployed Engineer / Full-Stack Resume (Joydeep_Das_FDE_Resume.docx) for your review. Thank you for your time and consideration—I look forward to discussing how I can contribute to CodeStore Technologies.

Best regards,

Joydeep Das
Full-Stack Developer | B.Tech CSE (2026)
Phone: +91-7085917058
Email: joy.thesloth@gmail.com
"""

body_html = """<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
</head>
<body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; font-size: 15px; line-height: 1.65; color: #1e293b; max-width: 620px; margin: 0 auto; padding: 20px 0;">

  <p style="margin-top: 0; margin-bottom: 16px;">Hi HR Team at CodeStore Technologies,</p>

  <p style="margin-bottom: 18px;">
    I am writing to apply for the <strong>Trainee Software Engineer</strong> position at <strong>CodeStore Technologies</strong>. As a 2026 B.Tech Computer Science graduate from Amity University with proven hands-on experience across full-stack web development, Python, JavaScript/React, and relational databases, I would love to contribute to your client and product engineering teams.
  </p>

  <p style="font-weight: 600; margin-bottom: 8px; color: #0f172a;">Why I am a strong candidate for CodeStore:</p>
  <ul style="padding-left: 20px; margin-top: 0; margin-bottom: 20px;">
    <li style="margin-bottom: 8px;">
      <strong>Core Engineering &amp; OOP Foundations:</strong> Solid grasp of Object-Oriented Programming, data structures, algorithms, and clean architecture, backed by hands-on development in Python and JavaScript/TypeScript.
    </li>
    <li style="margin-bottom: 8px;">
      <strong>Full-Stack &amp; Database Proficiency:</strong> Hands-on experience developing RESTful APIs, integrating SQL / PostgreSQL databases, and crafting responsive web interfaces with React and Tailwind CSS.
    </li>
    <li style="margin-bottom: 8px;">
      <strong>Track Record of Shipping:</strong> Built and shipped 6+ live projects including <em>Pandalé Kolkata</em> (7,000+ visitors in 7 days) and <em>MediRAG-Eval</em> (Rank 62 nationally at India Innovates 2026 Hackathon).
    </li>
    <li style="margin-bottom: 8px;">
      <strong>Team &amp; Tooling Discipline:</strong> Proficient with Git/GitHub version control, collaborative code reviews, and fast adaptability to new enterprise tech stacks and frameworks.
    </li>
  </ul>

  <p style="font-weight: 600; margin-bottom: 8px; color: #0f172a;">Portfolio &amp; Profiles:</p>
  <p style="margin-top: 0; margin-bottom: 20px; font-size: 14px;">
    🌐 <a href="https://joydeepdas-portfolio.vercel.app" style="color: #2563eb; text-decoration: none; font-weight: 500;">Live Portfolio</a> &nbsp;&bull;&nbsp; 
    💻 <a href="https://github.com/JoyTheSloth" style="color: #2563eb; text-decoration: none; font-weight: 500;">GitHub</a> &nbsp;&bull;&nbsp; 
    💼 <a href="https://linkedin.com/in/joydeep-das-78123522a" style="color: #2563eb; text-decoration: none; font-weight: 500;">LinkedIn</a>
  </p>

  <p style="margin-bottom: 24px;">
    I have attached my <strong>Full-Stack / Software Engineer Resume</strong> for your review. Thank you for your time and consideration—I look forward to the opportunity to discuss my qualifications further.
  </p>

  <div style="margin-top: 24px; padding-top: 16px; border-top: 1px solid #e2e8f0; font-size: 14px; color: #475569;">
    <p style="margin: 0; font-weight: 600; color: #0f172a; font-size: 15px;">Joydeep Das</p>
    <p style="margin: 3px 0; color: #64748b;">Full-Stack Developer &bull; B.Tech CSE (2026)</p>
    <p style="margin: 3px 0;">📞 +91-7085917058 &nbsp;&bull;&nbsp; ✉️ <a href="mailto:joy.thesloth@gmail.com" style="color: #2563eb; text-decoration: none;">joy.thesloth@gmail.com</a></p>
  </div>

</body>
</html>
"""

def dispatch():
    send_application.send_application_email(
        to_email="hr@codestoresolutions.com",
        subject=subject,
        body_plain=body_plain,
        body_html=body_html,
        role_type="fde"
    )

if __name__ == "__main__":
    dispatch()
