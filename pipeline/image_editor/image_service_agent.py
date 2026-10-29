#!/usr/bin/env python3
"""
Service Agent: Image Creative & Carousel Editor
Produces political campaign visual assets, infographic quote cards, and multi-image carousels.

Workflow:
1. Receives campaign brief or survey insight.
2. Selects or generates background scene / candidate image.
3. Overlays branding, high-contrast typography, and key political pledges.
4. Outputs web-optimized JPG/PNG for Facebook feed and carousel formats.
"""

import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = Path(__file__).resolve().parent.parent.parent
OUTPUT_DIR = BASE_DIR / "data" / "generated_images"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

class ImageServiceAgent:
    def __init__(self, brand_color=(12, 84, 180)): # RSP Blue / Primary Brand
        self.brand_color = brand_color

    def create_campaign_stat_card(
        self,
        headline: str,
        stat_number: str,
        subtext: str,
        output_filename: str = "stat_card.png"
    ) -> Path:
        """Generates a high-contrast social media stat card for Facebook feeds."""
        width, height = 1080, 1080 # Standard Facebook 1:1 post
        img = Image.new("RGB", (width, height), color=(248, 249, 250))
        draw = ImageDraw.Draw(img)

        # Header banner
        draw.rectangle([0, 0, width, 160], fill=self.brand_color)

        # Text rendering (using default or basic PIL font)
        # Banner Title
        draw.text((60, 60), headline, fill=(255, 255, 255))

        # Main Stat / Callout
        draw.rectangle([60, 240, width - 60, 680], outline=self.brand_color, width=4)
        draw.text((120, 360), stat_number, fill=self.brand_color)
        draw.text((120, 520), subtext, fill=(40, 40, 40))

        # Footer call to action
        draw.rectangle([0, height - 120, width, height], fill=(230, 235, 245))
        draw.text((60, height - 80), "Nepal Political Campaign Intelligence | Public Insight", fill=(80, 80, 80))

        out_path = OUTPUT_DIR / output_filename
        img.save(out_path)
        print(f"[Image Agent] Generated creative: {out_path}")
        return out_path

if __name__ == "__main__":
    agent = ImageServiceAgent()
    agent.create_campaign_stat_card(
        headline="PUBLIC OPINION & SURVEY REPORT",
        stat_number="78% VOTER SHIFT",
        subtext="Urban voters prioritize anti-corruption & digital public services."
    )

