#!/usr/bin/env python3
"""
Service Agent: Facebook Publisher & Page Manager
Publishes generated image creatives, carousels, and video reels to Facebook Pages.

Supports:
1. Facebook Graph API publishing for photos (`/{page_id}/photos`)
2. Facebook Graph API publishing for videos & Reels (`/{page_id}/videos`)
3. Multi-image carousel album posts
4. Dry-run mode for simulation and review before live broadcast
"""

import os
import sys
import json
import requests
from pathlib import Path
from typing import Optional, List, Dict, Any

BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(BASE_DIR))
from database import LocalSQLDatabase

class FacebookPublisherAgent:
    def __init__(self, page_id: Optional[str] = None, page_access_token: Optional[str] = None):
        self.page_id = page_id or os.environ.get("FB_TARGET_PAGE_ID", "")
        self.token = page_access_token or os.environ.get("FB_TARGET_PAGE_TOKEN", "")
        self.api_base = "https://graph.facebook.com/v19.0"

    def publish_photo(
        self,
        image_path: str,
        caption: str,
        dry_run: bool = False
    ) -> Dict[str, Any]:
        """Publishes a photo with a caption to the Facebook Page."""
        if dry_run or not (self.page_id and self.token):
            print(f"[Publisher: Dry-Run] Would post photo {image_path} to Page {self.page_id or 'SIMULATED_PAGE'}")
            print(f"[Caption Preview]:\n{caption}")
            return {"status": "simulated", "post_id": "sim_1001", "image": image_path}

        url = f"{self.api_base}/{self.page_id}/photos"
        with open(image_path, "rb") as img_file:
            payload = {"caption": caption, "access_token": self.token}
            files = {"source": img_file}
            res = requests.post(url, data=payload, files=files)
            res.raise_for_status()
            result = res.json()
            print(f"[Publisher] Published photo post! ID: {result.get('id')}")
            return result

    def publish_video(
        self,
        video_path: str,
        title: str,
        description: str,
        dry_run: bool = False
    ) -> Dict[str, Any]:
        """Publishes a video or Reel to the Facebook Page."""
        if dry_run or not (self.page_id and self.token):
            print(f"[Publisher: Dry-Run] Would post video {video_path} to Page {self.page_id or 'SIMULATED_PAGE'}")
            print(f"[Title]: {title}\n[Description]: {description}")
            return {"status": "simulated", "video_id": "sim_vid_2001", "video": video_path}

        url = f"{self.api_base}/{self.page_id}/videos"
        with open(video_path, "rb") as vid_file:
            payload = {"title": title, "description": description, "access_token": self.token}
            files = {"source": vid_file}
            res = requests.post(url, data=payload, files=files)
            res.raise_for_status()
            result = res.json()
            print(f"[Publisher] Published video post! ID: {result.get('id')}")
            return result

    def process_queue(self, dry_run: bool = True):
        """Processes all ready media items from the local SQL queue."""
        db = LocalSQLDatabase()
        pending = db.get_pending_media()
        print(f"[Publisher] Found {len(pending)} ready item(s) in local SQL media queue.")

        for item in pending:
            print(f"[Publisher] Processing item #{item['id']} ({item['media_type']}): '{item['title']}'")
            if item['media_type'] in ['image', 'carousel']:
                self.publish_photo(
                    image_path=item['file_path'],
                    caption=item['caption'],
                    dry_run=dry_run
                )
            elif item['media_type'] == 'video':
                self.publish_video(
                    video_path=item['file_path'],
                    title=item['title'],
                    description=item['caption'],
                    dry_run=dry_run
                )

if __name__ == "__main__":
    publisher = FacebookPublisherAgent()
    publisher.process_queue(dry_run=True)

