# 🇳🇵 Nepal Campaign Intelligence & Social Agentic OS

An end-to-end autonomous multi-agent intelligence and media operations platform designed to analyze, produce, benchmark, and deploy high-converting political advertisements, voter sentiment surveys, and multimedia campaigns across Nepal on Meta (Facebook & Instagram) platforms.

---

## 🔒 Security, Privacy & Repository Isolation
- **Private Repository:** Hosted exclusively under personal account [`NUOM01/Political-Facebook`](https://github.com/NUOM01/Political-Facebook).
- **Zero Cloud Leakage:** 100% offline local SQL storage (`data/campaign.db`).
- **Complete Project Isolation:** Strictly separated from external projects with independent Git credentials (`useraadityaid@gmail.com`).

---

## 🤖 The Autonomous Sub-Agent Swarm

```
┌────────────────────────────────────────────────────────────────────────┐
│                   POLITICAL CAMPAIGN MEDIA OS SWARM                    │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
       ┌────────────────────────────┼───────────────────────────┐
       ▼                            ▼                           ▼
┌──────────────┐             ┌──────────────┐            ┌──────────────┐
│  SUB-AGENT 1 │             │  SUB-AGENT 2 │            │  SUB-AGENT 3 │
│  Competitor  │             │  Political   │            │ Multimodal   │
│  Ad Scraper  │ ──────────► │  Copywriter  │ ─────────► │ Image Creator│
│ & Intelligence             │  (Nepali/Eng)│            │(Nano Banana) │
└──────────────┘             └──────────────┘            └──────────────┘
                                    │                           │
                                    ▼                           ▼
                             ┌──────────────┐            ┌──────────────┐
                             │  SUB-AGENT 4 │            │  SUB-AGENT 5 │
                             │  API Video   │ ─────────► │  Facebook    │
                             │  Director    │            │  Publisher   │
                             │(Creatomate/etc)           │ (Graph API)  │
                             └──────────────┘            └──────────────┘
```

### 1. Competitor Ad Scraper & Intelligence (`pipeline/competitor/competitor_analyzer_agent.py`)
- Continuously extracts Meta Ad Library data (country: `NP`) and competitor Facebook posts.
- Tracks regional spend distribution (Bagmati, Gandaki, Koshi), audience demographics (18-24, 25-34), and identifies messaging vulnerabilities to counter-position.

### 2. Political Copywriter Sub-Agent (`pipeline/copywriter/copywriter_agent.py`)
- Crafts high-converting, emotive copies in शुद्ध Devanagari Nepali, Romanized Nepali, and English.
- Implements the 4-tier mobile conversion framework:
  1. **Scroll-Stopper Hook** (3-second thumb stop)
  2. **Core Conflict / Agitation** (Lived citizen frustrations: red tape, corruption, youth migration)
  3. **Policy Solution** (Actionable legislative and executive commitments)
  4. **Call to Action** (Vote, comment, take voter survey, share)
- Automatically suggests detailed visual prompts for the Multimodal Image Creator.

### 3. Multimodal Image Creator Agent (`pipeline/image_editor/`)
- Powered by Antigravity multimodal generation (Nano Banana / Imagen).
- Renders high-contrast bilingual stat cards, candidate hero visuals, and carousel cards matching RSP branding (`#0066CC` electric blue, `#FFB800` bell gold).

### 4. API Video Director Sub-Agent (`pipeline/video_editor/video_api_agent.py`)
- Programmatically constructs dynamic 9:16 vertical short-form Reels (1080x1920) for Facebook and Instagram.
- Integrates with video editing APIs (Creatomate, Shotstack) or local render engines to assemble kinetic subtitles, sound effects, voiceovers, and lower-third tickers.

### 5. Facebook Publisher & Scheduler (`pipeline/publisher/facebook_uploader.py`)
- Integrates with Meta Graph API v26.0 for scheduled publishing to Facebook Pages.
- Enforces strict safety rails: dry-run inspection mode before any live post goes out.

---

## 📂 Project Directory Structure

```text
├── docs/
│   ├── STYLE_GUIDE.md             # Comprehensive writing rules, tone pillars, and copy frameworks
│   └── SUBAGENT_ARCHITECTURE.md   # Swarm specs, agent contracts, and execution roadmap
├── data/
│   ├── campaign.db                # Local SQLite relational database (ads, surveys, media queue)
│   ├── generated_images/          # Rendered campaign infographics, stat cards, and banners
│   └── generated_videos/          # 9:16 Video Reel project manifests and rendered clips
├── pipeline/
│   ├── competitor/                # Competitor intelligence & ad analysis agent
│   ├── copywriter/                # Emotive bilingual political copywriter agent
│   ├── image_editor/              # Multimodal image and stat card creator agent
│   ├── video_editor/              # API-driven video editing and Reel assembly agent
│   └── publisher/                 # Meta Graph API publisher & queue processor
├── skills/
│   ├── meta_ad_scraper.py         # Meta Ad Library API & Playwright extractor
│   ├── live_chrome_scraper.py     # Live CDP scraper for Facebook pages
│   └── political_sentiment_analyzer.py
├── surveys/
│   └── survey_engine.py           # Voter questionnaire and demographic poll engine
├── config.py                      # App configuration & Graph API credentials
└── database.py                    # Local SQL database schema & queue manager
```

---

## 🚀 Quickstart & Execution

### 1. Run Voter Sentiment Survey & Intelligence
```bash
python3 surveys/survey_engine.py
```

### 2. Analyze Competitor Ads & Find Counter-Strategies
```bash
python3 pipeline/competitor/competitor_analyzer_agent.py
```

### 3. Generate Emotive Facebook Ad Copy
```bash
python3 pipeline/copywriter/copywriter_agent.py
```

### 4. Assemble 9:16 Video Reel Storyboard
```bash
python3 pipeline/video_editor/video_api_agent.py
```

### 5. Review & Publish Media Queue (Dry-Run Mode)
```bash
python3 pipeline/publisher/facebook_uploader.py
```

---

## 🎨 Writing Style & Tone Playbook
For complete messaging guardrails, rhetorical formulas (PAS, BAB), and bilingual Devanagari templates, refer to [docs/STYLE_GUIDE.md](file:///Users/aadityasah/Documents/Political%20Facebook/docs/STYLE_GUIDE.md).
