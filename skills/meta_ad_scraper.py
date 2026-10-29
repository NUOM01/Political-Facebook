#!/usr/bin/env python3
"""
Meta Ad Library & Facebook Campaign Scraper
Designed for analyzing Political Ads in Nepal (e.g., Rastriya Swatantra Party / RSP).

Features:
1. Meta Ad Archive Graph API integration (Official API mode).
2. Playwright-powered headless scraper for public Ad Library queries without tokens.
3. Automated ETL into structured JSON and tabular CSV.
4. Demographic & geographic impression analysis (Bagmati, Gandaki, Koshi, etc.).
"""

import os
import sys
import json
import time
import argparse
from pathlib import Path
from typing import Dict, List, Any, Optional

import requests

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

sys.path.insert(0, str(BASE_DIR))
from database import LocalSQLDatabase

class MetaAdLibraryScraper:
    def __init__(self, access_token: Optional[str] = None):
        self.access_token = access_token or os.environ.get("FB_ACCESS_TOKEN", "")
        self.api_version = "v19.0"
        self.api_base = f"https://graph.facebook.com/{self.api_version}/ads_archive"

    def fetch_via_api(
        self,
        search_terms: str,
        country: str = "NP",
        ad_type: str = "POLITICAL_AND_ISSUE_ADS",
        limit: int = 50,
        page_ids: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """Queries the official Meta Ad Library API for political & issue ads in Nepal."""
        if not self.access_token:
            print("[Warning] No FB_ACCESS_TOKEN found. Cannot query official Graph API.")
            return []

        fields = [
            "id", "ad_creation_time", "ad_creative_bodies",
            "ad_creative_link_captions", "ad_creative_link_descriptions",
            "ad_creative_link_titles", "ad_delivery_start_time",
            "ad_delivery_stop_time", "ad_snapshot_url", "currency",
            "demographic_distribution", "bylines", "publisher_platforms",
            "region_distribution", "spend", "impressions", "page_id", "page_name"
        ]

        params = {
            "access_token": self.access_token,
            "ad_reached_countries": f"['{country}']",
            "ad_type": ad_type,
            "search_terms": search_terms,
            "fields": ",".join(fields),
            "limit": str(limit)
        }

        if page_ids:
            params["search_page_ids"] = ",".join(page_ids)

        print(f"[API] Querying Meta Ad Library for '{search_terms}' in country '{country}'...")
        all_ads = []
        url = self.api_base

        while url and len(all_ads) < limit:
            try:
                res = requests.get(url, params=params if url == self.api_base else None)
                res.raise_for_status()
                data = res.json()
                ads = data.get("data", [])
                all_ads.extend(ads)
                print(f"[API] Retrieved {len(ads)} ads (Total: {len(all_ads)})")

                paging = data.get("paging", {})
                url = paging.get("next")
                params = None  # Next URL already includes parameters
                if not ads:
                    break
            except Exception as e:
                print(f"[API Error] Failed to fetch: {e}")
                break

        return all_ads

    def scrape_via_playwright(
        self,
        query: str,
        country: str = "NP",
        max_ads: int = 30
    ) -> List[Dict[str, Any]]:
        """Uses headless Playwright to scrape public Meta Ad Library search results."""
        from playwright.sync_api import sync_playwright

        encoded_q = requests.utils.quote(query)
        ad_lib_url = (
            f"https://www.facebook.com/ads/library/?"
            f"active_status=all&ad_type=political_and_issue_ads&country={country}&q={encoded_q}&sort_data[direction]=desc&sort_data[mode]=relevancy_monthly_grouped"
        )

        print(f"[Playwright] Navigating to public Ad Library: {ad_lib_url}")
        results = []

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
            page = context.new_page()

            try:
                page.goto(ad_lib_url, timeout=45000, wait_until="domcontentloaded")
                time.sleep(4)

                # Scroll down to load ad cards
                for _ in range(4):
                    page.mouse.wheel(0, 1500)
                    time.sleep(2)

                # Extract ad cards
                cards = page.query_selector_all("div[class*='_99s5'], div[role='article']")
                print(f"[Playwright] Found {len(cards)} potential ad cards on page.")

                for idx, card in enumerate(cards[:max_ads]):
                    text = card.inner_text()
                    results.append({
                        "card_index": idx + 1,
                        "raw_text": text,
                        "query": query,
                        "country": country,
                        "scraped_at": time.strftime("%Y-%m-%d %H:%M:%S")
                    })
            except Exception as e:
                print(f"[Playwright Error] Scrape failed: {e}")
            finally:
                browser.close()

        return results

    def save_results(self, data: List[Dict[str, Any]], filename: str):
        filepath = DATA_DIR / filename
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"[Storage] Saved {len(data)} items to JSON: {filepath}")

        # Persist to isolated local SQL database
        db = LocalSQLDatabase()
        saved_count = 0
        for item in data:
            db.upsert_ad(item)
            saved_count += 1
        print(f"[SQL Storage] Upserted {saved_count} ads into local SQL database (data/campaign.db)")

def main():
    parser = argparse.ArgumentParser(description="Scrape Meta Ad Library for Political Ads in Nepal")
    parser.add_argument("--query", type=str, default="Rastriya Swatantra Party", help="Search query or party name")
    parser.add_argument("--method", choices=["api", "playwright"], default="api", help="Scraping method")
    parser.add_argument("--limit", type=int, default=25, help="Number of ads to retrieve")
    parser.add_argument("--out", type=str, default="nepal_political_ads.json", help="Output filename")

    args = parser.parse_args()

    scraper = MetaAdLibraryScraper()
    if args.method == "api":
        data = scraper.fetch_via_api(search_terms=args.query, limit=args.limit)
        if not data:
            print("[Fallback] No API results or token not set. Running Playwright fallback...")
            data = scraper.scrape_via_playwright(query=args.query, max_ads=args.limit)
    else:
        data = scraper.scrape_via_playwright(query=args.query, max_ads=args.limit)

    scraper.save_results(data, args.out)

if __name__ == "__main__":
    main()

