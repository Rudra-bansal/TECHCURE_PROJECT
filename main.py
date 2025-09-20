import os
import json
from moviepy.config import change_settings

# Make sure these file names and function names are correct
from storygenerator import generate_script
from prototype_video import generate_reel

# --- Update this path to match your ImageMagick installation ---
change_settings({"IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.2-Q16-HDRI\magick.exe"})

def main():
    print("🎬 Starting the reel generation process...")

    # Define your project details
    artisan_info = {
        "artisan_name": "Ravi Sharma",
        "product": "handmade clay pot",
        "material": "natural clay",
        "inspiration": "traditional village art",
        "target_audience": "urban families who love tradition"
    }

    # Images for the video
    IMAGES = [
        "pottery_rawmaterial.jpg",
        "artisants.jpg",
        "pottery_finalproduct.jpg",
       
    ]

    # Step 1: Generate the script using Gemini
    scenes_data = generate_script(**artisan_info)

    if not scenes_data:
        print("❌ Failed to generate a valid script. Exiting.")
        return

    print("✅ Script successfully generated:")
    print(json.dumps(scenes_data, indent=2))
    print("-" * 30)

    # Step 2: Build the video from the script and images
    output_filename = f"{artisan_info['artisan_name'].replace(' ', '_')}_{artisan_info['product'].replace(' ', '_')}_reel.mp4"
    generate_reel(scenes_data=scenes_data, image_paths=IMAGES, output_filename=output_filename)

    print(f"✅ Process complete! Video saved as: {output_filename}")


if __name__ == "__main__":
    main()