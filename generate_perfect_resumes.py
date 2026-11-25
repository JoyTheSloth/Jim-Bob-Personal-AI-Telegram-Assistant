"""
Pixel-Perfect Resume PDF & DOCX Generator for Joydeep Das.
Generates an ATS-compliant, strictly 1-page or perfectly structured 2-page CV
with modern typography, precise margins, zero overflow, and clean visual hierarchy.
Supports tracks: 'frontend', 'uiux', 'fde'.
"""

import os
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

OUT_DIR = Path(__file__).parent / "resumes_pdf"
OUT_DIR.mkdir(exist_ok=True)

# Complete Resume Data Source for Joydeep Das
RESUME_DATA = {
    "name": "JOYDEEP DAS",
    "location": "Kolkata, West Bengal, India",
    "phone": "+91-7085917058",
    "email": "joy.thesloth@gmail.com",
    "links": [
        {"label": "Portfolio", "url": "https://joydeepdas-portfolio.vercel.app"},
        {"label": "GitHub", "url": "https://github.com/JoyTheSloth"},
        {"label": "LinkedIn", "url": "https://linkedin.com/in/joydeep-das-78123522a"},
    ],
    "tracks": {
        "frontend": {
            "title": "Frontend Developer  |  React, Next.js, TypeScript  |  UI/UX Engineer",
            "summary": "Design-forward Frontend Developer and UI/UX Designer (2026 B.Tech CSE) bridging Figma design systems with production React 19, TypeScript, and Tailwind CSS. Built and launched Pandalé Kolkata from scratch—driving 7,000+ unique visitors and 31K+ page views in 7 days. Experienced delivering responsive client platforms across travel, real estate, and consumer tech with high Core Web Vitals, CDN caching, and streaming AI frontend integrations.",
            "skills": [
                ("Frontend", "React 19, Next.js (App Router, SSR), TypeScript, JavaScript (ES6+), Tailwind CSS, Vite, HTML5, CSS3, Responsive Design, Design Systems"),
                ("Design & Tools", "Figma, UI/UX Wireframing, Rapid Prototyping, Component Kits, Design Tokens, Git, GitHub, Vercel, Netlify"),
                ("Backend & AI", "Node.js, Express, FastAPI, Python, RESTful APIs, NDJSON Streaming, Supabase (PostgreSQL), Groq (Llama 3), Google Gemini API"),
            ],
            "projects": [
                {
                    "title": "Pandalé Kolkata: Durga Puja Discovery & Navigation",
                    "link": "https://pandale-kolkata.vercel.app",
                    "tech": "React, TypeScript, Tailwind CSS, Vercel Analytics",
                    "year": "2026",
                    "bullets": [
                        "Designed and engineered mobile-first discovery platform reaching 7,000+ unique visitors and 31K+ page views in first week.",
                        "Optimized Core Web Vitals and CDN caching, driving ~30% faster initial asset loading and sub-second route transitions.",
                        "Owned end-to-end delivery: Figma design system, interactive metro route planning, wishlist state, and production release."
                    ]
                },
                {
                    "title": "Resume Darzi: Real-Time AI Resume Studio",
                    "link": "https://resume-darzi.vercel.app",
                    "tech": "Next.js, React 19, TypeScript, Groq LLM, Tailwind CSS",
                    "year": "2026",
                    "bullets": [
                        "Built AI tailoring workspace with real-time NDJSON streaming responses for keyword alignment against target job descriptions.",
                        "Engineered zero-hallucination constraint engine enforcing candidate profile facts with in-browser DOCX & PDF live preview."
                    ]
                },
                {
                    "title": "Job Dalal: Dynamic Job Aggregator & Matching Portal",
                    "link": "https://github.com/JoyTheSloth",
                    "tech": "React 19, TypeScript, Node.js, Apify, Groq",
                    "year": "2026",
                    "bullets": [
                        "Created responsive dashboard featuring interactive multi-filter tables, live resume-JD match scoring, and one-tap CSV exports."
                    ]
                },
                {
                    "title": "MediRAG-Eval: Clinical RAG Safety Audit Suite",
                    "link": "https://github.com/JoyTheSloth",
                    "tech": "React 19, FastAPI, LangChain, FAISS",
                    "year": "India Innovates '26 (Rank 62)",
                    "bullets": [
                        "Architected React 19 UI with real-time hallucination risk metrics, citation inspection cards, and side-by-side A/B audit views."
                    ]
                }
            ],
            "experience": [
                {
                    "role": "Freelance Frontend Engineer & Designer",
                    "company": "mabbele.studios",
                    "period": "August 2026 – Present",
                    "bullets": [
                        "Shipped production web interfaces for client platforms across travel, real estate, and ERP including TripEva and Modern Mahal.",
                        "Authored modular React component libraries translating Figma wireframes into pixel-perfect, accessible production interfaces."
                    ]
                },
                {
                    "role": "React Developer & UI/UX Designer",
                    "company": "GEETBIH Labs Pvt. Ltd.",
                    "period": "April 2026 – October 2026",
                    "bullets": [
                        "Maintained centralized Figma component library and built scalable React/Tailwind frontend views for web and mobile platforms."
                    ]
                },
                {
                    "role": "Generative AI Developer Intern",
                    "company": "Al Wallah",
                    "period": "May 2025 – July 2025",
                    "bullets": [
                        "Integrated Google Gemini LLM workflows into client web frontends via RESTful APIs, cutting response latency with structured outputs."
                    ]
                }
            ]
        },
        "uiux": {
            "title": "Product Designer  |  UI/UX Designer  |  Design Systems & Design-to-Code",
            "summary": "Product & UI/UX Designer with hands-on frontend engineering experience (React / Tailwind CSS). Proven track record crafting complete design systems in Figma—from typography scales and color tokens to responsive component libraries. Shipped consumer products with real traction including Pandalé Kolkata (7,000+ users in 7 days) and the 2GatherApp mobile UX (live on Google Play).",
            "skills": [
                ("Design & Systems", "Figma, UI/UX Design, Wireframing, High-Fidelity Prototyping, Design Systems, Typography Scales, Color Tokens, Mobile UX"),
                ("Design-to-Code", "HTML5, CSS3, Tailwind CSS, React 19, Responsive Layouts, Developer Handoff, Design QA"),
                ("User Research & Strategy", "User Journey Mapping, Information Architecture, Usability Testing, Visual Branding, Web Analytics"),
            ],
            "projects": [
                {
                    "title": "Pandalé Kolkata: Mobile-First Consumer UX",
                    "link": "https://pandale-kolkata.vercel.app",
                    "tech": "Figma, Mobile-First UI/UX, React, Tailwind CSS",
                    "year": "2026",
                    "bullets": [
                        "Conducted rapid user research and designed intuitive mobile-first interface serving 7,000+ unique visitors in week 1.",
                        "Built comprehensive Figma component kit with interactive metro route flows, dark/light contrast badges, and bookmarking."
                    ]
                },
                {
                    "title": "2GatherApp: Mobile Social & Discovery UX",
                    "link": "https://play.google.com",
                    "tech": "Figma, Mobile Design System, Micro-interactions",
                    "year": "Live on Google Play",
                    "bullets": [
                        "Designed end-to-end mobile user experience, onboarding flows, and design system for live location-based meetup app."
                    ]
                },
                {
                    "title": "Modern Mahal & TripEva: Client Web Platforms",
                    "link": "https://joydeepdas-portfolio.vercel.app",
                    "tech": "Figma, Responsive Web, Component Tokens",
                    "year": "2026",
                    "bullets": [
                        "Crafted visual brand identity, wireframes, and scalable component systems for luxury real estate and travel client platforms."
                    ]
                }
            ],
            "experience": [
                {
                    "role": "Lead Product & UI/UX Designer",
                    "company": "mabbele.studios (Freelance)",
                    "period": "August 2026 – Present",
                    "bullets": [
                        "Direct end-to-end product design across client web applications, bridging creative wireframes with front-end React developers."
                    ]
                },
                {
                    "role": "UI/UX Designer & React Developer",
                    "company": "GEETBIH Labs Pvt. Ltd.",
                    "period": "April 2026 – October 2026",
                    "bullets": [
                        "Established design tokens, icon sets, and responsive layout standards across internal and customer-facing web platforms."
                    ]
                },
                {
                    "role": "UI/UX Designer & Growth Creative",
                    "company": "2GatherApp",
                    "period": "February 2025 – October 2025",
                    "bullets": [
                        "Delivered high-fidelity mobile prototypes and marketing creatives driving thousands of early community downloads."
                    ]
                }
            ]
        },
        "fde": {
            "title": "Forward Deployed Engineer  |  Full-Stack Developer  |  AI Systems",
            "summary": "Forward Deployed / Full-Stack Engineer specializing in modern web applications, Python/Node.js backends, and GenAI production systems. Experienced shipping 6+ production web applications, including Pandalé Kolkata (7,000+ users in 7 days) and MediRAG-Eval (Rank 62 nationally in India Innovates Hackathon). Adept at converting complex business and technical requirements into high-reliability software.",
            "skills": [
                ("Engineering", "Python (FastAPI, Flask), Node.js, Express, React 19, TypeScript, Next.js, PostgreSQL (Supabase), SQL, RESTful APIs"),
                ("AI & Automation", "LangChain, RAG, FAISS, Google Gemini API, Groq (Llama 3), Playwright Automation, Prompt Engineering, Embeddings"),
                ("DevOps & Delivery", "Docker, Git, GitHub Actions, Vercel, Hugging Face Spaces, Web Analytics, CDN Optimization, Linux"),
            ],
            "projects": [
                {
                    "title": "MediRAG-Eval: Clinical RAG Safety & Verification",
                    "link": "https://github.com/JoyTheSloth",
                    "tech": "FastAPI, BioBERT, FAISS, React 19, RAGAS",
                    "year": "India Innovates '26 (Rank 62)",
                    "bullets": [
                        "Co-engineered hybrid BioBERT + BM25 clinical retrieval pipeline over 107k-vector index with automated faithfulness scoring.",
                        "Delivered production FastAPI audit endpoints and evaluation interface for side-by-side LLM diagnostic comparisons."
                    ]
                },
                {
                    "title": "Pandalé Kolkata: High-Traffic Web Platform",
                    "link": "https://pandale-kolkata.vercel.app",
                    "tech": "React, TypeScript, Tailwind CSS, CDN Caching",
                    "year": "2026",
                    "bullets": [
                        "Engineered and scaled mobile web application handling 7,000+ unique users and 31K+ page views in 7 days without downtime."
                    ]
                },
                {
                    "title": "Researcix: Multi-Agent Research Synthesis Engine",
                    "link": "https://github.com/JoyTheSloth",
                    "tech": "Node.js, Express, React 19, Groq, arXiv API",
                    "year": "2026",
                    "bullets": [
                        "Built autonomous 4-stage agent pipeline outputting IEEE-format LaTeX research papers in under 3 minutes with live streaming."
                    ]
                }
            ],
            "experience": [
                {
                    "role": "Forward Deployed Engineer & Designer",
                    "company": "mabbele.studios (Freelance)",
                    "period": "August 2026 – Present",
                    "bullets": [
                        "Deliver full-stack web platforms and backend automation pipelines for business clients across ERP, travel, and real estate."
                    ]
                },
                {
                    "role": "Full-Stack & React Developer",
                    "company": "GEETBIH Labs Pvt. Ltd.",
                    "period": "April 2026 – October 2026",
                    "bullets": [
                        "Developed client web applications, REST API integrations, and reusable component libraries in modern React and TypeScript."
                    ]
                },
                {
                    "role": "Generative AI Developer Intern",
                    "company": "Al Wallah",
                    "period": "May 2025 – July 2025",
                    "bullets": [
                        "Built and deployed LLM-powered services with Google Gemini API, reducing hallucination via structured JSON output schemas."
                    ]
                }
            ]
        }
    },
    "education": {
        "institution": "Amity University, Kolkata",
        "degree": "B.Tech in Computer Science and Engineering",
        "period": "July 2022 – 2026",
        "cgpa": "7.25 / 10"
    },
    "honors": [
        "India Innovates 2026 National Hackathon: Rank 62 Nationally (MediRAG-Eval)",
        "OpenAI x NamasteDev Hackathon 2026: Built and shipped Stash AI clipboard vault",
        "Founder of 'Ask Joy Bhaiya': Mentorship platform for Amity University engineering students"
    ]
}

def render_html_resume(track: str = "frontend") -> str:
    data = RESUME_DATA
    track_info = data["tracks"].get(track, data["tracks"]["frontend"])

    skills_html = "".join([
        f'<div class="skill-row"><span class="skill-cat">{cat}:</span> <span class="skill-val">{val}</span></div>'
        for cat, val in track_info["skills"]
    ])

    projects_html = ""
    for proj in track_info["projects"]:
        bullets_html = "".join([f"<li>{b}</li>" for b in proj["bullets"]])
        projects_html += f"""
        <div class="item">
            <div class="item-header">
                <div>
                    <span class="item-title">{proj['title']}</span>
                    <span class="item-meta"> | {proj['tech']}</span>
                </div>
                <div class="item-date">{proj['year']}</div>
            </div>
            <ul class="bullets">
                {bullets_html}
            </ul>
        </div>
        """

    exp_html = ""
    for exp in track_info["experience"]:
        bullets_html = "".join([f"<li>{b}</li>" for b in exp["bullets"]])
        exp_html += f"""
        <div class="item">
            <div class="item-header">
                <div>
                    <span class="item-title">{exp['role']}</span>
                    <span class="item-meta"> — {exp['company']}</span>
                </div>
                <div class="item-date">{exp['period']}</div>
            </div>
            <ul class="bullets">
                {bullets_html}
            </ul>
        </div>
        """

    links_str = " &bull; ".join([
        f'<a href="{l["url"]}">{l["label"]}</a>' for l in data["links"]
    ])

    honors_html = "".join([f"<li>{h}</li>" for h in data["honors"]])

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{data['name']} - {track.upper()} Resume</title>
<style>
@page {{
    size: A4;
    margin: 0.35in 0.42in;
}}
* {{
    box-sizing: border-box;
    -webkit-print-color-adjust: exact;
}}
body {{
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    color: #0f172a;
    background: #ffffff;
    margin: 0;
    padding: 0;
    font-size: 8.8pt;
    line-height: 1.28;
}}
a {{
    color: #1d4ed8;
    text-decoration: none;
}}
.header {{
    text-align: center;
    border-bottom: 1.5px solid #0f172a;
    padding-bottom: 5px;
    margin-bottom: 7px;
}}
.name {{
    font-size: 17pt;
    font-weight: 800;
    letter-spacing: 0.8px;
    margin: 0 0 2px 0;
    color: #020617;
}}
.tagline {{
    font-size: 9pt;
    font-weight: 600;
    color: #1e3a8a;
    margin-bottom: 3px;
}}
.contact-line {{
    font-size: 8pt;
    color: #475569;
}}
.contact-line a {{
    color: #1d4ed8;
    font-weight: 500;
}}
.section-title {{
    font-size: 9.3pt;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    color: #0f172a;
    border-bottom: 1px solid #cbd5e1;
    padding-bottom: 1.5px;
    margin-top: 6.5px;
    margin-bottom: 4px;
}}
.summary-text {{
    font-size: 8.5pt;
    color: #334155;
    margin: 0 0 4px 0;
    text-align: justify;
}}
.skill-row {{
    margin-bottom: 1.5px;
    font-size: 8.4pt;
}}
.skill-cat {{
    font-weight: 700;
    color: #0f172a;
}}
.skill-val {{
    color: #334155;
}}
.item {{
    margin-bottom: 4px;
}}
.item-header {{
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    font-size: 8.8pt;
}}
.item-title {{
    font-weight: 700;
    color: #020617;
}}
.item-meta {{
    font-size: 8.2pt;
    color: #475569;
    font-style: italic;
}}
.item-date {{
    font-size: 8pt;
    font-weight: 600;
    color: #64748b;
    white-space: nowrap;
}}
.bullets {{
    margin: 1.5px 0 0 0;
    padding-left: 14px;
}}
.bullets li {{
    font-size: 8.3pt;
    color: #334155;
    margin-bottom: 1px;
}}
.edu-row {{
    display: flex;
    justify-content: space-between;
    font-size: 8.5pt;
}}
.edu-degree {{
    font-weight: 700;
    color: #020617;
}}
.edu-inst {{
    color: #475569;
}}
.edu-meta {{
    font-size: 8pt;
    font-weight: 600;
    color: #64748b;
}}
</style>
</head>
<body>

<div class="header">
    <div class="name">{data['name']}</div>
    <div class="tagline">{track_info['title']}</div>
    <div class="contact-line">
        {data['location']} &bull; {data['phone']} &bull; <a href="mailto:{data['email']}">{data['email']}</a><br>
        {links_str}
    </div>
</div>

<div class="section-title">Professional Summary</div>
<p class="summary-text">{track_info['summary']}</p>

<div class="section-title">Technical Skills &amp; Stack</div>
{skills_html}

<div class="section-title">Key Shipped Projects</div>
{projects_html}

<div class="section-title">Work Experience</div>
{exp_html}

<div class="section-title">Education</div>
<div class="edu-row">
    <div>
        <span class="edu-degree">{data['education']['degree']}</span> &mdash; 
        <span class="edu-inst">{data['education']['institution']}</span> (CGPA: {data['education']['cgpa']})
    </div>
    <div class="edu-meta">{data['education']['period']}</div>
</div>

<div class="section-title">Honors &amp; Hackathons</div>
<ul class="bullets">
    {honors_html}
</ul>

</body>
</html>
"""
    return html

def build_pdf(track: str = "frontend") -> Path:
    html_content = render_html_resume(track)
    filename_map = {
        "frontend": "Joydeep_Das_Frontend_CV.pdf",
        "uiux": "Joydeep_Das_UIUX_CV.pdf",
        "fde": "Joydeep_Das_FDE_Resume.pdf"
    }
    out_file = OUT_DIR / filename_map.get(track, "Joydeep_Das_Frontend_CV.pdf")

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.set_content(html_content, wait_until="networkidle")
        page.pdf(
            path=str(out_file),
            format="A4",
            print_background=True,
            prefer_css_page_size=True,
            margin={"top": "0.35in", "bottom": "0.35in", "left": "0.42in", "right": "0.42in"}
        )
        browser.close()

    print(f"  [✓] Generated pixel-perfect PDF ({track.upper()}): {out_file}")
    return out_file

def generate_all():
    print("Generating pixel-perfect 1-page resumes across all tracks...")
    for track in ["frontend", "uiux", "fde"]:
        build_pdf(track)
    print("All resumes successfully generated!")

if __name__ == "__main__":
    generate_all()
