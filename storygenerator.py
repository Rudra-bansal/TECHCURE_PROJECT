# storygeneration.py
import os
import json
import re
from dotenv import load_dotenv
import google.generativeai as genai
from json import JSONDecodeError

# --- Load API key safely ---
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise EnvironmentError("❌ GOOGLE_API_KEY not found. Please set it in your .env file.")

genai.configure(api_key=API_KEY)


def build_prompt(artisan_name, product, material, inspiration, target_audience):
    """
    Build a concise prompt for Gemini to generate a marketing reel script.
    Includes system instructions and a JSON example for robust output.
    """
    return f"""
You are a scriptwriter for social media marketing reels. Your task is to generate a compelling and concise script for a product created by a local artisan.

Instructions:
1.  **The output must be a JSON array of 3-4 objects.**
2.  **Each object must have the keys `scene`, `voiceover`, and `text`.**
3.  **Keep the total voiceover content around 100-120 words.**
4.  **The final scene must be a clear Call to Action (CTA).**

Context:
- Artisan: {artisan_name}
- Product: {product}
- Material: {material}
- Inspiration: {inspiration}
- Target audience: {target_audience}

Example JSON format:
```json
[
  {{
    "scene": "A close-up shot of the artisan's hands shaping the clay.",
    "voiceover": "Every piece tells a story, handcrafted with passion and tradition.",
    "text": "Crafted by hand."
  }},
  {{
    "scene": "The finished ceramic vase, slowly rotating on a pedestal with light catching its unique glaze.",
    "voiceover": "This isn't just a vase; it's a piece of art, a blend of timeless technique and modern design.",
    "text": "Timeless design, modern home."
  }},
  {{
    "scene": "The vase is placed in a cozy living room, bringing warmth and color to the space.",
    "voiceover": "Bring home a piece of art that brightens your space and supports local craftsmanship.",
    "text": "Support local artisans."
  }},
  {{
    "scene": "A final shot with the artisan's brand logo and website URL.",
    "voiceover": "Find your perfect piece and bring home tradition today.",
    "text": "Shop now at [Your Website]."
  }}
]
"""


def generate_script(artisan_name, product, material, inspiration, target_audience):
    """
    Uses Gemini to create a marketing reel script.
    Returns a list of dictionaries with scene, voiceover, and text.
    """
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = build_prompt(artisan_name, product, material, inspiration, target_audience)

    try:
        response = model.generate_content(prompt)
        raw_text = response.text.strip()
    except Exception as e:
        print(f"❌ Error during Gemini API call: {e}")
        return None  # Correctly indented

    json_match = re.search(r"```json\n(.*)\n```", raw_text, re.DOTALL)
    if json_match:
        text_to_parse = json_match.group(1).strip()
    else:
        text_to_parse = raw_text

    try:
        data = json.loads(text_to_parse)
        if isinstance(data, list) and all(isinstance(s, dict) and "scene" in s and "voiceover" in s for s in data):
            return [
                {
                    "scene": s.get("scene", "").strip(),
                    "voiceover": s.get("voiceover", "").strip(),
                    "text": s.get("text", "").strip(),
                }
                for s in data
            ]
        else:
            print("⚠️ Parsed JSON but it does not match the expected format.")
            return None  # Correctly indented

    except JSONDecodeError as e:
        print(f"❌ JSON parsing failed: {e}")
        return None  # Correctly indented


# --- Example Usage for a Hackathon Demo ---
if __name__ == "__main__":
    test_script = generate_script(
        artisan_name="Aisha",
        product="Hand-stitched Leather Journal",
        material="Full-grain cowhide, recycled paper",
        inspiration="Classic travel diaries",
        target_audience="Writers, students, adventurers"
    )

    if test_script:
        print("✅ Successfully generated and parsed a valid script:")
        print(json.dumps(test_script, indent=2))
    else:
        print("❌ Script generation and parsing failed.")