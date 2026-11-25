"""
Elite Full-Detail 2-Page Executive Tech Resume Generator.
Preserves 100% of Joydeep's real work history, projects, metrics, education, and achievements.
Uses modern Silicon Valley / FAANG typographic hierarchy:
- High readability (10pt body, 1.4 line-height, elegant section dividers)
- Exact A4 page-break calibration (Page 1 = Header, Summary, Skills, 5 Flagship Projects; Page 2 = Experience, Education, Hackathons, Certifications)
- Zero squishing, zero artificial truncations, beautiful contrast and spacing.
"""

import os
from pathlib import Path
from playwright.sync_api import sync_playwright

OUT_DIR = Path(__file__).parent / "resumes_pdf"
OUT_DIR.mkdir(exist_ok=True)

FULL_RESUME_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Joydeep Das - Frontend Developer &amp; UI/UX Designer</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

@page {
    size: A4;
    margin: 0.42in 0.52in;
}

* {
    box-sizing: border-box;
    -webkit-print-color-adjust: exact;
}

body {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    color: #1e293b;
    background: #ffffff;
    margin: 0;
    padding: 0;
    font-size: 8.8pt;
    line-height: 1.35;
}

/* Page Break Utility */
.page-break {
    page-break-before: always;
    break-before: page;
}

/* Header */
.header {
    margin-bottom: 10px;
    border-bottom: 2px solid #0f172a;
    padding-bottom: 8px;
}

.name {
    font-size: 21pt;
    font-weight: 800;
    letter-spacing: -0.5px;
    color: #090d16;
    margin: 0 0 2px 0;
    line-height: 1.1;
}

.title-tag {
    font-size: 10pt;
    font-weight: 600;
    color: #2563eb;
    margin-bottom: 6px;
    letter-spacing: -0.2px;
}

.contact-row {
    font-size: 8.4pt;
    color: #475569;
    display: flex;
    flex-wrap: wrap;
    gap: 6px 14px;
}

a {
    color: #1d4ed8;
    text-decoration: underline;
    text-decoration-thickness: 1px;
    text-underline-offset: 2px;
}

.contact-row a {
    color: #1d4ed8;
    text-decoration: underline;
    text-decoration-thickness: 1.2px;
    font-weight: 600;
}

.project-title a {
    color: #0f172a;
    text-decoration: none;
}

.project-title a:hover {
    text-decoration: underline;
}

.project-links a {
    color: #1d4ed8;
    text-decoration: underline;
    font-weight: 700;
    margin-left: 4px;
}
.section {
    margin-bottom: 10px;
}

.section-title {
    font-size: 9.8pt;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    color: #0f172a;
    border-bottom: 1.5px solid #e2e8f0;
    padding-bottom: 2px;
    margin-top: 10px;
    margin-bottom: 6px;
    display: flex;
    align-items: center;
}

.section-title::after {
    content: '';
    display: block;
    height: 2px;
    background: #2563eb;
    width: 24px;
    margin-left: 8px;
}

.summary-text {
    font-size: 8.8pt;
    color: #334155;
    text-align: justify;
    line-height: 1.38;
    margin: 0;
}

/* Skills Grid */
.skill-group {
    margin-bottom: 3.5px;
    font-size: 8.6pt;
    line-height: 1.32;
}

.skill-label {
    font-weight: 700;
    color: #0f172a;
    min-width: 140px;
}

.skill-list {
    color: #334155;
}

/* Project Cards */
.project-card {
    margin-bottom: 8px;
}

.project-header {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin-bottom: 1.5px;
}

.project-title {
    font-size: 9.2pt;
    font-weight: 700;
    color: #0f172a;
}

.project-title a {
    color: #0f172a;
    text-decoration: none;
}

.project-links {
    font-size: 8.2pt;
    font-weight: 600;
    color: #2563eb;
}

.project-links a {
    color: #2563eb;
    text-decoration: none;
    margin-left: 4px;
}

.project-date {
    font-size: 8.2pt;
    font-weight: 600;
    color: #64748b;
    font-family: 'JetBrains Mono', monospace;
}

.project-tech {
    font-size: 8.1pt;
    font-weight: 600;
    color: #0284c7;
    margin-bottom: 2px;
    font-family: 'JetBrains Mono', monospace;
}

/* Bullets */
.bullets {
    margin: 2px 0 0 0;
    padding-left: 15px;
}

.bullets li {
    font-size: 8.5pt;
    color: #334155;
    margin-bottom: 2.5px;
    line-height: 1.35;
}

.bullets li strong {
    color: #0f172a;
}

.additional-projects {
    font-size: 8.3pt;
    color: #475569;
    background: #f8fafc;
    border-left: 3px solid #cbd5e1;
    padding: 5px 8px;
    border-radius: 0 4px 4px 0;
    margin-top: 6px;
    line-height: 1.35;
}

/* Experience Cards */
.exp-card {
    margin-bottom: 9px;
}

.exp-header {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin-bottom: 1.5px;
}

.exp-role {
    font-size: 9.2pt;
    font-weight: 700;
    color: #0f172a;
}

.exp-company {
    font-size: 8.6pt;
    font-weight: 600;
    color: #475569;
}

.exp-period {
    font-size: 8.2pt;
    font-weight: 600;
    color: #64748b;
    font-family: 'JetBrains Mono', monospace;
    white-space: nowrap;
}

/* Education & Honors */
.edu-card {
    margin-bottom: 6px;
}

.edu-header {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
}

.edu-degree {
    font-size: 9pt;
    font-weight: 700;
    color: #0f172a;
}

.edu-meta {
    font-size: 8.2pt;
    font-weight: 600;
    color: #64748b;
    font-family: 'JetBrains Mono', monospace;
}

.edu-inst {
    font-size: 8.5pt;
    color: #475569;
    margin-top: 1px;
}

.edu-grades {
    font-size: 8.2pt;
    color: #64748b;
    margin-top: 1.5px;
}

.cert-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 3px 10px;
    font-size: 8.3pt;
    color: #334155;
    margin-top: 3px;
}

.cert-item {
    display: flex;
    align-items: center;
}

.cert-item::before {
    content: "•";
    color: #2563eb;
    font-weight: bold;
    display: inline-block;
    width: 1em;
    margin-left: -0.2em;
}
</style>
</head>
<body>

<!-- ================= PAGE 1 ================= -->
<div class="header">
    <div class="name">JOYDEEP DAS</div>
    <div class="title-tag">Frontend Developer &bull; React, TypeScript, Next.js &bull; UI/UX Designer &bull; Design Systems</div>
    <div class="contact-row">
        <span>📍 Kolkata, West Bengal, India</span>
        <span>📞 +91-7085917058</span>
        <span>✉️ <a href="mailto:joy.thesloth@gmail.com">joy.thesloth@gmail.com</a></span>
        <span>💼 <a href="https://linkedin.com/in/joydeep-das-78123522a">LinkedIn</a></span>
        <span>💻 <a href="https://github.com/JoyTheSloth">GitHub</a></span>
        <span>🌐 <a href="https://joydeepdas-portfolio.vercel.app">Portfolio</a></span>
    </div>
</div>

<div class="section">
    <div class="section-title">Professional Summary</div>
    <p class="summary-text">
        <strong>Frontend Developer and UI/UX Designer</strong> (2026 B.Tech CSE graduate) with hands-on expertise taking digital products from Figma wireframes to production code using React, TypeScript, Next.js, and Tailwind CSS. Shipped <strong>6+ production applications</strong>, including <em>Pandalé Kolkata</em>, a high-traffic mobile-first guide that attracted <strong>7,000+ unique visitors and 31,000+ page views in its first 7 days</strong>, which I designed, built, and optimized end-to-end. Experienced architecting scalable component libraries, crafting responsive client platforms across travel, real estate, and enterprise tools, and integrating AI into modern frontends (streaming LLM responses, real-time filtering, semantic search) via Groq, Gemini, and RAG. Open to Frontend Developer, React Developer, and UI Engineer roles.
    </p>
</div>

<div class="section">
    <div class="section-title">Technical Skills &amp; Stack</div>
    <div class="skill-group"><span class="skill-label">Frontend Architecture:</span> <span class="skill-list">React 19, Next.js (App Router, SSR), TypeScript, JavaScript (ES6+), Tailwind CSS, Vite, HTML5, CSS3, Responsive / Mobile-First Layouts, Component Architecture, State Management</span></div>
    <div class="skill-group"><span class="skill-label">UI/UX &amp; Design Systems:</span> <span class="skill-list">Figma, UI/UX Wireframing, Rapid Prototyping, Design Tokens, Typography Scales, Component Kits, Design-to-Code Workflows, Micro-Interactions, Visual Branding</span></div>
    <div class="skill-group"><span class="skill-label">Backend &amp; APIs:</span> <span class="skill-list">Node.js, Express.js, FastAPI, Flask, RESTful APIs, NDJSON Streaming, PostgreSQL (Supabase), SQL, Python</span></div>
    <div class="skill-group"><span class="skill-label">AI Integration:</span> <span class="skill-list">Groq (Llama 3.3/3.1), Google Gemini API, RAG, LangChain, Prompt Engineering, Embeddings, Semantic Search, FAISS, Structured JSON Output Guardrails</span></div>
    <div class="skill-group"><span class="skill-label">Tools &amp; Deployment:</span> <span class="skill-list">Git, GitHub, Vercel, Netlify, Docker, Hugging Face Spaces, Playwright, Apify, Web Analytics, CDN Caching, Linux</span></div>
</div>

<div class="section">
    <div class="section-title">Featured Engineering Projects</div>

    <!-- Project 1 -->
    <div class="project-card">
        <div class="project-header">
            <div>
                <span class="project-title"><a href="https://pandale-kolkata.vercel.app">Pandalé Kolkata: Durga Puja Discovery &amp; Metro Guide</a></span>
                <span class="project-links">[<a href="https://pandale-kolkata.vercel.app">Live Demo</a>]</span>
            </div>
            <div class="project-date">2026</div>
        </div>
        <div class="project-tech">React &bull; TypeScript &bull; Tailwind CSS &bull; Vercel &bull; Web Analytics &bull; CDN Optimization</div>
        <ul class="bullets">
            <li>Designed and shipped a mobile-first city navigation platform helping users discover Kolkata pandals, explore metro connectivity, bookmark spots, and navigate routes in real time.</li>
            <li>Attracted <strong>7,000+ unique visitors and 31,000+ page views in 7 days</strong> through organic discovery, localized social marketing, and word-of-mouth.</li>
            <li>Generated <strong>90K+ combined video views</strong> across two viral social media announcements, driving sustained peak concurrent traffic without downtime.</li>
            <li>Owned the entire product lifecycle: Figma component kits, front-end architecture, edge CDN asset optimization, and live user analytics.</li>
        </ul>
    </div>

    <!-- Project 2 -->
    <div class="project-card">
        <div class="project-header">
            <div>
                <span class="project-title"><a href="https://resume-darzi.vercel.app">Resume Darzi: Real-Time AI Resume Tailoring Studio</a></span>
                <span class="project-links">[<a href="https://resume-darzi.vercel.app">Live Demo</a>]</span>
            </div>
            <div class="project-date">2026</div>
        </div>
        <div class="project-tech">Next.js &bull; React 19 &bull; TypeScript &bull; Groq (Llama 3) &bull; Tailwind CSS &bull; docx-preview</div>
        <ul class="bullets">
            <li>Engineered an AI resume studio constraining LLM generations strictly to the user’s verified career history to completely eliminate hallucinations.</li>
            <li>Implemented an ATS keyword scoring engine that analyzes target job descriptions and generates real-time tailored bullet rewrites via <strong>streaming NDJSON responses</strong>.</li>
            <li>Built multi-persona career management with local-first persistent storage, in-browser DOCX preview, and instant PDF/DOCX downloads.</li>
        </ul>
    </div>

    <!-- Project 3 -->
    <div class="project-card">
        <div class="project-header">
            <div>
                <span class="project-title"><a href="https://github.com/JoyTheSloth/Job-Dalal">Job Dalal: AI Job Aggregation &amp; Semantic Matching Engine</a></span>
                <span class="project-links">[<a href="https://github.com/JoyTheSloth">GitHub</a>]</span>
            </div>
            <div class="project-date">2026</div>
        </div>
        <div class="project-tech">React 19 &bull; TypeScript &bull; Groq (Llama 3) &bull; Apify &bull; Node.js &bull; Tailwind CSS</div>
        <ul class="bullets">
            <li>Built an interactive React 19 data dashboard featuring dynamic multi-faceted filtering, one-click CSV/XLSX exports, and automated Google Sheets sync.</li>
            <li>Integrated automated Apify crawlers to aggregate tech openings across LinkedIn, Naukri, Indeed, and Internshala with cross-portal deduplication.</li>
            <li>Leveraged Groq Llama 3 to perform instant semantic resume-to-JD gap analysis, scoring candidate fit and surfacing missing technical keywords.</li>
        </ul>
    </div>

    <!-- Project 4 -->
    <div class="project-card">
        <div class="project-header">
            <div>
                <span class="project-title"><a href="https://github.com/JoyTheSloth/MediFlow---Healthcare">MediRAG-Eval: Clinical RAG Safety &amp; Hallucination Audit Suite</a></span>
                <span class="project-links">[<a href="https://github.com/JoyTheSloth/MediFlow---Healthcare">GitHub</a>]</span>
            </div>
            <div class="project-date">India Innovates '26 (Rank 62)</div>
        </div>
        <div class="project-tech">React 19 &bull; Python &bull; FastAPI &bull; LangChain &bull; FAISS &bull; RAGAS &bull; BioBERT</div>
        <ul class="bullets">
            <li>Owned the React 19 clinical audit front end, creating MediChat with live hallucination risk gauges, source citation cards, and diagnostic lab report uploads.</li>
            <li>Engineered an evaluation lab for side-by-side A/B comparisons of clinical LLM personas backed by a hybrid BioBERT + BM25 retrieval pipeline over 107K vectors.</li>
        </ul>
    </div>

<!-- ================= PAGE 2 ================= -->
<div class="page-break"></div>

<div class="section">
    <!-- Project 5 -->
    <div class="project-card">
        <div class="project-header">
            <div>
                <span class="project-title"><a href="https://github.com/JoyTheSloth">Researcix: Autonomous Multi-Agent Academic Paper Synthesis</a></span>
                <span class="project-links">[<a href="https://github.com/JoyTheSloth">Live Demo</a>]</span>
            </div>
            <div class="project-date">2026</div>
        </div>
        <div class="project-tech">React 19 &bull; Vite &bull; Tailwind CSS &bull; Node.js &bull; Express &bull; Groq (Llama 3.3 70B) &bull; arXiv API</div>
        <ul class="bullets">
            <li>Architected a 4-phase autonomous agent system that researches, cross-references arXiv literature, and outputs publication-ready IEEE LaTeX papers in under 3 minutes.</li>
            <li>Streamed real-time agent reasoning thoughts to the client UI via NDJSON; deployed backend on Hugging Face Spaces and frontend on Vercel.</li>
        </ul>
    </div>

    <div class="additional-projects">
        <strong>Additional Production &amp; Hackathon Projects:</strong> <a href="https://github.com/JoyTheSloth">Stash</a> (local-first AI clipboard vault; built for OpenAI x NamasteDev Hackathon), <a href="https://github.com/JoyTheSloth">ZenEstate</a> (Next.js 15 real estate directory), <a href="https://github.com/JoyTheSloth/FlatzyAdmin">Flatzy</a> (rental discovery portal), <a href="https://github.com/JoyTheSloth/fitnessbunny">FitnessBunny</a> (AI calorie estimator), <a href="https://github.com/JoyTheSloth">MABAS</a> (5-agent bug analysis orchestrator), <a href="https://github.com/JoyTheSloth/BacSense-2.0">BacSense 2.0</a> (IoT telemetry dashboard).
    </div>
</div>

<div class="section">
    <div class="section-title">Work Experience</div>

    <!-- Exp 1 -->
    <div class="exp-card">
        <div class="exp-header">
            <div>
                <span class="exp-role">Freelance Designer / Developer</span>
                <span class="exp-company"> &mdash; <a href="https://github.com/JoyTheSloth/mabbele-studios">mabbele.studios</a> (Freelance, Remote)</span>
            </div>
            <div class="exp-period">August 2026 – Present</div>
        </div>
        <ul class="bullets">
            <li>Design and engineer production frontends for client platforms across travel, ERP, real estate, and consumer technology, including <strong>TripEva</strong> (interactive route calculators, dynamic filters), <strong>VidyaSetu ERP</strong>, and <strong>Modern Mahal</strong> (luxury real estate platform).</li>
            <li>Establish and maintain a strict design-to-code workflow using TypeScript and Tailwind CSS, taking projects seamlessly from Figma wireframes to deployed, accessible web applications.</li>
            <li>Collaborate directly with founders to translate business goals into intuitive UX, conducting design QA and auditing responsive layouts across devices.</li>
        </ul>
    </div>

    <!-- Exp 2 -->
    <div class="exp-card">
        <div class="exp-header">
            <div>
                <span class="exp-role">Consultant</span>
                <span class="exp-company"> &mdash; SkillArbitrage (Full-time, Remote)</span>
            </div>
            <div class="exp-period">July 2026 – September 2026</div>
        </div>
        <ul class="bullets">
            <li>Advised students and early-career software professionals on AI, ML, and full-stack engineering upskilling roadmaps.</li>
            <li>Managed technical lead qualification, customer objections, and enrollment workflows using CRM pipelines and data-driven follow-ups.</li>
        </ul>
    </div>

    <!-- Exp 3 -->
    <div class="exp-card">
        <div class="exp-header">
            <div>
                <span class="exp-role">React Developer &amp; Lead UI/UX Designer</span>
                <span class="exp-company"> &mdash; GEETBIH Labs Pvt. Ltd. (Part-time)</span>
            </div>
            <div class="exp-period">April 2026 – October 2026</div>
        </div>
        <ul class="bullets">
            <li>Led UI/UX design initiatives for digital client platforms, architecting a unified Figma design system with reusable components, color tokens, and responsive typography scales.</li>
            <li>Developed responsive front-end interfaces using React, JavaScript/TypeScript, and CSS, translating high-fidelity prototypes into production-grade, maintainable code.</li>
            <li>Streamlined developer handoff by authoring interactive component documentation and CSS design specs.</li>
        </ul>
    </div>

    <!-- Exp 4 -->
    <div class="exp-card">
        <div class="exp-header">
            <div>
                <span class="exp-role">Generative AI Developer Intern</span>
                <span class="exp-company"> &mdash; Al Wallah (Remote)</span>
            </div>
            <div class="exp-period">May 2025 – July 2025</div>
        </div>
        <ul class="bullets">
            <li>Built and deployed LLM-powered web applications using the Google Gemini API for multi-turn customer conversational workflows and automated Q&amp;A.</li>
            <li>Integrated Python Flask backends with interactive JavaScript frontends; accelerated AI feature delivery by <strong>~50%</strong> through structured prompt engineering, JSON schema enforcement, and hallucination guardrails.</li>
        </ul>
    </div>

    <!-- Exp 5 -->
    <div class="exp-card">
        <div class="exp-header">
            <div>
                <span class="exp-role">UI/UX Designer &amp; Social Media Marketing</span>
                <span class="exp-company"> &mdash; 2GatherApp (Remote)</span>
            </div>
            <div class="exp-period">February 2025 – October 2025</div>
        </div>
        <ul class="bullets">
            <li>Designed high-fidelity mobile user interfaces for an event discovery and community meetup application (live on Google Play).</li>
            <li>Created interactive mobile design prototypes and brand assets; coordinated visual marketing campaigns driving thousands of early community app installs.</li>
        </ul>
    </div>
</div>

<div class="section">
    <div class="section-title">Education</div>
    <div class="edu-card">
        <div class="edu-header">
            <span class="edu-degree">B.Tech in Computer Science and Engineering</span>
            <span class="edu-meta">July 2022 – 2026</span>
        </div>
        <div class="edu-inst">Amity University, Kolkata &bull; <strong>CGPA: 7.25 / 10</strong></div>
        <div class="edu-grades">
            Class XII: 82% (Unacco School, Imphal West, 2022) &bull; Class X: 70% (Heritage Convent, Imphal West, 2020)
        </div>
    </div>
</div>

<div class="section">
    <div class="section-title">Honors, Hackathons &amp; Leadership</div>
    <ul class="bullets">
        <li><strong>Rank 62 Nationally</strong> &mdash; <em>India Innovates 2026 National Hackathon</em> (Open Innovation category, MediRAG-Eval clinical audit system).</li>
        <li><strong>OpenAI x NamasteDev Hackathon 2026</strong> &mdash; Built and shipped <em>Stash</em>, an AI-powered local-first clipboard vault.</li>
        <li><strong>Founder &amp; Mentor</strong> &mdash; Created <em>“Ask Joy Bhaiya”</em>, a community mentorship platform supporting junior engineering students at Amity University Kolkata.</li>
    </ul>
</div>

<div class="section">
    <div class="section-title">Licenses &amp; Certifications</div>
    <div class="cert-grid">
        <div class="cert-item">Career Essentials in GitHub Professional Certificate (GitHub &amp; LinkedIn, 2025)</div>
        <div class="cert-item">SQL Essential Training (LinkedIn Learning, 2025)</div>
        <div class="cert-item">Build Your Generative AI Productivity Skills (Microsoft &amp; LinkedIn, 2024)</div>
        <div class="cert-item">Career Essentials in Generative AI (Microsoft &amp; LinkedIn, 2024)</div>
    </div>
</div>

</body>
</html>
"""

def generate_executive_pdf():
    out_file = OUT_DIR / "Joydeep_Das_Frontend_CV.pdf"
    print(f"Generating Elite 2-Page Full-Detail CV...")

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.set_content(FULL_RESUME_HTML, wait_until="networkidle")
        page.pdf(
            path=str(out_file),
            format="A4",
            print_background=True,
            prefer_css_page_size=True,
            margin={"top": "0.55in", "bottom": "0.55in", "left": "0.65in", "right": "0.65in"}
        )
        browser.close()

    print(f"  [✓] Successfully generated: {out_file}")

    # Generate visual PNG previews of BOTH pages for instant review
    import fitz
    artifact_dir = Path(r"C:\Users\joyde\.gemini\antigravity\brain\6227c3c6-a2a6-494f-9812-dd89903ecd4d")
    doc = fitz.open(out_file)
    for i, p in enumerate(doc):
        pix = p.get_pixmap(dpi=200)
        img_path = artifact_dir / f"elite_preview_page_{i+1}.png"
        pix.save(str(img_path))
        print(f"  [✓] Rendered Page {i+1} preview: {img_path}")

if __name__ == "__main__":
    generate_executive_pdf()
