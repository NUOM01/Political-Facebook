#!/usr/bin/env python3
"""
Local SQLite Database Engine for Nepal Political Campaign Intelligence
100% private, zero-cloud dependency, runs locally on your machine.
Author: Aaditya Sah (useraadityaid@gmail.com)
"""

import sqlite3
import json
from pathlib import Path
from typing import List, Dict, Any, Optional

DB_PATH = Path(__file__).resolve().parent / "data" / "campaign.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes local tables for ad intelligence, surveys, and the agent publishing queue."""
    conn = get_connection()
    cursor = conn.cursor()

    # 1. Scraped Political Ads Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS political_ads (
        id TEXT PRIMARY KEY,
        page_name TEXT,
        page_id TEXT,
        ad_body TEXT,
        media_url TEXT,
        spend_range TEXT,
        impressions_range TEXT,
        demographics TEXT,
        regions TEXT,
        scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # 2. Voter Opinion Surveys Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS surveys (
        id TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        questions_json TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # 3. Survey Responses Table
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

    # 4. Multi-Agent Media & Publishing Queue Table
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
    conn.close()
    print(f"[Database] Local SQLite initialized at {DB_PATH}")

if __name__ == "__main__":
    init_db()
