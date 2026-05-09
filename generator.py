import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

def extract_research_fields(research_json):
    """
    Extracts key fields from the research JSON to stay within token limits.
    """
    try:
        data = research_json
        extracted = {
            "product_name": data.get("awarenessResearch", {}).get("inferredProductName", "Product"),
            "summary": data.get("awarenessResearch", {}).get("summary", ""),
            "target_audience": data.get("awarenessResearch", {}).get("targetAudience", ""),
            "hooks": data.get("awarenessResearch", {}).get("messagingImplications", {}).get("examplesOfEffectiveHooks", []),
            "fears": data.get("psychographicResearch", {}).get("fearsAndPainPoints", [])[:5],
            "benefits": data.get("solutionNarrativeResearch", {}).get("benefits", {}).get("functionalImprovements", []),
            "mechanism": data.get("solutionNarrativeResearch", {}).get("uniqueMechanism", {}).get("simpleExplanation", ""),
            "avatar": data.get("avatarResearch", {}).get("avatarSynthesis", {}).get("rankedAvatars", [{}])[0],
            "angle": data.get("angleAvatarSynthesis", {}).get("combinations", [{}])[0],
            "guarantee": data.get("solutionNarrativeResearch", {}).get("objectionDemolition", {}).get("guaranteeStrategy", "")
        }
        return extracted
    except Exception as e:
        print(f"Error extracting research fields: {e}")
        return {}

def generate_listicle_content(research_data, media_urls):
    """
    Sends data to Groq and returns structured JSON for the listicle.
    """
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    
    prompt = f"""
    You are a world-class direct response copywriter specialized in advertorial listicles.
    Based on the following research data and available media, generate a high-converting listicle content in JSON format.
    
    RESEARCH DATA:
    {json.dumps(research_data, indent=2)}
    
    AVAILABLE MEDIA URLS:
    {json.dumps(media_urls, indent=2)}
    
    OUTPUT REQUIREMENTS:
    - Return ONLY valid JSON. No conversational text, no markdown backticks.
    - The JSON must follow this structure:
    {{
        "announcement_bar": "Short urgency/offer text",
        "blog_name": "WideInsider",
        "headline": "Punchy, curiosity-driven headline",
        "subheadline": "Benefit-driven subheadline",
        "warning_box": "Short urgency or health/safety warning",
        "author": {{
            "name": "Full Name",
            "title": "Health & Lifestyle Expert",
            "avatar_emoji": "👨‍⚕️"
        }},
        "intro_paragraphs": ["Paragraph 1", "Paragraph 2"],
        "comparison_table": {{
            "product_name": "{research_data.get('product_name')}",
            "competitor_name": "Standard Alternatives",
            "features": [
                {{"feature": "Feature name", "product_has": true, "competitor_has": false}}
            ]
        }},
        "benefits": [
            {{
                "number": 1,
                "title": "Benefit Title",
                "media_url": "One URL from the provided list that fits best",
                "paragraphs": ["Paragraph 1", "Paragraph 2"]
            }}
        ],
        "mid_page_cta": {{
            "title": "Why you need this now",
            "checklist": ["Point 1", "Point 2"],
            "button_text": "Claim Your Offer"
        }},
        "final_cta": {{
            "headline": "Ready to change your life?",
            "text": "Final persuasive sentence",
            "button_text": "Check Availability"
        }},
        "sticky_bar_text": "Limited Time Offer: Get {research_data.get('product_name')} today!"
    }}
    
    CRITICAL:
    - Generate exactly 7 benefit sections.
    - Assign the most relevant media URL to each benefit from the provided list. If no media is relevant or the list is empty, use a placeholder like 'https://via.placeholder.com/600x400?text=Product+Image'.
    - Ensure the tone is editorial, persuasive, and authentic.
    """
    
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that outputs only valid JSON."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model="llama-3.3-70b-versatile",
            response_format={"type": "json_object"}
        )
        
        content = chat_completion.choices[0].message.content
        # Strip potential backticks if any (though response_format should prevent them)
        content = content.strip().strip('`').replace('json\n', '', 1)
        
        return json.loads(content)
    
    except Exception as e:
        print(f"Groq API error: {e}")
        return {
            "announcement_bar": "Limited Time Offer — Shop Now",
            "blog_name": "WideInsider",
            "headline": "The Comfort Flat That Actually Works",
            "subheadline": "Here is what makes it different",
            "warning_box": "Read this before buying another pair of shoes",
            "author": {
                "name": "Sarah Mitchell",
                "title": "Health & Lifestyle Expert",
                "avatar_emoji": "👩‍⚕️"
            },
            "intro_paragraphs": [
                "Finding the right shoe when you have wide feet or bunions is exhausting.",
                "After testing dozens of options, one stood out for all the right reasons."
            ],
            "comparison_table": {
                "product_name": "WideStep Elora",
                "competitor_name": "Standard Alternatives",
                "features": [
                    {"feature": "40% wider toe box", "product_has": True, "competitor_has": False},
                    {"feature": "Orthopedic sole", "product_has": True, "competitor_has": False},
                    {"feature": "All-day comfort", "product_has": True, "competitor_has": False}
                ]
            },
            "benefits": [
                {"number": i, "title": f"Benefit {i}", "media_url": "https://via.placeholder.com/600x400?text=Product", "paragraphs": ["Content coming soon."]}
                for i in range(1, 8)
            ],
            "mid_page_cta": {
                "title": "Why thousands of women love this flat",
                "checklist": ["30-Day Money Back Guarantee", "Free Shipping", "Buy 1 Get 1 Free"],
                "button_text": "Get Your Pair Today"
            },
            "final_cta": {
                "headline": "Your feet deserve better",
                "text": "Try them risk-free today.",
                "button_text": "Check Availability"
            },
            "sticky_bar_text": "Limited Time Offer — Get WideStep Elora today"
        }