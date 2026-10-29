#!/usr/bin/env python3
"""
Political Copywriter Sub-Agent for Nepal Campaign Intelligence OS
Generates high-converting, emotive, policy-grounded Facebook ad copies and post scripts
in Devanagari Nepali, Romanized Nepali, and English.

Author: Aaditya Sah (useraadityaid@gmail.com)
"""

import sys
import json
from pathlib import Path
from typing import Dict, Any, List, Optional

# Add parent directory for module imports
BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(BASE_DIR))

from database import LocalSQLDatabase


class PoliticalCopywriter:
    """
    Sub-agent responsible for translating voter sentiment, survey data,
    and political campaign priorities into persuasive Facebook ad copy.
    """

    def __init__(self, db: Optional[LocalSQLDatabase] = None):
        self.db = db or LocalSQLDatabase()

    def get_voter_sentiment_context(self) -> Dict[str, Any]:
        """Queries local database for live voter survey priorities."""
        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT top_issue, COUNT(*) as vote_count 
                    FROM survey_responses 
                    GROUP BY top_issue 
                    ORDER BY vote_count DESC
                """)
                top_issues = [dict(row) for row in cursor.fetchall()]

                cursor.execute("SELECT COUNT(*) as total_voters FROM survey_responses")
                total_voters = cursor.fetchone()["total_voters"]

                return {
                    "total_responses": total_voters,
                    "top_issues": top_issues
                }
        except Exception as e:
            return {
                "total_responses": 0,
                "top_issues": [{"top_issue": "Anti-Corruption & Service Delivery", "vote_count": 1}]
            }

    def generate_ad_copy(
        self,
        topic: str = "anti_corruption",
        target_audience: str = "youth_urban",
        province: str = "Bagmati",
        language: str = "nepali"
    ) -> Dict[str, Any]:
        """
        Generates a 4-tier Facebook ad copy (Hook, Agitation, Solution, CTA)
        along with an optimized prompt for the Multimodal Image Creator agent.
        """
        sentiment = self.get_voter_sentiment_context()
        top_issue_str = sentiment["top_issues"][0]["top_issue"] if sentiment["top_issues"] else "सुशासन र भ्रष्टाचार नियन्त्रण"

        # Templates tailored to Nepal campaign dynamics
        campaign_templates = {
            "anti_corruption": {
                "nepali": {
                    "headline": "🚨 बिचौलिया बिना सरकारी काम कहिले बन्ने? नागरिकको सास्ती अब अन्त्य हुनुपर्छ!",
                    "hook": "५ घण्टा लाइन बस्दा पनि ढिलासुस्ती, आफ्नै अधिकार लिन पनि चाकडी गर्नुपर्ने अवस्था कहिलेसम्म?",
                    "body": (
                        "सरकारी कार्यालयमा नागरिकले भोग्नुपरेको हैरानी कुनै नयाँ समस्या होइन। "
                        "फाइल अड्काउने र बिचौलिया पोस्ने पुराना सिन्डिकेटहरूले जनताको समय र आत्मसम्मान दुवै लुटिरहेका छन्। "
                        "हाम्रो प्रष्ट दृष्टिकोण छ: सार्वजनिक सेवामा आमूल रूपान्तरण र डिजिटल पारदर्शी प्रणाली!"
                    ),
                    "bullets": [
                        "🔹 सम्पूर्ण सार्वजनिक सेवालाई टाइम-बाउन्ड र पारदर्शी बनाउने",
                        "🔹 सेवाग्राहीलाई अनावश्यक सास्ती दिनेमाथि तत्काल कारबाही",
                        "🔹 दलीय भागबण्डा अन्त्य गरी योग्य र सक्षम जनशक्ति परिचालन"
                    ],
                    "cta": "👇 तपाईंले हालै सरकारी सेवा लिँदा कस्तो अनुभव गर्नुभयो? आफ्नो राय कमेन्टमा राख्नुहोस् र नागरिक अभियानमा जोडिनुहोस्।",
                    "hashtags": ["#RSP", "#RabiLamichhane", "#GoodGovernance", "#NepalkoAawaz", "#ServiceDelivery"],
                    "image_prompt": (
                        "High contrast photojournalistic documentary style: Front desk of a bustling Nepali public office, "
                        "modern digital token system displayed prominently, frustrated young citizen receiving instant transparent service, "
                        "warm natural lighting, striking blue and gold accents (#0066CC), professional cinematic 8k."
                    )
                },
                "english": {
                    "headline": "🚨 How long must citizens wait in line for their basic rights? Time for radical governance reform.",
                    "hook": "Hours wasted in bureaucratic queues just to get simple documents signed. The status quo cannot continue.",
                    "body": (
                        "Decades of political patronage have crippled public service delivery in Nepal. "
                        "Ordinary citizens bear the daily brunt of inefficiency, lost files, and institutional inertia. "
                        "We stand for absolute meritocracy, 100% digital governance, and uncompromising accountability."
                    ),
                    "bullets": [
                        "🔹 End political interference in civil service administration",
                        "🔹 Implement time-bound digital services for passports, licenses, and permits",
                        "🔹 Zero tolerance for corruption at every level of government"
                    ],
                    "cta": "👉 Stand with transparent governance. Share your thoughts in the comments below.",
                    "hashtags": ["#NepalReform", "#RSP", "#TransparencyNow", "#PublicServiceFirst"],
                    "image_prompt": (
                        "Clean modern editorial infographic: Split layout showing traditional chaotic paper files vs sleek digital tablet interface, "
                        "bold typography overlay 'CITIZENS FIRST, CORRUPTION ZERO', dark navy and vibrant electric blue palette."
                    )
                }
            },
            "youth_employment": {
                "nepali": {
                    "headline": "✈️ दैनिक हजारौं युवा विदेशिन बाध्य: आफ्नो माटोमा भविष्य कहिले?",
                    "hook": "त्रिभुवन विमानस्थलको प्रस्थान कक्षमा आँसु झार्दै बिदाइ हुने यो बाध्यता अब रोकिनैपर्छ।",
                    "body": (
                        "नेपालका प्रतिभाशाली युवाहरू विदेशी मरुभूमिमा पसिना बगाउन विवश छन्। "
                        "देशमै अवसर, लगानीमैत्री वातावरण र उद्यमशीलताको सम्मान नभएसम्म यो पलायन रोकिँदैन। "
                        "हाम्रो संकल्प: स्वदेशमै उद्योग, योग्यता अनुसारको रोजगारी र परदेशमा रहेका नेपालीहरूको मताधिकार सुनिश्चितता।"
                    ),
                    "bullets": [
                        "✅ स्वदेशी स्टार्टअप र कृषि-प्रविधि उद्योगलाई कर छुट र सहुलियत",
                        "✅ विदेशमा रहेका नेपालीहरूको मताधिकार (Voting Rights) कार्यान्वयन",
                        "✅ रेमिट्यान्सलाई उत्पादनशील उद्योग र पूर्वाधारमा लगानी गर्ने नीति"
                    ],
                    "cta": "🔔 घण्टी परिवर्तनको संकेत हो—युवा पुस्ताको भविष्य निर्माणमा साथ दिनुहोस्!",
                    "hashtags": ["#YouthForChange", "#YouthEmployment", "#RSP", "#HamroNepal", "#RabiLamichhane"],
                    "image_prompt": (
                        "Cinematic wide shot: Energetic Nepali youth working in modern collaborative tech and agricultural workspace in Kathmandu valley, "
                        "Himalayan peaks in soft background morning glow, inspiring hopeful mood, crisp RSP blue branding."
                    )
                }
            }
        }

        # Select matching category
        cat_data = campaign_templates.get(topic, campaign_templates["anti_corruption"])
        copy_data = cat_data.get(language, cat_data.get("nepali"))

        # Combine into complete Facebook formatted ad text
        full_ad_text = (
            f"{copy_data['headline']}\n\n"
            f"{copy_data['hook']}\n\n"
            f"{copy_data['body']}\n\n"
            f"मुख्य प्रतिबद्धता तथा कार्ययोजना:\n"
            + "\n".join(copy_data["bullets"]) + "\n\n"
            f"{copy_data['cta']}\n\n"
            + " ".join(copy_data["hashtags"])
        )

        return {
            "topic": topic,
            "target_audience": target_audience,
            "province": province,
            "language": language,
            "headline": copy_data["headline"],
            "hook": copy_data["hook"],
            "body": copy_data["body"],
            "bullets": copy_data["bullets"],
            "cta": copy_data["cta"],
            "hashtags": copy_data["hashtags"],
            "full_ad_text": full_ad_text,
            "suggested_image_prompt": copy_data["image_prompt"],
            "voter_context": sentiment
        }

    def enqueue_for_review(self, ad_copy: Dict[str, Any]) -> int:
        """
        Stores the newly written ad copy into the media queue for the Image Creator
        or Video Director agent to generate the visual and finalize publication.
        """
        return self.db.enqueue_media(
            media_type="image",
            title=f"Ad: {ad_copy['headline'][:40]}...",
            caption=ad_copy["full_ad_text"],
            file_path="pending_image_render"
        )


if __name__ == "__main__":
    print("=" * 70)
    print("🧠 Testing Political Copywriter Sub-Agent")
    print("=" * 70)

    writer = PoliticalCopywriter()
    
    # Generate Anti-Corruption Ad Copy
    ad_1 = writer.generate_ad_copy(topic="anti_corruption", province="Bagmati", language="nepali")
    print(f"\n[Generated Ad Headline]:\n{ad_1['headline']}")
    print(f"\n[Hook]:\n{ad_1['hook']}")
    print(f"\n[Full Facebook Text Sample]:\n{ad_1['full_ad_text'][:250]}...\n")
    print(f"[Image Creator Brief]:\n{ad_1['suggested_image_prompt']}\n")

    # Enqueue into database
    item_id = writer.enqueue_for_review(ad_1)
    print(f"✅ Enqueued generated ad copy into local database media_queue (ID: {item_id})")
