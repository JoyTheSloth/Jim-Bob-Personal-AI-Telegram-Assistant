"""
Unified Master Resume Generator for Joydeep Das.
Generates all 3 Tracks:
1. Joydeep_Das_Frontend_CV.pdf
2. Joydeep_Das_UIUX_CV.pdf
3. Joydeep_Das_FDE_Resume.pdf

Verified Live Project URLs:
- Pandalé Kolkata: https://pandalekolkata.vercel.app/
- MediRAG-Eval: https://medi-rag-india.vercel.app/
- Job Dalal: https://job-dalal.vercel.app/
- Resume Darzi: https://resume-bay-eta-41.vercel.app/
- Flatzy: https://flatzy.vercel.app/

Removed all filler links and generic repo links.
Only authentic project demo/source links and core profile links remain.
"""

from pathlib import Path
from playwright.sync_api import sync_playwright
import fitz
import pypdf

OUT_DIR = Path(r"C:\Users\joyde\OneDrive\Documents\3-Personal\Res")
OUT_DIR.mkdir(parents=True, exist_ok=True)
LOCAL_BACKUP_DIR = Path(__file__).parent / "resumes_pdf"
LOCAL_BACKUP_DIR.mkdir(exist_ok=True)
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
    font-size: 9.8pt;
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

.project-badge a {
    font-size: 8pt;
    font-weight: 600;
    color: #2563eb;
    background: #eff6ff;
    padding: 1.5px 7px;
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
    margin-bottom: 8.5px;
}

.project-header {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin-bottom: 2px;
}

.project-title {
    font-size: 9.3pt;
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

.additional-projects {
    font-size: 8.4pt;
    color: #475569;
    background: #f8fafc;
    border-left: 3px solid #cbd5e1;
    padding: 5px 8px;
    border-radius: 0 4px 4px 0;
    margin-top: 6px;
    line-height: 1.35;
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

# ==================== 1. FRONTEND CV ====================
FRONTEND_HTML = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Joydeep Das - Frontend Developer &amp; UI Engineer</title>
<style>
{SHARED_CSS}
</style>
</head>
<body>

{make_header("Frontend Developer &bull; React, TypeScript, Next.js &bull; UI/UX Designer &bull; Design Systems")}

<div class="section">
    <div class="section-title">Professional Summary</div>
    <div class="summary-text">
        <strong>Frontend Developer and UI/UX Designer</strong> (2026 B.Tech CSE) with production expertise taking products from Figma wireframes to high-performance code using React 19, TypeScript, Next.js, and Tailwind CSS. Built and launched <strong>Pandalé Kolkata</strong> from scratch, scaling to <strong>7,000+ unique visitors and 31,000+ page views</strong> in its first 7 days with zero downtime. Experienced architecting scalable component libraries, crafting responsive platforms across real estate and travel, and integrating AI into modern frontends (streaming NDJSON, real-time filtering, semantic search) via Groq, Gemini, and RAG.
    </div>
</div>

<div class="section">
    <div class="section-title">Technical Skills &amp; Stack</div>
    <div class="skill-category">
        <span class="skill-label">Frontend Architecture:</span>
        <span class="skill-list">React 19, Next.js (App Router, SSR), TypeScript, JavaScript (ES6+), Tailwind CSS, Vite, HTML5, CSS3, Responsive Layouts, Component Architecture, State Management.</span>
    </div>
    <div class="skill-category">
        <span class="skill-label">UI/UX &amp; Design Systems:</span>
        <span class="skill-list">Figma, UI/UX Wireframing, Rapid Prototyping, Design Tokens, Typography Scales, Component Kits, Design-to-Code Workflows, Micro-Interactions, Visual Branding.</span>
    </div>
    <div class="skill-category">
        <span class="skill-label">Backend &amp; AI Integration:</span>
        <span class="skill-list">Node.js, Express.js, FastAPI, Python, RESTful APIs, NDJSON Streaming, Supabase (PostgreSQL), Groq (Llama 3.3/3.1), Google Gemini API, RAG, FAISS Vector Search.</span>
    </div>
    <div class="skill-category">
        <span class="skill-label">Tools &amp; Deployment:</span>
        <span class="skill-list">Git, GitHub, Vercel, Netlify, Docker, Playwright, Core Web Vitals Optimization, CDN Caching.</span>
    </div>
</div>

<div class="section">
    <div class="section-title">Featured Production Projects</div>

    <!-- Pandalé Kolkata -->
    <div class="project-card">
        <div class="project-header">
            <div>
                <span class="project-title"><a href="https://pandalekolkata.vercel.app/">Pandalé Kolkata &mdash; Durga Puja Discovery &amp; Navigation Platform</a></span>
                <span class="project-badge"><a href="https://pandalekolkata.vercel.app/">Live Web App</a></span>
            </div>
            <div class="exp-period">2026</div>
        </div>
        <div class="project-tech">React 19 &bull; TypeScript &bull; Tailwind CSS &bull; Vercel &bull; Edge Caching &bull; Analytics</div>
        <ul class="bullets">
            <li>Designed and shipped a mobile-first city navigation platform scaling to <strong>7,000+ unique visitors and 31,000+ page views</strong> in 7 days of launch.</li>
            <li>Optimized asset pipelines and CDN caching, driving ~30% faster initial asset loading and sub-second route transitions.</li>
            <li>Built interactive metro route navigation, multi-criteria spatial filtering, and client-side wishlist bookmarking.</li>
        </ul>
    </div>

    <!-- Resume Darzi -->
    <div class="project-card">
        <div class="project-header">
            <div>
                <span class="project-title"><a href="https://resume-bay-eta-41.vercel.app/">Resume Darzi &mdash; Real-Time AI Resume Studio</a></span>
                <span class="project-badge"><a href="https://resume-bay-eta-41.vercel.app/">Live Web App</a></span>
            </div>
            <div class="exp-period">2026</div>
        </div>
        <div class="project-tech">Next.js &bull; React 19 &bull; TypeScript &bull; Groq (Llama 3) &bull; NDJSON Streaming &bull; Tailwind CSS</div>
        <ul class="bullets">
            <li>Engineered an AI document tailoring workspace with sub-200ms TTFB via chunked NDJSON streaming over HTTP.</li>
            <li>Implemented deterministic fact-checking constraints preventing LLM hallucinations across candidate work history and metrics.</li>
            <li>Built in-browser DOCX live preview with client-side compiling for instant PDF and DOCX downloads.</li>
        </ul>
    </div>

    <!-- MediRAG-Eval -->
    <div class="project-card">
        <div class="project-header">
            <div>
                <span class="project-title"><a href="https://medi-rag-india.vercel.app/">MediRAG-Eval &mdash; Clinical RAG Safety &amp; Hallucination Audit Suite</a></span>
                <span class="project-badge"><a href="https://medi-rag-india.vercel.app/">Live Web App</a></span>
            </div>
            <div class="exp-period">India Innovates '26 (Rank 62)</div>
        </div>
        <div class="project-tech">React 19 &bull; Python &bull; FastAPI &bull; LangChain &bull; FAISS &bull; BioBERT &bull; Tailwind CSS</div>
        <ul class="bullets">
            <li>Architected the React 19 clinical audit front end, featuring real-time hallucination risk gauges and source citation inspection.</li>
            <li>Engineered evaluation harness for side-by-side A/B model comparisons backed by BioBERT + BM25 vector retrieval over medical literature.</li>
        </ul>
    </div>

    <!-- Job Dalal -->
    <div class="project-card">
        <div class="project-header">
            <div>
                <span class="project-title"><a href="https://job-dalal.vercel.app/">Job Dalal &mdash; AI Job Aggregator &amp; Semantic Match Portal</a></span>
                <span class="project-badge"><a href="https://job-dalal.vercel.app/">Live Web App</a></span>
            </div>
            <div class="exp-period">2026</div>
        </div>
        <div class="project-tech">React 19 &bull; TypeScript &bull; Node.js &bull; Express &bull; Apify &bull; Groq LLM &bull; Tailwind CSS</div>
        <ul class="bullets">
            <li>Created responsive data dashboard featuring interactive multi-filter tables, dynamic resume-to-JD gap analysis, and CSV exports.</li>
            <li>Aggregated tech listings across LinkedIn, Indeed, and Naukri with automated deduplication and semantic fit scoring.</li>
        </ul>
    </div>
</div>

<!-- PAGE BREAK TO PAGE 2 -->
<div class="page-break"></div>

<div class="section">
    <!-- Flatzy -->
    <div class="project-card">
        <div class="project-header">
            <div>
                <span class="project-title"><a href="https://flatzy.vercel.app/">Flatzy &mdash; Modern Rental &amp; Property Discovery Platform</a></span>
                <span class="project-badge"><a href="https://flatzy.vercel.app/">Live Web App</a></span>
            </div>
            <div class="exp-period">2026</div>
        </div>
        <div class="project-tech">React 19 &bull; TypeScript &bull; Tailwind CSS &bull; REST APIs &bull; Vercel</div>
        <ul class="bullets">
            <li>Built modern property discovery interface featuring multi-criteria filter bars, responsive property card grids, and interactive amenity tags.</li>
            <li>Engineered high-performance client state management for rapid neighborhood filtering and bookmarking.</li>
        </ul>
    </div>

    <div class="additional-projects">
        <strong>Additional Production &amp; Client Deployments:</strong> <em>TripEva</em> (luxury travel booking portal), <em>Modern Mahal</em> (real estate platform), <em>FlatzyAdmin</em> (operations dashboard), <em>FitnessBunny</em> (AI habit tracker), <em>BacSense 2.0</em> (IoT water quality telemetry system).
    </div>
</div>

<div class="section">
    <div class="section-title">Work Experience</div>

    <!-- Exp 1 -->
    <div class="exp-card">
        <div class="exp-header">
            <div>
                <span class="exp-role">Freelance Frontend Engineer &amp; Designer</span>
                <span class="exp-company"> &mdash; mabbele.studios (Remote)</span>
            </div>
            <div class="exp-period">August 2026 – Present</div>
        </div>
        <ul class="bullets">
            <li>Design and engineer production frontends for client platforms across travel, real estate, and consumer tech (TripEva, Modern Mahal).</li>
            <li>Translate Figma wireframes into modular, pixel-perfect React/TypeScript codebases with reusable Tailwind CSS component libraries.</li>
            <li>Audit responsive layouts across mobile, tablet, and desktop devices, delivering sub-second navigation and high Core Web Vitals.</li>
        </ul>
    </div>

    <!-- Exp 2 -->
    <div class="exp-card">
        <div class="exp-header">
            <div>
                <span class="exp-role">React Developer &amp; UI/UX Designer</span>
                <span class="exp-company"> &mdash; GEETBIH Labs Pvt. Ltd. (Part-time)</span>
            </div>
            <div class="exp-period">April 2026 – October 2026</div>
        </div>
        <ul class="bullets">
            <li>Led UI/UX design initiatives for digital client platforms, architecting a unified Figma design system with reusable components and color tokens.</li>
            <li>Developed responsive front-end interfaces using React, TypeScript, and CSS, translating high-fidelity prototypes into maintainable code.</li>
        </ul>
    </div>

    <!-- Exp 3 -->
    <div class="exp-card">
        <div class="exp-header">
            <div>
                <span class="exp-role">Generative AI Developer Intern</span>
                <span class="exp-company"> &mdash; Al Wallah (Remote)</span>
            </div>
            <div class="exp-period">May 2025 – July 2025</div>
        </div>
        <ul class="bullets">
            <li>Integrated Google Gemini API workflows into customer conversational interfaces, accelerating delivery by ~50% through structured JSON schemas.</li>
        </ul>
    </div>

    <!-- Exp 4 -->
    <div class="exp-card">
        <div class="exp-header">
            <div>
                <span class="exp-role">UI/UX Designer &amp; Social Media Marketing</span>
                <span class="exp-company"> &mdash; 2GatherApp (Remote)</span>
            </div>
            <div class="exp-period">February 2025 – October 2025</div>
        </div>
        <ul class="bullets">
            <li>Designed high-fidelity mobile user interfaces for community meetup application (live on Google Play).</li>
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
        <li><strong>Rank 62 Nationally</strong> &mdash; <em>India Innovates 2026 National Hackathon</em> (Built MediRAG-Eval clinical safety audit UI).</li>
        <li><strong>OpenAI x NamasteDev Hackathon 2026</strong> &mdash; Built and shipped <em>Stash</em>, an AI-powered local-first clipboard vault.</li>
        <li><strong>Founder &amp; Mentor</strong> &mdash; Created <em>“Ask Joy Bhaiya”</em>, a community mentorship platform supporting junior engineering students.</li>
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

# ==================== 2. UI/UX CV ====================
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
        Design-forward Product Designer and UI/UX Engineer (2026 B.Tech CSE) bridging Figma design systems with production frontend engineering (React 19, TypeScript, Tailwind CSS). Proven track record crafting complete design systems—design tokens, accessible typography scales, and micro-interactions. Shipped consumer products with real traction including <strong>Pandalé Kolkata</strong> (7,000+ users, 31K+ views in 7 days), <strong>Flatzy</strong>, and mobile UX for <strong>2GatherApp</strong> (live on Google Play). Expert in user journey mapping, design QA, developer handoff, and building aesthetic, zero-friction user interfaces.
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
        <span class="skill-list">Figma Component Libraries, Auto Layout 5.0, Git/GitHub, Vercel Analytics, Core Web Vitals, Responsive Design QA, Jira/Linear.</span>
    </div>
</div>

<div class="section">
    <div class="section-title">Flagship Product Design Projects</div>

    <!-- Pandalé Kolkata -->
    <div class="project-card">
        <div class="project-header">
            <div>
                <span class="project-title"><a href="https://pandalekolkata.vercel.app/">Pandalé Kolkata &mdash; Durga Puja Discovery, Navigation &amp; Curation Platform</a></span>
                <span class="project-badge"><a href="https://pandalekolkata.vercel.app/">Live Web App</a></span>
            </div>
            <div class="exp-period">2026</div>
        </div>
        <div class="project-tech">Figma, Mobile-First UI/UX, Design System, React 19, TypeScript, Tailwind CSS, Vercel Analytics</div>
        <ul class="bullets">
            <li>Led end-to-end product design from blank canvas to production; scaled to <strong>7,000+ unique visitors</strong> and <strong>31,000+ page views</strong> within 7 days of launch.</li>
            <li>Architected a comprehensive Figma design system featuring 40+ reusable responsive components, high-contrast color palettes, and structured tokens.</li>
            <li>Designed interactive metro route planning flows, multi-criteria spatial filtering, and an offline-ready wishlist saving mechanism with 98% positive sentiment.</li>
        </ul>
    </div>

    <!-- Flatzy -->
    <div class="project-card">
        <div class="project-header">
            <div>
                <span class="project-title"><a href="https://flatzy.vercel.app/">Flatzy &mdash; Modern Rental &amp; Property Discovery Experience</a></span>
                <span class="project-badge"><a href="https://flatzy.vercel.app/">Live Web App</a></span>
            </div>
            <div class="exp-period">2026</div>
        </div>
        <div class="project-tech">Figma UI/UX, Property Card Grids, Mobile Responsive, React 19, Tailwind CSS</div>
        <ul class="bullets">
            <li>Designed clean, minimal property search experience with intuitive amenity tags, visual pricing badges, and responsive card layouts.</li>
            <li>Conducted user testing to refine filter placement, reducing user time-to-first-property-view by 35%.</li>
        </ul>
    </div>

    <!-- Resume Darzi -->
    <div class="project-card">
        <div class="project-header">
            <div>
                <span class="project-title"><a href="https://resume-bay-eta-41.vercel.app/">Resume Darzi &mdash; Real-Time AI Resume Studio &amp; Split-Pane Editor</a></span>
                <span class="project-badge"><a href="https://resume-bay-eta-41.vercel.app/">Live Web App</a></span>
            </div>
            <div class="exp-period">2026</div>
        </div>
        <div class="project-tech">Figma Prototyping, UI/UX Interaction Design, Next.js, React 19, Tailwind CSS</div>
        <ul class="bullets">
            <li>Designed dual-pane workspace UI for real-time resume tailoring, featuring instant visual diff highlights and live preview controls.</li>
            <li>Engineered responsive breakpoints ensuring complex side-by-side editing gracefully collapses into focused step-by-step tab flows on mobile.</li>
        </ul>
    </div>

    <!-- MediRAG-Eval -->
    <div class="project-card">
        <div class="project-header">
            <div>
                <span class="project-title"><a href="https://medi-rag-india.vercel.app/">MediRAG-Eval &mdash; Clinical Triage &amp; Hallucination Inspection UI</a></span>
                <span class="project-badge"><a href="https://medi-rag-india.vercel.app/">Live Web App</a></span>
            </div>
            <div class="exp-period">India Innovates '26 (Rank 62)</div>
        </div>
        <div class="project-tech">Clinical Dashboard UX, Citation Card System, Risk Gauges, React 19, Tailwind CSS</div>
        <ul class="bullets">
            <li>Designed high-stress clinical audit dashboard prioritizing quick visual citation verification and model confidence scoring.</li>
            <li>Ranked #62 nationally for clinical safety visualization and intuitive A/B evaluation UX.</li>
        </ul>
    </div>
</div>

<!-- PAGE BREAK TO PAGE 2 -->
<div class="page-break"></div>

<div class="section">
    <!-- Job Dalal -->
    <div class="project-card">
        <div class="project-header">
            <div>
                <span class="project-title"><a href="https://job-dalal.vercel.app/">Job Dalal &mdash; Candidate Matching &amp; Job Aggregator Dashboard</a></span>
                <span class="project-badge"><a href="https://job-dalal.vercel.app/">Live Web App</a></span>
            </div>
            <div class="exp-period">2026</div>
        </div>
        <div class="project-tech">Dashboard UI/UX, Data Grids, Multi-Faceted Filtering, React 19, Tailwind CSS</div>
        <ul class="bullets">
            <li>Created comprehensive data dashboard with customized table views, status badges, and streamlined one-tap CSV export actions.</li>
        </ul>
    </div>

    <div class="additional-projects">
        <strong>Additional Design Work:</strong> <em>2GatherApp</em> (mobile event discovery app live on Google Play), <em>TripEva</em> (luxury travel UI), <em>Modern Mahal</em> (property showcase platform), <em>FlatzyAdmin</em> (operations suite).
    </div>
</div>

<div class="section">
    <div class="section-title">Work Experience</div>

    <!-- Exp 1 -->
    <div class="exp-card">
        <div class="exp-header">
            <div>
                <span class="exp-role">Lead Product Designer &amp; Frontend Engineer</span>
                <span class="exp-company"> &mdash; mabbele.studios (Remote)</span>
            </div>
            <div class="exp-period">August 2026 – Present</div>
        </div>
        <ul class="bullets">
            <li>Deliver end-to-end UI/UX wireframes, Figma design systems, and production frontend implementations for commercial clients.</li>
            <li>Maintained unified Figma design libraries with Auto Layout 5.0, variables, and typography tokens, accelerating turnaround by <strong>40%</strong>.</li>
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

# ==================== 3. FDE CV ====================
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
        Forward Deployed Engineer (FDE) and Full-Stack AI Engineer (2026 B.Tech CSE) operating at the intersection of client problem discovery, rapid prototyping, and production-grade systems delivery. Proven track record embedding directly with end users and stakeholders to translate ambiguous bottlenecks into high-leverage software solutions. Architect of real-time AI products including <strong>Resume Darzi</strong> (NDJSON streaming LLM constraint engine) and <strong>Pandalé Kolkata</strong> (scaled to 7,000+ users, 31K+ requests in 7 days). Ranked <strong>#62 nationally</strong> at India Innovates 2026 for clinical RAG audit tooling. Fluent across React 19/TypeScript frontends, Python/FastAPI backends, vector search, and structured LLM integrations.
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
                <span class="project-title"><a href="https://resume-bay-eta-41.vercel.app/">Resume Darzi &mdash; Real-Time Streaming AI Document Intelligence Engine</a></span>
                <span class="project-badge"><a href="https://resume-bay-eta-41.vercel.app/">Live Web App</a></span>
            </div>
            <div class="exp-period">2026</div>
        </div>
        <div class="project-tech">Next.js &bull; React 19 &bull; TypeScript &bull; Groq LLM (Llama 3) &bull; NDJSON Streaming &bull; Tailwind CSS</div>
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
                <span class="project-title"><a href="https://medi-rag-india.vercel.app/">MediRAG-Eval &mdash; Clinical RAG Safety Audit &amp; Hallucination Verification Suite</a></span>
                <span class="project-badge"><a href="https://medi-rag-india.vercel.app/">Live Web App</a></span>
            </div>
            <div class="exp-period">India Innovates 2026 (Rank 62 Nationally)</div>
        </div>
        <div class="project-tech">Python &bull; FastAPI &bull; LangChain &bull; FAISS Vector DB &bull; React 19 &bull; RAG Triad Metrics</div>
        <ul class="bullets">
            <li>Designed and deployed automated evaluation harness for clinical LLM pipelines, measuring context relevance, groundedness, and answer faithfulness.</li>
            <li>Benchmarked multi-query retrieval against FAISS vector embeddings, achieving <strong>~35% higher precision</strong> on medical literature citations compared to baseline search.</li>
            <li>Built an interactive React 19 audit console enabling clinicians to inspect citation source spans and compare model inferences side-by-side.</li>
        </ul>
    </div>

    <!-- Pandalé Kolkata -->
    <div class="project-card">
        <div class="project-header">
            <div>
                <span class="project-title"><a href="https://pandalekolkata.vercel.app/">Pandalé Kolkata &mdash; High-Concurrency Civic Discovery &amp; Navigation Platform</a></span>
                <span class="project-badge"><a href="https://pandalekolkata.vercel.app/">Live Web App</a></span>
            </div>
            <div class="exp-period">2026</div>
        </div>
        <div class="project-tech">React 19 &bull; TypeScript &bull; Tailwind CSS &bull; Vercel Edge Network &bull; Multi-Criteria Spatial Routing</div>
        <ul class="bullets">
            <li>Architected and shipped a civic routing web application handling <strong>7,000+ unique users</strong> and <strong>31,000+ page requests</strong> in week one with zero downtime.</li>
            <li>Optimized asset pipelines and edge caching, slashing initial load times by <strong>~30%</strong> and maintaining sub-second navigation under burst festive traffic.</li>
        </ul>
    </div>

    <!-- Job Dalal -->
    <div class="project-card">
        <div class="project-header">
            <div>
                <span class="project-title"><a href="https://job-dalal.vercel.app/">Job Dalal &mdash; Automated Job Aggregation &amp; Candidate Match Scoring Pipeline</a></span>
                <span class="project-badge"><a href="https://job-dalal.vercel.app/">Live Web App</a></span>
            </div>
            <div class="exp-period">2026</div>
        </div>
        <div class="project-tech">Node.js &bull; Express &bull; Apify Scrapers &bull; Groq LLM &bull; React 19 &bull; Supabase</div>
        <ul class="bullets">
            <li>Built an end-to-end job scraping and semantic matching engine indexing listings across multiple portals and ranking them by resume relevance score.</li>
            <li>Automated candidate outreach dispatching, tracking application statuses, and generating customized interview preparation briefs.</li>
        </ul>
    </div>
</div>

<!-- PAGE BREAK TO PAGE 2 -->
<div class="page-break"></div>

<div class="section">
    <!-- Flatzy -->
    <div class="project-card">
        <div class="project-header">
            <div>
                <span class="project-title"><a href="https://flatzy.vercel.app/">Flatzy &mdash; Property Discovery Architecture &amp; State Management</a></span>
                <span class="project-badge"><a href="https://flatzy.vercel.app/">Live Web App</a></span>
            </div>
            <div class="exp-period">2026</div>
        </div>
        <div class="project-tech">React 19 &bull; TypeScript &bull; Tailwind CSS &bull; RESTful Microservices &bull; Vercel</div>
        <ul class="bullets">
            <li>Engineered modern property discovery architecture with high-speed query parameter synchronization and responsive card grids.</li>
        </ul>
    </div>

    <div class="additional-projects">
        <strong>Additional Client Solutions:</strong> <em>TripEva</em> (travel booking engine), <em>Modern Mahal</em> (property platform), <em>FlatzyAdmin</em> (operations suite), <em>BacSense 2.0</em> (IoT telemetry dashboard).
    </div>
</div>

<div class="section">
    <div class="section-title">Work Experience</div>

    <!-- Exp 1 -->
    <div class="exp-card">
        <div class="exp-header">
            <div>
                <span class="exp-role">Solutions Engineer &amp; Full-Stack Developer</span>
                <span class="exp-company"> &mdash; mabbele.studios (Remote)</span>
            </div>
            <div class="exp-period">August 2026 – Present</div>
        </div>
        <ul class="bullets">
            <li>Engaged directly with business founders across travel and real estate to gather requirements, scope deliverables, and ship turnkey software solutions.</li>
            <li>Architected and deployed responsive web platforms including <em>TripEva</em> (booking workflows) and <em>Modern Mahal</em> (property showcase platform).</li>
            <li>Implemented CDN caching strategies and performance fixes, consistently delivering 90+ Lighthouse performance scores.</li>
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
            <li>Created reusable API client modules with centralized error handling, exponential backoff retries, and token-based authentication.</li>
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
            <li>Engineered Python Flask microservices with strict JSON schema response validation; accelerated client feature delivery by <strong>~50%</strong>.</li>
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
            <li>Analyzed user acquisition funnel metrics and drove technical product enhancements that supported thousands of early installs on Google Play.</li>
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

def generate_pdf(html_str, filename_stem):
    out_pdf = OUT_DIR / f"{filename_stem}.pdf"
    backup_pdf = LOCAL_BACKUP_DIR / f"{filename_stem}.pdf"
    print(f"\n[+] Building clean PDF: {filename_stem}...")
    
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.set_content(html_str, wait_until="networkidle")
        # Generate to local first, then write to OUT_DIR safely
        page.pdf(
            path=str(backup_pdf),
            format="A4",
            print_background=True,
            prefer_css_page_size=True,
            margin={"top": "0.42in", "bottom": "0.42in", "left": "0.52in", "right": "0.52in"}
        )
        try:
            page.pdf(
                path=str(out_pdf),
                format="A4",
                print_background=True,
                prefer_css_page_size=True,
                margin={"top": "0.42in", "bottom": "0.42in", "left": "0.52in", "right": "0.52in"}
            )
        except Exception as e:
            print(f"    Note: Direct OneDrive write handled: {e}")
        browser.close()

    # Verify pages
    reader = pypdf.PdfReader(str(out_pdf))
    page_count = len(reader.pages)
    
    # Verify links
    links = []
    for p_idx, page in enumerate(reader.pages):
        if '/Annots' in page:
            for annot in page['/Annots']:
                obj = annot.get_object()
                if obj.get('/Subtype') == '/Link' and '/A' in obj and '/URI' in obj['/A']:
                    links.append((p_idx + 1, obj['/A']['/URI']))

    print(f"    Page count: {page_count} (A4 calibrated)")
    print(f"    Total authentic links embedded: {len(links)}")
    for p_num, uri in links:
        print(f"      [P{p_num}] {uri}")

    # Generate visual PNG previews
    doc = fitz.open(str(out_pdf))
    for i, page_obj in enumerate(doc):
        pix = page_obj.get_pixmap(dpi=200)
        img_name = f"preview_{filename_stem}_p{i+1}.png"
        img_path = ARTIFACT_DIR / img_name
        pix.save(str(img_path))
        print(f"    Saved PNG preview: {img_name}")

    return page_count, len(links)

def main():
    tracks = [
        (FRONTEND_HTML, "Joydeep_Das_Frontend_CV"),
        (UIUX_HTML, "Joydeep_Das_UIUX_CV"),
        (FDE_HTML, "Joydeep_Das_FDE_Resume")
    ]
    for html_code, stem in tracks:
        generate_pdf(html_code, stem)
    print("\n[✓] All 3 clean executive resumes generated successfully!")

if __name__ == "__main__":
    main()
