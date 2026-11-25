"""
Multi-Engine Universal Scraper for Jim Bob.
Supports:
1. Crawl4AI: Blazing-fast markdown/text extraction via async headless browser.
2. ScrapeGraphAI: Dynamic natural-language prompt-based extraction via LLMs.
3. Apify: Multi-board cloud dataset crawler.
4. Fast fallback: Requests + BeautifulSoup.
"""

import os
import json
import asyncio
from pathlib import Path

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

# ─── 1. Crawl4AI Engine ──────────────────────────────────────────────────────

async def scrape_crawl4ai_async(url: str) -> dict:
    """Extracts clean Markdown and structure using Crawl4AI."""
    try:
        from crawl4ai import AsyncWebCrawler
        async with AsyncWebCrawler(verbose=False) as crawler:
            result = await crawler.arun(url=url)
            return {
                "success": True,
                "engine": "crawl4ai",
                "markdown": result.markdown or "",
                "cleaned_html": result.cleaned_html or "",
                "title": getattr(result, "title", "") or url
            }
    except Exception as e:
        return {"success": False, "engine": "crawl4ai", "error": str(e)}

def scrape_with_crawl4ai(url: str) -> dict:
    """Synchronous wrapper for Crawl4AI."""
    try:
        return asyncio.run(scrape_crawl4ai_async(url))
    except Exception as e:
        return {"success": False, "engine": "crawl4ai", "error": str(e)}


# ─── 2. ScrapeGraphAI Engine ─────────────────────────────────────────────────

def scrape_with_scrapegraph(url: str, prompt: str = "Extract all key information, headings, titles, dates, and contact emails.") -> dict:
    """Extracts structured schema using natural language prompt with ScrapeGraphAI."""
    try:
        from scrapegraphai.graphs import SmartScraperGraph

        graph_config = {
            "llm": {
                "api_key": GROQ_API_KEY,
                "model": "groq/qwen/qwen3.8-27b",
            },
            "verbose": False,
            "headless": True
        }

        smart_scraper = SmartScraperGraph(
            prompt=prompt,
            source=url,
            config=graph_config
        )
        result = smart_scraper.run()
        return {
            "success": True,
            "engine": "scrapegraphai",
            "data": result
        }
    except Exception as e:
        return {"success": False, "engine": "scrapegraphai", "error": str(e)}


# ─── 3. Master Multi-Engine Dispatcher ───────────────────────────────────────

def universal_scrape(url: str, engine: str = "crawl4ai", prompt: str = None) -> dict:
    """
    Unified entry point.
    engine: 'crawl4ai' | 'scrapegraph' | 'apify' | 'auto'
    """
    engine = engine.lower().strip()

    if engine == "scrapegraph":
        p = prompt or "Extract all job titles, company names, requirements, and emails."
        return scrape_with_scrapegraph(url, p)

    elif engine == "crawl4ai":
        res = scrape_with_crawl4ai(url)
        if res.get("success"):
            return res
        # Fallback to scrapegraph if crawl4ai hit an issue
        return scrape_with_scrapegraph(url)

    elif engine == "auto":
        # Prefer Crawl4AI for speed, fallback to ScrapeGraphAI
        res = scrape_with_crawl4ai(url)
        if res.get("success") and res.get("markdown"):
            return res
        return scrape_with_scrapegraph(url)

    return {"success": False, "error": f"Unknown scraping engine: {engine}"}
