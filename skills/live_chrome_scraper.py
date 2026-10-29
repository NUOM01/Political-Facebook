#!/usr/bin/env python3
"""
Live Chrome Web Scraper for Facebook Campaign Intelligence
Connects to the user's active, authenticated Chrome browser session via CDP (port 9222).
Scrapes Meta Ad Library, RSP Official Page, and Rabi Lamichhane Page.
Saves all data directly into the local isolated SQL database.

Author: Aaditya Sah (useraadityaid@gmail.com)
"""

import os
import sys
import json
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))
from database import LocalSQLDatabase

DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

def scrape_meta_ad_library(page, query="Rastriya Swatantra Party", country="NP"):
    """Scrapes political ads from Meta Ad Library in Nepal using live Chrome."""
    encoded_q = query.replace(" ", "%20")
    url = f"https://www.facebook.com/ads/library/?active_status=all&ad_type=political_and_issue_ads&country={country}&q={encoded_q}"
    print(f"[Chrome Scraper] Navigating to Meta Ad Library: {url}")
    page.goto(url, wait_until="domcontentloaded")
    page.wait_for_timeout(5000)

    # Scroll down to trigger lazy-load
    for _ in range(3):
        page.mouse.wheel(0, 1500)
        page.wait_for_timeout(2000)

    # Extract all text blocks and ad cards
    cards = page.query_selector_all("div[class*='_99s5'], div[role='article'], div:has(> span:has-text('Started running'))")
    print(f"[Chrome Scraper] Found {len(cards)} ad card containers in live Chrome.")

    extracted_ads = []
    db = LocalSQLDatabase()

    if not cards:
        # Fallback to broader text extraction
        body_text = page.inner_text("body")
        extracted_ads.append({
            "id": f"ad_lib_summary_{int(time.time())}",
            "page_name": "Meta Ad Library Overview",
            "page_id": "meta_ads_nepal",
            "raw_text": body_text[:2000],
            "query": query,
            "country": country,
            "scraped_at": time.strftime("%Y-%m-%d %H:%M:%S")
        })
    else:
        for idx, card in enumerate(cards[:15]):
            raw_text = card.inner_text().strip()
            if raw_text and len(raw_text) > 30:
                ad_item = {
                    "id": f"ad_live_{int(time.time())}_{idx}",
                    "page_name": query,
                    "page_id": "rsp_ad",
                    "raw_text": raw_text,
                    "query": query,
                    "country": country,
                    "scraped_at": time.strftime("%Y-%m-%d %H:%M:%S")
                }
                extracted_ads.append(ad_item)
                db.upsert_ad(ad_item)

    print(f"[Chrome Scraper] Extracted and stored {len(extracted_ads)} ads in local SQL.")
    return extracted_ads

def scrape_facebook_page_feed(page, page_url, page_label):
    """Scrapes recent public posts and messaging from a Facebook page."""
    print(f"[Chrome Scraper] Navigating to Facebook Page: {page_url}")
    page.goto(page_url, wait_until="domcontentloaded")
    page.wait_for_timeout(5000)

    # Scroll to load feed
    for _ in range(3):
        page.mouse.wheel(0, 1200)
        page.wait_for_timeout(2000)

    # Extract post containers
    posts = page.query_selector_all("div[role='article'], div[data-ad-preview='message'], div[class*='userContent']")
    if not posts:
        # Fallback to text blocks
        posts = page.query_selector_all("div[dir='auto']")
    print(f"[Chrome Scraper] Found {len(posts)} post elements on {page_label}.")

    extracted_posts = []
    db = LocalSQLDatabase()

    for idx, p in enumerate(posts[:10]):
        text = p.inner_text().strip()
        if text and len(text) > 40:
            item = {
                "id": f"fb_{page_label}_{int(time.time())}_{idx}",
                "page_name": page_label,
                "page_id": page_url.split("/")[-1],
                "raw_text": text,
                "scraped_at": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            extracted_posts.append(item)
            db.upsert_ad(item)

    print(f"[Chrome Scraper] Saved {len(extracted_posts)} posts for {page_label} in local SQL.")
    return extracted_posts

def main():
    print("=" * 65)
    print("LIVE CHROME RAPID SCRAPER — NEPAL CAMPAIGN INTELLIGENCE")
    print("=" * 65)

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://localhost:9222")
        ctx = browser.contexts[0]
        tab = ctx.new_page()

        # 1. Scrape Meta Ad Library for RSP political ads in Nepal
        print("\n--- [Step 1: Meta Ad Library Scraping] ---")
        ad_results = scrape_meta_ad_library(tab, query="Rastriya Swatantra Party", country="NP")

        # 2. Scrape RSP Official Page
        print("\n--- [Step 2: RSP Official Facebook Page] ---")
        rsp_posts = scrape_facebook_page_feed(tab, "https://www.facebook.com/rspsnepal", "RSP_Official")

        # 3. Scrape Rabi Lamichhane Page
        print("\n--- [Step 3: Rabi Lamichhane Facebook Page] ---")
        rabi_posts = scrape_facebook_page_feed(tab, "https://www.facebook.com/lamichhanerabi", "Rabi_Lamichhane")

        tab.close()

    print("\n[Complete] Live scraping finished successfully and all records persisted to local SQL!")

if __name__ == "__main__":
    main()
