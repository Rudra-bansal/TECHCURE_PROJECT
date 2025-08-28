import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Configure Gemini with API key from .env
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Select model
model = genai.GenerativeModel("gemini-1.5-flash")

print("✨ Welcome to Artisan Storytelling Assistant ✨")
print("This tool helps local artisans promote their products through storytelling.\n")

while True:
    # Collect artisan/product details
    artisan_name = input("👉 Enter artisan's name: ")
    product = input("👉 What product do they make? ")
    material = input("👉 What material is used? (e.g., clay, wood, fabric): ")
    inspiration = input("👉 What is their inspiration or tradition? ")
    target_audience = input("👉 Who is the target audience? (e.g., young buyers, tourists, eco-conscious customers): ")

    # Build prompt
    prompt = (
        f"Create a marketing story for artisan {artisan_name}, "
        f"who makes {product} using {material}. Their inspiration is {inspiration}. "
        f"Target audience: {target_audience}. "
        f"Give me:\n"
        f"1. A short tagline (5-10 words)\n"
        f"2. A social media caption (1-2 sentences)\n"
        f"3. A detailed story (2-3 paragraphs) highlighting artisan's journey and uniqueness."
    )

    # Generate content
    response = model.generate_content(prompt)
    story = response.text

    # Print output
    print("\n📖 Marketing Story Package:\n")
    print(story)

    # Save to file
    filename = f"{artisan_name}_{product}_marketing_story.txt".replace(" ", "_")
    with open(filename, "w", encoding="utf-8") as f:
        f.write(story)

    print(f"\n✅ Story saved as '{filename}'")

    # Ask if user wants another story
    again = input("\nDo you want to generate another artisan story? (yes/no): ").strip().lower()
    if again != "yes":
        print("\n👋 Thank you for supporting local artisans with storytelling. Goodbye!")
        break
