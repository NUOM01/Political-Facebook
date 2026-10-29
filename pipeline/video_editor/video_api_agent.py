#!/usr/bin/env python3
"""
API Video Director Sub-Agent for Nepal Campaign Intelligence OS
Connects to Cloud Video Editing APIs (Creatomate, Shotstack) or local engine
to assemble high-energy 9:16 vertical Facebook Reels with dynamic typography,
voiceover sync, and candidate branding.

Author: Aaditya Sah (useraadityaid@gmail.com)
"""

import os
import sys
import json
import urllib.request
import urllib.error
from pathlib import Path
from typing import Dict, Any, List, Optional

BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(BASE_DIR))

from database import LocalSQLDatabase

OUTPUT_DIR = BASE_DIR / "data" / "generated_videos"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


class ApiVideoDirectorAgent:
    """
    Sub-agent that programmatically generates vertical Reels (1080x1920)
    using video editing APIs or local manifests.
    """

    def __init__(self, db: Optional[LocalSQLDatabase] = None):
        self.db = db or LocalSQLDatabase()
        self.creatomate_api_key = os.environ.get("CREATOMATE_API_KEY", "")
        self.shotstack_api_key = os.environ.get("SHOTSTACK_API_KEY", "")

    def build_reel_storyboard(
        self,
        title: str,
        hook_text: str,
        stat_highlight: str,
        solution_points: List[str],
        call_to_action: str
    ) -> Dict[str, Any]:
        """
        Builds a structured timeline storyboard for a 15-30 second viral political Reel.
        Format: 1080x1920 (9:16 Aspect Ratio).
        """
        scenes = [
            {
                "scene_id": "scene_01_hook",
                "duration_seconds": 3.5,
                "layout": "full_screen_video",
                "caption_text": hook_text,
                "text_animation": "kinetic_pop",
                "accent_color": "#FFB800", # Gold accent
                "sound_effect": "whoosh_impact"
            },
            {
                "scene_id": "scene_02_data_impact",
                "duration_seconds": 4.5,
                "layout": "stat_card_overlay",
                "caption_text": f"तथ्यांक: {stat_highlight}",
                "text_animation": "counter_slide_up",
                "accent_color": "#0080FF", # RSP Electric Blue
                "sound_effect": "subtle_glitch"
            },
            {
                "scene_id": "scene_03_solution",
                "duration_seconds": 6.0,
                "layout": "split_screen_action",
                "bullet_points": solution_points,
                "caption_text": "हाम्रो स्पष्ट कार्ययोजना र संकल्प",
                "text_animation": "typewriter",
                "accent_color": "#FFFFFF"
            },
            {
                "scene_id": "scene_04_cta",
                "duration_seconds": 4.0,
                "layout": "branded_end_card",
                "caption_text": call_to_action,
                "symbol": "Bell / घण्टी",
                "text_animation": "scale_in_bounce",
                "accent_color": "#FFB800"
            }
        ]

        total_duration = sum(s["duration_seconds"] for s in scenes)

        return {
            "title": title,
            "dimensions": {"width": 1080, "height": 1920, "aspect_ratio": "9:16"},
            "total_duration_seconds": total_duration,
            "scenes": scenes,
            "audio_track": {
                "genre": "Inspiring Cinematic Drums & Strings",
                "volume": 0.35,
                "duck_on_speech": True
            }
        }

    def render_via_creatomate(self, storyboard: Dict[str, Any], template_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Renders video using Creatomate REST API (https://creatomate.com/docs/api).
        """
        if not self.creatomate_api_key:
            return {
                "status": "skipped",
                "message": "CREATOMATE_API_KEY environment variable not set. Saved storyboard manifest locally."
            }

        url = "https://api.creatomate.com/v1/renders"
        headers = {
            "Authorization": f"Bearer {self.creatomate_api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "template_id": template_id or "default_nepal_campaign_reel",
            "modifications": {
                "Headline.text": storyboard["scenes"][0]["caption_text"],
                "Stat.text": storyboard["scenes"][1]["caption_text"],
                "CTA.text": storyboard["scenes"][3]["caption_text"]
            }
        }

        req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers, method="POST")
        try:
            with urllib.request.urlopen(req) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                return {"status": "success", "render_data": data}
        except Exception as e:
            return {"status": "error", "error": str(e)}

    def save_and_enqueue_reel(self, storyboard: Dict[str, Any]) -> Path:
        """Saves project manifest and enqueues video for rendering/publishing."""
        safe_title = "".join(c if c.isalnum() or c in ("-", "_") else "_" for c in storyboard["title"].lower())
        manifest_path = OUTPUT_DIR / f"{safe_title}.manifest.json"
        
        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(storyboard, f, indent=2, ensure_ascii=False)

        # Enqueue in database
        video_target_path = str(OUTPUT_DIR / f"{safe_title}.mp4")
        self.db.enqueue_media(
            media_type="video",
            title=storyboard["title"],
            caption=storyboard["scenes"][0]["caption_text"] + "\n\n" + storyboard["scenes"][3]["caption_text"],
            file_path=video_target_path
        )

        return manifest_path


if __name__ == "__main__":
    print("=" * 70)
    print("🎬 Testing API Video Director Sub-Agent")
    print("=" * 70)

    director = ApiVideoDirectorAgent()
    storyboard = director.build_reel_storyboard(
        title="Nepal Youth Employment Reel",
        hook_text="दैनिक हजारौं युवा किन देश छाड्न बाध्य छन्?",
        stat_highlight="७४% युवा देशमै काम गर्न इच्छुक",
        solution_points=[
            "स्वदेशी उद्योगलाई कर छुट",
            "डिजिटल सुशासन र स्टार्टअप प्रवर्द्धन",
            "रेमिट्यान्सलाई उत्पादनमा जोड्ने नीति"
        ],
        call_to_action="घण्टी बजिसकेको छ—परिवर्तनको पक्षमा उभिनुहोस्!"
    )

    manifest_file = director.save_and_enqueue_reel(storyboard)
    print(f"✅ Generated 9:16 Video Storyboard: {manifest_file.name}")
    print(f"⏱️ Total Video Duration: {storyboard['total_duration_seconds']}s")
    print(f"📝 Scene 1 Hook: {storyboard['scenes'][0]['caption_text']}")
    print(f"📦 Successfully enqueued video Reel into local database media_queue!")
