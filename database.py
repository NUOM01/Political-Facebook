#!/usr/bin/env python3
"""
Local SQL Database Engine for Nepal Political Campaign Intelligence
Provides 100% complete isolation from Supabase and any cloud service.
Runs entirely on your local machine using standard SQL.

Features:
1. Native local SQL storage (SQLite3 / MySQL compatible schema).
2. Zero external network calls or cloud database dependencies.
3. Tables for:
   - political_ads: Scraped Meta Ad Library payloads, spend ranges, demographics
   - surveys: Voter sentiment questionnaire definitions
   - survey_responses: Electorate poll answers and regional demographic data
   - media_queue: Creative generation pipeline status and scheduled Facebook posts
"""

import sqlite3
import json
import os
from pathlib import Path
from typing import List, Dict, Any, Optional

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "data" / "campaign.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

class LocalSQLDatabase:
    def __init__(self, db_path: Path = DB_PATH):
        self.db_path = db_path
        self.init_schema()

    def get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_schema(self):
        """Creates the relational SQL tables locally."""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            # 1. Scraped Political Ads
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS political_ads (
                id TEXT PRIMARY KEY,
                page_name TEXT NOT NULL,
                page_id TEXT,
                ad_body TEXT,
                media_url TEXT,
                spend_range TEXT,
                impressions_range TEXT,
                demographics_json TEXT,
                regions_json TEXT,
                scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """)

            # 2. Voter Opinion Surveys
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS surveys (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                questions_json TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """)

            # 3. Survey Responses
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS survey_responses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                survey_id TEXT NOT NULL,
                voter_region TEXT,
                voter_age_group TEXT,
                answers_json TEXT NOT NULL,
                submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (survey_id) REFERENCES surveys(id)
            );
            """)

            # 4. Multi-Agent Media & Publishing Queue
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS media_queue (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                media_type TEXT CHECK(media_type IN ('image', 'carousel', 'video')),
                title TEXT,
                caption TEXT,
                file_path TEXT NOT NULL,
                status TEXT DEFAULT 'pending' CHECK(status IN ('pending', 'rendering', 'ready', 'published')),
                target_page_id TEXT,
                published_post_id TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """)
            conn.commit()

    # ─── Ads CRUD ─────────────────────────────────────────────────────────────

    def upsert_ad(self, ad_data: Dict[str, Any]) -> str:
        ad_id = str(ad_data.get("id") or ad_data.get("card_index") or hash(ad_data.get("raw_text", "")))
        page_name = ad_data.get("page_name") or ad_data.get("query") or "Unknown"
        body = ad_data.get("raw_text") or " ".join(ad_data.get("ad_creative_bodies") or [])
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT OR REPLACE INTO political_ads 
            (id, page_name, page_id, ad_body, media_url, spend_range, impressions_range, demographics_json, regions_json)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                ad_id,
                page_name,
                ad_data.get("page_id", ""),
                body,
                ad_data.get("ad_snapshot_url", ""),
                str(ad_data.get("spend", "")),
                str(ad_data.get("impressions", "")),
                json.dumps(ad_data.get("demographic_distribution", [])),
                json.dumps(ad_data.get("region_distribution", []))
            ))
            conn.commit()
        return ad_id

    def list_ads(self, limit: int = 50) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM political_ads ORDER BY scraped_at DESC LIMIT ?", (limit,))
            return [dict(row) for row in cursor.fetchall()]

    # ─── Surveys CRUD ─────────────────────────────────────────────────────────

    def save_survey(self, survey_id: str, title: str, questions: list):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT OR REPLACE INTO surveys (id, title, questions_json)
            VALUES (?, ?, ?)
            """, (survey_id, title, json.dumps(questions)))
            conn.commit()

    def record_survey_response(self, survey_id: str, region: str, age_group: str, answers: Dict[str, Any]):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO survey_responses (survey_id, voter_region, voter_age_group, answers_json)
            VALUES (?, ?, ?, ?)
            """, (survey_id, region, age_group, json.dumps(answers)))
            conn.commit()

    # ─── Media Queue CRUD ─────────────────────────────────────────────────────

    def enqueue_media(self, media_type: str, title: str, caption: str, file_path: str, target_page_id: str = "") -> int:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO media_queue (media_type, title, caption, file_path, status, target_page_id)
            VALUES (?, ?, ?, ?, 'ready', ?)
            """, (media_type, title, caption, str(file_path), target_page_id))
            conn.commit()
            return cursor.lastrowid

    def get_pending_media(self) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM media_queue WHERE status = 'ready' ORDER BY created_at ASC")
            return [dict(row) for row in cursor.fetchall()]

if __name__ == "__main__":
    db = LocalSQLDatabase()
    print(f"[SQL Setup] Database online and 100% isolated at: {db.db_path}")
