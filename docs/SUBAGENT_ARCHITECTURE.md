# Sub-Agent Architecture & Operating Pipeline

## 1. System Vision
The **Nepal Campaign Intelligence & Social Media OS** operates as a specialized swarm of autonomous sub-agents designed to analyze, produce, evaluate, and publish high-impact political campaigns on Facebook.

Each sub-agent has a dedicated responsibility, strict input/output contracts, and direct integration with our isolated local SQLite database (`data/campaign.db`).

```
┌────────────────────────────────────────────────────────────────────────┐
│                        CAMPAIGN MEDIA OS SWARM                         │
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

---

## 2. Detailed Sub-Agent Specifications

### Sub-Agent 1: Competitor Intelligence & Ad Scraper (`competitor_agent`)
- **Role:** Continuous market surveillance on Facebook Ad Library and rival party/candidate pages.
- **Capabilities:**
  - Connects to Meta Ad Library API and active Chrome CDP session for headless extraction.
  - Analyzes competitor spend distribution by region (Bagmati, Gandaki, Koshi, etc.).
  - Extracts active messaging angles, video hooks, and demographic targeting brackets (18-24, 25-34, 35+).
  - Flags emerging negative attacks or counter-narratives for rapid response.
- **Storage:** Persists raw and normalized ad records into `political_ads` table in `campaign.db`.

---

### Sub-Agent 2: Political Copywriter (`copywriter_agent`)
- **Role:** Crafts emotive, high-converting political copy in Devanagari Nepali, Romanized Nepali, and English.
- **Capabilities:**
  - Pulls voter pain points directly from `survey_responses` and live issues.
  - Implements proven copywriting formulas:
    - **P-A-S:** Problem (भ्रष्टाचार र सास्ती) -> Agitation (दैनिक जीवनको असर) -> Solution (घण्टी र नीतिगत सुधार)
    - **B-A-B:** Before -> After -> Bridge
    - **Hook-Story-Offer (CTA):** Emotional narrative leading to survey participation or voting mobilization.
  - Generates 3 A/B test variations per campaign theme:
    - Variant A: Urgent & Confrontational
    - Variant B: Data & Policy Focused
    - Variant C: Inspirational & Community Storytelling
- **Output:** Structured JSON containing `headline`, `hook`, `primary_text`, `call_to_action`, and suggested visual prompt.

---

### Sub-Agent 3: Multimodal Image Creator (Antigravity / Nano Banana)
- **Role:** Generates visual assets, statistical infographics, social cards, and hero banners.
- **Capabilities:**
  - Generates custom high-resolution visuals via Antigravity image generation pipelines.
  - Adheres to brand color scheme:
    - Primary: RSP Electric Blue (`#0066CC` / `#0080FF`) & Bell Gold (`#FFB800`)
    - Contrast: Deep Charcoal/Navy (`#0F172A`) and Crisp White (`#FFFFFF`)
  - Typesets clean bilingual statistical overlays (e.g. "८८% युवाको प्राथमिकता: सुशासन र रोजगारी").
- **Output:** Rendered PNG/JPG saved into `data/generated_images/` and registered into `media_queue`.

---

### Sub-Agent 4: API Video Director (`video_api_agent`)
- **Role:** Programmatic short-form video (Reel / TikTok / Shorts) creation and editing.
- **Capabilities:**
  - Connects to automated video rendering engines via REST API (Creatomate, Shotstack, or local FFmpeg pipelines).
  - Automatically stitches:
    - High-energy opening hook video clip / avatar / speaker sequence.
    - Kinetic animated subtitles in Nepali/English with keyword color highlights.
    - Background dramatic ambient audio / campaign theme score.
    - Dynamic lower-third ticker with survey stats and candidate logo.
    - Final branded end-card with RSP Bell symbol and voting appeal.
- **Output:** Rendered 1080x1920 (9:16) MP4 files saved in `data/generated_videos/` and registered in `media_queue`.

---

### Sub-Agent 5: Facebook Publisher & Scheduler (`publisher_agent`)
- **Role:** Direct API publishing, scheduling, and live performance monitoring.
- **Capabilities:**
  - Authenticates via Meta Graph API v26.0 with Page Access Tokens.
  - Manages publishing rate limits and schedules posts for peak Nepali engagement windows:
    - Morning commute: 7:30 AM – 9:00 AM NPT
    - Lunch break: 12:30 PM – 2:00 PM NPT
    - Prime evening scroll: 7:00 PM – 10:00 PM NPT
  - Dry-run verification mode ensuring zero unintended live posts without user confirmation.

---

## 3. Database Schema Overview (`campaign.db`)

1. **`political_ads`**: Stores competitor ad creative ID, page name, spend ranges, impressions, start/end dates, demographics JSON, and regions JSON.
2. **`surveys`**: Master survey definitions (e.g., `nepal_campaign_survey_01`).
3. **`survey_responses`**: Voter survey answers across provinces, age brackets, and top voting priorities.
4. **`media_queue`**: Media items awaiting rendering or publication (`post_type`, `title`, `content_text`, `media_path`, `status`).

---

## 4. One-by-One Implementation Roadmap

| Phase | Deliverable | Status |
| :--- | :--- | :--- |
| **Phase 1** | Local Infrastructure, DB isolation, Meta Graph API setup | ✅ **Complete** |
| **Phase 2** | Style Guide (`STYLE_GUIDE.md`) & Architecture Spec | ✅ **Complete** |
| **Phase 3** | Political Copywriter Sub-Agent (`pipeline/copywriter/copywriter_agent.py`) | 🚀 **In Progress** |
| **Phase 4** | Multimodal Image Creator Agent (Antigravity / Nano Banana) | ⏳ Upcoming |
| **Phase 5** | Video Editing API Connector & Automated Reel Assembly | ⏳ Upcoming |
| **Phase 6** | Competitor Intelligence Deep-Scraping & Graph API Publishing | ⏳ Upcoming |
