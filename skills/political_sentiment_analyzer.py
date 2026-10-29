#!/usr/bin/env python3
"""
Political Sentiment & Campaign Strategy Analyzer
Analyzes political advertisements and Facebook posts in Nepal (e.g., RSP, Rabi Lamichhane).

Key Capabilities:
1. Message Framing Analysis (Anti-corruption, Good Governance, Youth/Diaspora, Economy).
2. Sentiment & Emotional Appeals (Hope, Frustration, Urgency, Pride).
3. Demographic Targeting Inferences.
4. Gemini-powered qualitative analysis + Heuristic NLP fallback.
"""

import os
import sys
import json
import re
from pathlib import Path
from typing import Dict, List, Any

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

# Common Political Campaign Themes in Nepal (especially for RSP and new parties)
CORE_THEMES = {
    "Anti-Corruption & Systemic Reform": ["corruption", "bhrastachar", "ghanti", "system change", "old parties", "shasan", "niti", "accountability"],
    "Youth & Foreign Employment": ["youth", "bidesh", "employment", "rojgari", "remittance", "brain drain", "yuwa"],
    "Public Services & Healthcare": ["swasthya", "hospital", "sikshya", "school", "education", "infrastructure", "sadak"],
    "Judicial & Electoral Integrity": ["court", "adalat", "chunab", "election commission", "voting", "direct election"],
    "Economic & Entrepreneurship": ["armathantra", "tax", "startup", "industry", "udyog", "business"]
}

class CampaignAnalyzer:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY", "")

    def heuristic_theme_tagging(self, text: str) -> Dict[str, Any]:
        """Categorizes text based on keyword prevalence in Nepali and English."""
        text_lower = text.lower()
        matched_themes = {}
        for theme, keywords in CORE_THEMES.items():
            matches = [kw for kw in keywords if kw in text_lower]
            if matches:
                matched_themes[theme] = matches

        # Basic sentiment heuristic
        urgency_terms = ["urgent", "aaja nai", "now", "time for change", "parivartan", "badlav"]
        hope_terms = ["future", "bhavishya", "hope", "nawa", "vision", "samriddha"]
        critique_terms = ["fail", "loot", "dhoka", "purana", "lootera"]

        return {
            "themes": matched_themes,
            "has_urgency": any(t in text_lower for t in urgency_terms),
            "has_hope": any(t in text_lower for t in hope_terms),
            "critique_level": sum(1 for t in critique_terms if t in text_lower)
        }

    def analyze_ad_corpus(self, ads_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Processes a corpus of scraped ads and generates an aggregate intelligence breakdown."""
        total_ads = len(ads_data)
        theme_counts = {theme: 0 for theme in CORE_THEMES}
        page_counts = {}

        for ad in ads_data:
            text = ""
            if "raw_text" in ad:
                text = ad["raw_text"]
            elif "ad_creative_bodies" in ad:
                text = " ".join(ad.get("ad_creative_bodies") or [])

            tag_res = self.heuristic_theme_tagging(text)
            for theme in tag_res["themes"]:
                theme_counts[theme] += 1

            p_name = ad.get("page_name") or "Unknown Page"
            page_counts[p_name] = page_counts.get(p_name, 0) + 1

        return {
            "total_analyzed": total_ads,
            "theme_distribution": theme_counts,
            "page_distribution": page_counts,
            "analysis_timestamp": str(Path(__file__).stat().st_mtime)
        }

if __name__ == "__main__":
    analyzer = CampaignAnalyzer()
    print("[Analyzer] Political Campaign Analyzer loaded successfully.")

