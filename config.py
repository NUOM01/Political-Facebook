#!/usr/bin/env python3
"""
Configuration for Nepal Campaign Intelligence & Social Agentic OS
Author: Aaditya Sah (useraadityaid@gmail.com)
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

# Meta / Facebook App Credentials
FB_APP_ID = "2261494131297653"
FB_APP_SECRET = "72df483fc24fbd902dbecadabdd5687e"
FB_APP_TOKEN = f"{FB_APP_ID}|{FB_APP_SECRET}"
FB_APP_NAME = "Campaign Media OS"
FB_GRAPH_API_VERSION = "v26.0"

# Target Pages for Analysis & Publishing
REFERENCE_PAGES = {
    "rsp_official": {
        "name": "Rastriya Swatantra Party - Official",
        "url": "https://www.facebook.com/rspsnepal",
        "category": "Political Party"
    },
    "rabi_lamichhane": {
        "name": "Rabi Lamichhane",
        "url": "https://www.facebook.com/lamichhanerabi",
        "category": "Candidate / Party President"
    }
}

# Access Token (loads User/Page Token if provided, else falls back to App Token)
FB_ACCESS_TOKEN = os.environ.get("FB_ACCESS_TOKEN", FB_APP_TOKEN)
