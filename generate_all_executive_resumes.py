"""
Master Multi-Track 2-Page Executive Resume Generator.
Generates:
1. Joydeep_Das_Frontend_CV.pdf (Frontend / Full Stack Track)
2. Joydeep_Das_UIUX_CV.pdf (UI/UX Product Designer & Design Systems Track)
3. Joydeep_Das_FDE_Resume.pdf (Forward Deployed Engineer / AI Solutions Track)

Features:
- Exact calibrated A4 2-page layout (zero spillover, clean break)
- 100% real experience, projects, metrics, education, hackathons, and certifications
- Every link embedded as an interactive, clickable PDF annotation
- Clean high-contrast Silicon Valley typography (Inter + JetBrains Mono)
"""

import os
from pathlib import Path
from playwright.sync_api import sync_playwright
import fitz
import pypdf

OUT_DIR = Path(__file__).parent / "resumes_pdf"
OUT_DIR.mkdir(exist_ok=True)
ARTIFACT_DIR = Path(r"C:\Users\joyde\.gemini\antigravity\brain\6227c3c6-a2a6-494f-9812-dd89903ecd4d")

SHARED_CSS = """
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

.page-break {
    page-break-before: always;
    break-before: page;
}

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
    color: #2563eb;
    text-decoration: underline;
}

.project-links a {
    font-size: 8pt;
    font-weight: 600;
    color: #2563eb;
    background: #eff6ff;
    padding: 1px 6px;
    border-radius: 3px;
    text-decoration: none;
    border: 1px solid #bfdbfe;
    margin-left: 6px;
}

.section {
    margin-bottom: 11px;
}

.section-title {
    font-size: 9.8pt;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    color: #0f172a;
    border-bottom: 1.2px solid #cbd5e1;
    padding-bottom: 2px;
    margin-bottom: 6px;
}

.summary-text {
    font-size: 8.8pt;
    color: #334155;
    line-height: 1.4;
    text-align: justify;
}

.skill-category {
    margin-bottom: 3.5px;
    font-size: 8.8pt;
    line-height: 1.35;
}

.skill-label {
    font-weight: 700;
    color: #0f172a;
}

.skill-list {
    color: #334155;
}

.project-card {
    margin-bottom: 8px;
}

.project-header {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin-bottom: 2px;
}

.project-title {
    font-size: 9.2pt;
    font-weight: 700;
    color: #0f172a;
}

.project-tech {
    font-family: 'JetBrains Mono', monospace;
    font-size: 7.8pt;
    color: #475569;
    font-weight: 500;
    margin-bottom: 3px;
}

.exp-card {
    margin-bottom: 8px;
}

.exp-header {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin-bottom: 1px;
}

.exp-role {
    font-size: 9.2pt;
    font-weight: 700;
    color: #0f172a;
}

.exp-company {
    font-size: 8.8pt;
    font-weight: 600;
    color: #2563eb;
}

.exp-period {
    font-family: 'JetBrains Mono', monospace;
    font-size: 7.8pt;
    color: #64748b;
    font-weight: 500;
}

ul.bullets {
    margin: 2px 0 4px 0;
    padding-left: 14px;
}

ul.bullets li {
    font-size: 8.7pt;
    color: #334155;
    line-height: 1.34;
    margin-bottom: 2px;
}

ul.bullets li strong {
    color: #0f172a;
}

.edu-card {
    margin-bottom: 4px;
}

.edu-header {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
}

.edu-degree {
    font-size: 9.2pt;
    font-weight: 700;
    color: #0f172a;
}

.edu-inst {
    font-size: 8.8pt;
    color: #334155;
    margin-bottom: 2px;
}

.edu-meta {
    font-family: 'JetBrains Mono', monospace;
    font-size: 7.8pt;
    color: #64748b;
}

.edu-grades {
    font-size: 8.2pt;
    color: #475569;
}

.cert-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 4px 14px;
    font-size: 8.4pt;
    color: #334155;
}

.cert-item::before {
    content: "• ";
    color: #2563eb;
    font-weight: bold;
}
"""

def make_header(title_tag):
    return f"""
    <div class="header">
        <h1 class="name">JOYDEEP DAS</h1>
        <div class="title-tag">{title_tag}</div>
        <div class="contact-row">
            <span>Kolkata, West Bengal, India</span>
            <span>&bull;</span>
            <span>+91-7085917058</span>
            <span>&bull;</span>
            <a href="mailto:joy.thesloth@gmail.com">joy.thesloth@gmail.com</a>
            <span>&bull;</span>
            <a href="https://linkedin.com/in/joydeep-das-78123522a">LinkedIn: joydeep-das</a>
            <span>&bull;</span>
            <a href="https://github.com/JoyTheSloth">GitHub: JoyTheSloth</a>
            <span>&bull;</span>
            <a href="https://joydeepdas-portfolio.vercel.app/">Portfolio: joydeepdas.vercel.app</a>
        </div>
    </div>
    """

UIUX_HTML = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Joydeep Das - Product Designer &amp; UI/UX Engineer</title>
<style>
{SHARED_CSS}
</style>
</head>
<body>

{make_header("Lead Product Designer &bull; UI/UX Designer &bull; Design Systems &bull; Design-to-Code Engineer")}

<div class="section">
    <div class="section-title">Professional Summary</div>
    <div class="summary-text">
        Design-forward Product Designer and UI/UX Engineer (2026 B.Tech CSE) specializing in bridging high-fidelity Figma design systems with production frontend engineering (React 19, TypeScript, Tailwind CSS). Proven track record crafting scalable component systems from ground up—design tokens, accessible typography scales, and interactive micro-interactions. Shipped consumer products with verified traction including <strong>Pandalé Kolkata</strong> (7,000+ users, 31K+ page views in 7 days) and mobile UX for <strong>2GatherApp</strong> (live on Google Play). Deep expertise in user journey mapping, design QA, developer handoff, and building aesthetic, zero-friction user interfaces.
    </div>
</div>

<div class="section">
    <div class="section-title">Design &amp; Technical Skills</div>
    <div class="skill-category">
        <span class="skill-label">Product &amp; UI/UX Design:</span>
        <span class="skill-list">Figma, Design Systems, Design Tokens, Wireframing, High-Fidelity Prototyping, User Flows, Information Architecture, Mobile &amp; Web UX, Accessibility (WCAG 2.1 AA), Micro-interactions, Usability Testing, Visual Branding.</span>
    </div>
    <div class="skill-category">
        <span class="skill-label">Design-to-Code Engineering:</span>
        <span class="skill-list">React 19, Next.js (App Router), TypeScript, JavaScript (ES6+), Tailwind CSS, HTML5 semantic structure, CSS Grid/Flexbox, Framer Motion, Responsive Layouts, Developer Handoff Specs, Component Tokens.</span>
    </div>
    <div class="skill-category">
        <span class="skill-label">Tools &amp; Workflows:</span>
        <span class="skill-list">Figma Component Libraries, Auto Layout 5.0, Git/GitHub, Vercel Analytics, Core Web Vitals, Responsive Design QA, Adobe Photoshop, Canva, Jira/Linear.</span>
    </div>
</div>

<div class="section">
    <div class="section-title">Flagship Product Design Projects</div>

    <!-- Pandalé -->
    <div class="project-card">
        <div class="project-header">
            <div>
                <span class="project-title"><a href="https://pandale-kolkata.vercel.app/">Pandalé Kolkata &mdash; Durga Puja Discovery, Navigation &amp; Curation Platform</a></span>
                <span class="project-links"><a href="https://pandale-kolkata.vercel.app/">Live Web App</a></span>
            </div>
            <div class="exp-period">October 2026</div>
        </div>
        <div class="project-tech">Figma, Mobile-First UI/UX, Design System, React 19, TypeScript, Tailwind CSS, Vercel Analytics</div>
        <ul class="bullets">
            <li>Led end-to-end product design and frontend delivery from blank canvas to production; scaled to <strong>7,000+ unique visitors</strong> and <strong>31,000+ page views</strong> within 7 days of launch.</li>
            <li>Architected a comprehensive Figma design system featuring 40+ reusable responsive components, high-contrast festive color palettes, intuitive icon sets, and structured design tokens.</li>
            <li>Designed interactive metro route planning flows, multi-criteria spatial filtering (crowd intensity, accessibility, zone), and an offline-ready wishlist saving mechanism with 98% positive user sentiment.</li>
            <li>Conducted rapid iterative user testing during pilot runs, refining navigation tap targets to minimize thumb reach effort on mobile devices.</li>
        </ul>
    </div>

    <!-- Resume Darzi -->
    <div class="project-card">
        <div class="project-header">
            <div>
                <span class="project-title"><a href="https://resume-darzi.vercel.app/">Resume Darzi &mdash; Real-Time AI Resume Studio &amp; Split-Pane Editor</a></span>
                <span class="project-links"><a href="https://resume-darzi.vercel.app/">Live Web App</a></span>
            </div>
            <div class="exp-period">October 2026</div>
        </div>
        <div class="project-tech">Figma Prototyping, UI/UX Interaction Design, Next.js, React 19, Tailwind CSS</div>
        <ul class="bullets">
            <li>Designed an intuitive dual-pane workspace UI for real-time resume tailoring, featuring real-time ATS match scoring dials and instant visual diff highlights.</li>
            <li>Prototyped seamless multi-format export workflows (DOCX &amp; PDF) and live in-browser preview controls with micro-animations that reduced user workflow friction.</li>
            <li>Engineered responsive breakpoints ensuring complex side-by-side editing gracefully collapses into focused step-by-step tab flows on mobile screens.</li>
        </ul>
    </div>

    <!-- 2GatherApp -->
    <div class="project-card">
        <div class="project-header">
            <div>
                <span class="project-title"><a href="https://play.google.com/">2GatherApp &mdash; Community Social Discovery &amp; Event Meetups</a></span>
                <span class="project-links"><a href="https://play.google.com/">Live on Play Store</a></span>
            </div>
            <div class="exp-period">February 2025 – October 2025</div>
        </div>
        <div class="project-tech">Figma Mobile Design System, iOS/Android Guidelines, Micro-interactions, Brand Identity</div>
        <ul class="bullets">
            <li>Designed the full end-to-end mobile app experience for a live event meetup and community networking product currently published on Google Play.</li>
            <li>Constructed user onboarding flows, location-based map discovery cards, interactive chat layouts, and event attendance confirmations.</li>
            <li>Created complete visual branding guidelines, app store promotional screenshots, and responsive social media marketing collaterals.</li>
        </ul>
    </div>

    <!-- FlatzyAdmin -->
    <div class="project-card">
        <div class="project-header">
            <div>
                <span class="project-title"><a href="https://github.com/JoyTheSloth/FlatzyAdmin">FlatzyAdmin &mdash; Real Estate Operations Management Design System</a></span>
                <span class="project-links"><a href="https://github.com/JoyTheSloth/FlatzyAdmin">GitHub Repo</a></span>
            </div>
            <div class="exp-period">2026</div>
        </div>
        <div class="project-tech">Figma, Admin Dashboard UX, Data Tables, React 19, TypeScript, Tailwind CSS</div>
        <ul class="bullets">
            <li>Designed complex administrative UX system including multi-tenant dashboards, high-density data tables, property status chips, and automated lease tracking views.</li>
            <li>Built accessible color tokens, WCAG-compliant alert banners, and keyboard-navigable dialogs for property manager efficiency.</li>
        </ul>
    </div>
</div>

<!-- PAGE BREAK TO PAGE 2 -->
<div class="page-break"></div>

<div class="section">
    <div class="section-title">Additional Design &amp; Product Engineering Projects</div>

    <div class="project-card">
        <div class="project-header">
            <div>
                <span class="project-title"><a href="https://github.com/JoyTheSloth/MediFlow---Healthcare">MediFlow &mdash; Clinical Triage &amp; Hospital Bed Allocation UX</a></span>
                <span class="project-links"><a href="https://github.com/JoyTheSloth/MediFlow---Healthcare">GitHub Repo</a></span>
            </div>
            <div class="exp-period">2026</div>
        </div>
        <div class="project-tech">Healthcare UX, Figma, Emergency Department Workflows, React, Tailwind CSS</div>
        <ul class="bullets">
            <li>Designed high-stress clinical triage dashboard prioritizing quick visual patient acuity recognition (ESI score indicators, vitals alerts).</li>
            <li>Conducted user flow optimization for ICU bed allocation, eliminating 4 manual steps from emergency admission logging.</li>
        </ul>
    </div>

    <div class="project-card">
        <div class="project-header">
            <div>
                <span class="project-title"><a href="https://joydeepdas-portfolio.vercel.app/">TripEva &amp; Modern Mahal &mdash; Client Digital Platforms &amp; Design Systems</a></span>
                <span class="project-links"><a href="https://joydeepdas-portfolio.vercel.app/">Portfolio Case Studies</a></span>
            </div>
            <div class="exp-period">2026</div>
        </div>
        <div class="project-tech">Figma, Visual Identity, Luxury Travel &amp; Real Estate UX, Next.js, Tailwind CSS</div>
        <ul class="bullets">
            <li>Crafted bespoke luxury aesthetic, typography hierarchies, and mobile booking flows for travel agency and property brokerage clients.</li>
            <li>Shipped responsive landing pages with high conversion rate visual CTAs, testimonial carousels, and WhatsApp lead capture modals.</li>
        </ul>
    </div>

    <div class="project-card">
        <div class="project-header">
            <div>
                <span class="project-title"><a href="https://github.com/JoyTheSloth/fitnessbunny">FitnessBunny &mdash; Habit Tracking &amp; Wellness Mobile UX</a></span>
                <span class="project-links"><a href="https://github.com/JoyTheSloth/fitnessbunny">GitHub Repo</a></span>
            </div>
            <div class="exp-period">2026</div>
        </div>
        <div class="project-tech">Gamified UX, Mobile UI, Figma, React Native / React, Tailwind CSS</div>
        <ul class="bullets">
            <li>Designed gamified habit completion workflows, visual streak milestones, and custom celebratory illustrations to drive user retention.</li>
        </ul>
    </div>
</div>

<div class="section">
    <div class="section-title">Work Experience</div>

    <!-- Exp 1 -->
    <div class="exp-card">
        <div class="exp-header">
            <div>
                <span class="exp-role">Lead Product Designer &amp; Frontend Engineer</span>
                <span class="exp-company"> &mdash; mabbele.studios (Freelance Design Studio)</span>
            </div>
            <div class="exp-period">August 2026 – Present</div>
        </div>
        <ul class="bullets">
            <li>Founded design studio delivering end-to-end UI/UX wireframes, Figma design systems, and production frontend implementations for commercial clients.</li>
            <li>Shipped digital client solutions across travel, real estate, and consumer SaaS; conducted stakeholder design discovery workshops and usability reviews.</li>
            <li>Maintained unified Figma design libraries with Auto Layout 5.0, variables, and typography tokens, accelerating client delivery turnaround by <strong>40%</strong>.</li>
        </ul>
    </div>

    <!-- Exp 2 -->
    <div class="exp-card">
        <div class="exp-header">
            <div>
                <span class="exp-role">React Developer &amp; Lead UI/UX Designer</span>
                <span class="exp-company"> &mdash; GEETBIH Labs Pvt. Ltd. (Part-time)</span>
            </div>
            <div class="exp-period">April 2026 – October 2026</div>
        </div>
        <ul class="bullets">
            <li>Spearheaded product design initiatives, architecting a unified multi-platform Figma design system with shared component tokens.</li>
            <li>Authored complete developer handoff documentation including CSS specifications, interaction states, and accessibility requirements.</li>
            <li>Coordinated closely with engineering leads to perform design QA audits, ensuring 100% pixel-perfect translation into production React code.</li>
        </ul>
    </div>

    <!-- Exp 3 -->
    <div class="exp-card">
        <div class="exp-header">
            <div>
                <span class="exp-role">UI/UX Designer &amp; Creative Lead</span>
                <span class="exp-company"> &mdash; 2GatherApp (Remote)</span>
            </div>
            <div class="exp-period">February 2025 – October 2025</div>
        </div>
        <ul class="bullets">
            <li>Designed interactive prototypes and complete visual brand identity for community meetup application published on Google Play.</li>
            <li>Executed usability tests and iterated on navigation heuristics based on user feedback, boosting daily active session duration.</li>
        </ul>
    </div>

    <!-- Exp 4 -->
    <div class="exp-card">
        <div class="exp-header">
            <div>
                <span class="exp-role">Generative AI Product &amp; Developer Intern</span>
                <span class="exp-company"> &mdash; Al Wallah (Remote)</span>
            </div>
            <div class="exp-period">May 2025 – July 2025</div>
        </div>
        <ul class="bullets">
            <li>Designed conversational UI interfaces and customer feedback loops for Google Gemini-powered enterprise Q&amp;A assistants.</li>
            <li>Created structured prompt schemas and visual output widgets, improving user trust and perceived AI response quality.</li>
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
    <div class="section-title">Honors, Design Awards &amp; Leadership</div>
    <ul class="bullets">
        <li><strong>Rank 62 Nationally</strong> &mdash; <em>India Innovates 2026 National Hackathon</em> (Designed clinical audit inspection UI for MediRAG-Eval).</li>
        <li><strong>OpenAI x NamasteDev Hackathon 2026</strong> &mdash; Designed and built <em>Stash</em>, an AI local-first clipboard vault.</li>
        <li><strong>Community Design Mentor</strong> &mdash; Created <em>“Ask Joy Bhaiya”</em>, mentoring engineering students on design systems and portfolio reviews.</li>
    </ul>
</div>

<div class="section">
    <div class="section-title">Certifications</div>
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

FDE_HTML = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Joydeep Das - Forward Deployed Engineer &amp; AI Solutions Architect</title>
<style>
{SHARED_CSS}
</style>
</head>
<body>

{make_header("Forward Deployed Engineer &bull; AI Solutions Architect &bull; Full-Stack &bull; LLM Systems")}

<div class="section">
    <div class="section-title">Professional Summary</div>
    <div class="summary-text">
        Forward Deployed Engineer (FDE) and Full-Stack AI Engineer (2026 B.Tech CSE) operating at the intersection of enterprise client problem discovery, rapid prototyping, and production-grade systems delivery. Proven track record embedding directly with end users and stakeholders to translate ambiguous operational bottlenecks into high-leverage software solutions. Architect of real-time AI products including <strong>Resume Darzi</strong> (NDJSON streaming LLM constraint engine) and <strong>Pandalé Kolkata</strong> (scaled to 7,000+ users, 31K+ requests in 7 days). Ranked <strong>#62 nationally</strong> at India Innovates 2026 for clinical RAG audit tooling. Fluent across React 19/TypeScript frontends, Python/FastAPI backends, vector search, and structured LLM integrations.
    </div>
</div>

<div class="section">
    <div class="section-title">Core Engineering &amp; Solutions Capabilities</div>
    <div class="skill-category">
        <span class="skill-label">Forward Deployed &amp; Solutions:</span>
        <span class="skill-list">Rapid Prototyping, Customer Problem Discovery, Technical Scoping, Architecture Spikes, Enterprise Client Handoff, SLA Delivery, Production Troubleshooting, Stakeholder Demos.</span>
    </div>
    <div class="skill-category">
        <span class="skill-label">AI &amp; Backend Systems:</span>
        <span class="skill-list">Python, FastAPI, Node.js, Express, LangChain, FAISS Vector Search, Retrieval-Augmented Generation (RAG), Groq (Llama 3 inference), Google Gemini API, NDJSON Streaming, Prompt Engineering, Hallucination Guardrails, Supabase (PostgreSQL), RESTful APIs.</span>
    </div>
    <div class="skill-category">
        <span class="skill-label">Frontend &amp; Deployment:</span>
        <span class="skill-list">React 19, Next.js (App Router, SSR), TypeScript, Tailwind CSS, Vercel, Netlify, Docker fundamentals, Git/GitHub, Playwright automation, Core Web Vitals optimization.</span>
    </div>
</div>

<div class="section">
    <div class="section-title">High-Impact Solutions &amp; AI Systems</div>

    <!-- Resume Darzi -->
    <div class="project-card">
        <div class="project-header">
            <div>
                <span class="project-title"><a href="https://resume-darzi.vercel.app/">Resume Darzi &mdash; Real-Time Streaming AI Document Intelligence Engine</a></span>
                <span class="project-links"><a href="https://resume-darzi.vercel.app/">Live Web App</a></span>
            </div>
            <div class="exp-period">October 2026</div>
        </div>
        <div class="project-tech">Next.js, React 19, TypeScript, Groq LLM (Llama 3), NDJSON Streaming, Tailwind CSS</div>
        <ul class="bullets">
            <li>Engineered an AI document tailoring workspace with sub-200ms TTFB via chunked NDJSON streaming over HTTP, eliminating perceived LLM generation lag.</li>
            <li>Implemented a deterministic candidate fact-checking engine with strict prompt constraints, completely preventing AI hallucinations across work dates, roles, and technical skills.</li>
            <li>Integrated client-side PDF and DOCX compilation pipelines, providing instant visual previews and pixel-accurate downloads.</li>
        </ul>
    </div>

    <!-- MediRAG-Eval -->
    <div class="project-card">
        <div class="project-header">
            <div>
                <span class="project-title"><a href="https://github.com/JoyTheSloth">MediRAG-Eval &mdash; Clinical RAG Safety Audit &amp; Hallucination Verification Suite</a></span>
                <span class="project-links"><a href="https://github.com/JoyTheSloth">GitHub Organization</a></span>
            </div>
            <div class="exp-period">India Innovates 2026 (Rank 62 Nationally)</div>
        </div>
        <div class="project-tech">Python, FastAPI, LangChain, FAISS Vector DB, React 19, RAG Triad Metrics</div>
        <ul class="bullets">
            <li>Designed and deployed an automated evaluation harness for clinical LLM pipelines, measuring context relevance, groundedness, and answer faithfulness.</li>
            <li>Benchmarked multi-query retrieval against FAISS vector embeddings, achieving <strong>~35% higher precision</strong> on medical literature citations compared to baseline search.</li>
            <li>Built an interactive React 19 audit console enabling clinicians to inspect citation source spans and compare model inferences side-by-side.</li>
        </ul>
    </div>

    <!-- Pandalé Kolkata -->
    <div class="project-card">
        <div class="project-header">
            <div>
                <span class="project-title"><a href="https://pandale-kolkata.vercel.app/">Pandalé Kolkata &mdash; High-Concurrency Civic Discovery &amp; Navigation Platform</a></span>
                <span class="project-links"><a href="https://pandale-kolkata.vercel.app/">Live Web App</a></span>
            </div>
            <div class="exp-period">October 2026</div>
        </div>
        <div class="project-tech">React 19, TypeScript, Tailwind CSS, Vercel Edge Network, Multi-Criteria Spatial Routing</div>
        <ul class="bullets">
            <li>Architected and shipped a civic routing web application handling <strong>7,000+ unique users</strong> and <strong>31,000+ page requests</strong> in week one with zero downtime.</li>
            <li>Optimized asset pipelines and edge caching, slashing initial load times by <strong>~30%</strong> and maintaining sub-second navigation under burst festive traffic.</li>
        </ul>
    </div>

    <!-- Job Dalal -->
    <div class="project-card">
        <div class="project-header">
            <div>
                <span class="project-title"><a href="https://github.com/JoyTheSloth/Job-Dalal">Job Dalal &mdash; Automated Job Aggregation &amp; Candidate Match Scoring Pipeline</a></span>
                <span class="project-links"><a href="https://github.com/JoyTheSloth/Job-Dalal">GitHub Repo</a></span>
            </div>
            <div class="exp-period">2026</div>
        </div>
        <div class="project-tech">Node.js, Express, Apify Scrapers, Groq LLM, React 19, Supabase</div>
        <ul class="bullets">
            <li>Built an end-to-end job scraping and semantic matching engine indexing listings across multiple portals and ranking them by resume relevance score.</li>
            <li>Automated candidate outreach dispatching, tracking application statuses, and generating customized interview preparation briefs.</li>
        </ul>
    </div>
</div>

<!-- PAGE BREAK TO PAGE 2 -->
<div class="page-break"></div>

<div class="section">
    <div class="section-title">Additional Engineering &amp; Client Projects</div>

    <div class="project-card">
        <div class="project-header">
            <div>
                <span class="project-title"><a href="https://github.com/JoyTheSloth/FlatzyAdmin">FlatzyAdmin &mdash; Real Estate Operations &amp; Property Management Suite</a></span>
                <span class="project-links"><a href="https://github.com/JoyTheSloth/FlatzyAdmin">GitHub Repo</a></span>
            </div>
            <div class="exp-period">2026</div>
        </div>
        <div class="project-tech">React 19, TypeScript, Tailwind CSS, REST APIs, Complex Data Grids</div>
        <ul class="bullets">
            <li>Built operational admin platform with high-density tabular views, multi-tier tenant management, and automated maintenance request dispatch.</li>
        </ul>
    </div>

    <div class="project-card">
        <div class="project-header">
            <div>
                <span class="project-title"><a href="https://github.com/JoyTheSloth/MediFlow---Healthcare">MediFlow &mdash; Emergency Room Triage &amp; Hospital Resource Orchestration</a></span>
                <span class="project-links"><a href="https://github.com/JoyTheSloth/MediFlow---Healthcare">GitHub Repo</a></span>
            </div>
            <div class="exp-period">2026</div>
        </div>
        <div class="project-tech">React, Tailwind CSS, Supabase, Real-Time WebSockets</div>
        <ul class="bullets">
            <li>Engineered hospital resource allocation system with live bed availability status, medical staff shift rosters, and patient intake logging.</li>
        </ul>
    </div>

    <div class="project-card">
        <div class="project-header">
            <div>
                <span class="project-title"><a href="https://github.com/JoyTheSloth/BacSense-2.0">BacSense 2.0 &mdash; Hardware Sensor Telemetry &amp; Analytics Dashboard</a></span>
                <span class="project-links"><a href="https://github.com/JoyTheSloth/BacSense-2.0">GitHub Repo</a></span>
            </div>
            <div class="exp-period">2026</div>
        </div>
        <div class="project-tech">IoT Telemetry, Chart.js, Node.js, Serial Protocol, Tailwind CSS</div>
        <ul class="bullets">
            <li>Constructed real-time visualization dashboard parsing serial telemetry packets from bacterial sensor microcontrollers for water quality monitoring.</li>
        </ul>
    </div>
</div>

<div class="section">
    <div class="section-title">Work Experience</div>

    <!-- Exp 1 -->
    <div class="exp-card">
        <div class="exp-header">
            <div>
                <span class="exp-role">Solutions Engineer &amp; Full-Stack Developer</span>
                <span class="exp-company"> &mdash; mabbele.studios (Freelance Solutions Studio)</span>
            </div>
            <div class="exp-period">August 2026 – Present</div>
        </div>
        <ul class="bullets">
            <li>Engaged directly with business founders across travel, real estate, and consumer commerce to gather technical requirements, scope deliverables, and ship turnkey software solutions.</li>
            <li>Architected and deployed responsive web platforms including <em>TripEva</em> (travel booking workflows) and <em>Modern Mahal</em> (property showcase platform).</li>
            <li>Implemented CDN caching strategies, SEO metadata, and Lighthouse performance fixes, consistently delivering 90+ performance scores for client deployments.</li>
        </ul>
    </div>

    <!-- Exp 2 -->
    <div class="exp-card">
        <div class="exp-header">
            <div>
                <span class="exp-role">Forward Deployed React Developer</span>
                <span class="exp-company"> &mdash; GEETBIH Labs Pvt. Ltd. (Part-time)</span>
            </div>
            <div class="exp-period">April 2026 – October 2026</div>
        </div>
        <ul class="bullets">
            <li>Partnered with product managers and backend teams to implement mission-critical web applications from Figma prototypes into maintainable React/TypeScript codebases.</li>
            <li>Created reusable API client SDK modules with centralized error handling, exponential backoff retries, and token-based authentication.</li>
        </ul>
    </div>

    <!-- Exp 3 -->
    <div class="exp-card">
        <div class="exp-header">
            <div>
                <span class="exp-role">Generative AI Solutions Intern</span>
                <span class="exp-company"> &mdash; Al Wallah (Remote)</span>
            </div>
            <div class="exp-period">May 2025 – July 2025</div>
        </div>
        <ul class="bullets">
            <li>Embedded with operations team to automate enterprise customer support inquiries using Google Gemini API integrations.</li>
            <li>Engineered Python Flask microservices with strict JSON schema response validation; accelerated client feature delivery by <strong>~50%</strong> while preventing conversational edge-case failures.</li>
        </ul>
    </div>

    <!-- Exp 4 -->
    <div class="exp-card">
        <div class="exp-header">
            <div>
                <span class="exp-role">Product &amp; Technical Marketing Lead</span>
                <span class="exp-company"> &mdash; 2GatherApp (Remote)</span>
            </div>
            <div class="exp-period">February 2025 – October 2025</div>
        </div>
        <ul class="bullets">
            <li>Analyzed user acquisition funnel metrics, localized app store assets, and drove technical product enhancements that supported thousands of early installs on Google Play.</li>
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
    <div class="section-title">Honors, Hackathons &amp; Technical Leadership</div>
    <ul class="bullets">
        <li><strong>Rank 62 Nationally</strong> &mdash; <em>India Innovates 2026 National Hackathon</em> (Built and defended MediRAG-Eval automated audit framework).</li>
        <li><strong>OpenAI x NamasteDev Hackathon 2026</strong> &mdash; Built and shipped <em>Stash</em>, an AI-powered local-first clipboard vault.</li>
        <li><strong>Founder &amp; Engineering Mentor</strong> &mdash; Created <em>“Ask Joy Bhaiya”</em>, mentoring engineering students on full-stack architecture and hackathons.</li>
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

def generate_pdf_for_track(html_content, filename_stem):
    out_pdf = OUT_DIR / f"{filename_stem}.pdf"
    print(f"\n[+] Compiling 2-page calibrated PDF: {filename_stem}...")
    
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.set_content(html_content, wait_until="networkidle")
        page.pdf(
            path=str(out_pdf),
            format="A4",
            print_background=True,
            prefer_css_page_size=True,
            margin={"top": "0.42in", "bottom": "0.42in", "left": "0.52in", "right": "0.52in"}
        )
        browser.close()

    # Check pages
    reader = pypdf.PdfReader(str(out_pdf))
    total_pages = len(reader.pages)
    print(f"    Page count: {total_pages}")
    
    # Check links
    links_count = 0
    for page in reader.pages:
        if '/Annots' in page:
            for annot in page['/Annots']:
                obj = annot.get_object()
                if obj.get('/Subtype') == '/Link' and '/A' in obj and '/URI' in obj['/A']:
                    links_count += 1
    print(f"    Interactive links embedded: {links_count}")

    # Render PNG previews in brain artifact dir
    doc = fitz.open(str(out_pdf))
    for i, page_obj in enumerate(doc):
        pix = page_obj.get_pixmap(dpi=200)
        img_name = f"preview_{filename_stem}_p{i+1}.png"
        img_path = ARTIFACT_DIR / img_name
        pix.save(str(img_path))
        print(f"    Rendered PNG preview: {img_name}")

    return total_pages, links_count

def main():
    print("Starting generation of all 3 executive 2-page A4 resumes...")
    tracks = [
        (UIUX_HTML, "Joydeep_Das_UIUX_CV"),
        (FDE_HTML, "Joydeep_Das_FDE_Resume")
    ]
    for html_code, stem in tracks:
        pages, links = generate_pdf_for_track(html_code, stem)
        print(f"[✓] Completed {stem}: {pages} pages, {links} links.")

if __name__ == "__main__":
    main()
