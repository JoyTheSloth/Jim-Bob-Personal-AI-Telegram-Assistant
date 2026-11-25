"""Apify-powered HR & Talent Outreach runner.

Uses APIFY_API_TOKEN from environment to run an Apify actor/dataset
and return HR leads for Telegram outreach.
"""
import os
import json
import urllib.request

def fetch_apify_hr_leads(limit: int = 10) -> list[dict]:
    token = os.getenv("APIFY_API_TOKEN")
    dataset_id = os.getenv("APIFY_HR_DATASET_ID")
    if not token or not dataset_id:
        return []
    url = f"https://api.apify.com/v2/datasets/{dataset_id}/items?token={token}&limit={limit}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode("utf-8"))
