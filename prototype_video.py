# create_video.py
import os
import json
import pyttsx3
from moviepy.editor import (
    ImageClip,
    AudioFileClip,
    CompositeAudioClip,
    concatenate_videoclips,
    concatenate_audioclips,
    TextClip,
    CompositeVideoClip,
)
from moviepy.config import change_settings
import moviepy.audio.fx.all as afx


# -----------------------------------------------------------
# SETTINGS
# -----------------------------------------------------------

# This line tells MoviePy exactly where to find FFmpeg
# Please check if this path is correct on your computer and update it if necessary.
change_settings({"FFMPEG_BINARY": r"C:\ffmpeg\bin\ffmpeg.exe"})

OUTPUT_DIR = "reels"
os.makedirs(OUTPUT_DIR, exist_ok=True)
VOICEOVER_DIR = "voiceovers"
os.makedirs(VOICEOVER_DIR, exist_ok=True)

VIDEO_SETTINGS = {
    "fps": 24,
    "codec": "libx264",
    "audio_codec": "aac",
    "font_path": "Arial-Bold",
    "text_color": "white",
    "text_stroke_color": "black",
    "text_stroke_width": 2,
    "text_fontsize": 50,
}


# -----------------------------------------------------------
# UTILITIES
# -----------------------------------------------------------

def tts_to_file(text: str, filename: str):
    """
    Generates speech audio from text and saves it to a file using pyttsx3.
    """
    engine = pyttsx3.init()
    engine.save_to_file(text, filename)
    engine.runAndWait()


def create_scene_clip(image_path: str, voice_text: str, caption_text: str, scene_id: int):
    """
    Creates a single video clip for a scene with image, voiceover, and captions.
    """
    voice_path = os.path.join(VOICEOVER_DIR, f"scene_{scene_id}.mp3")
    tts_to_file(voice_text, voice_path)

    voice_clip = AudioFileClip(voice_path)
    img_clip = ImageClip(image_path).set_duration(voice_clip.duration).resize(height=1080)
    
    txt_clip = (
        TextClip(
            caption_text,
            fontsize=VIDEO_SETTINGS["text_fontsize"],
            color=VIDEO_SETTINGS["text_color"],
            font=VIDEO_SETTINGS["font_path"],
            stroke_color=VIDEO_SETTINGS["text_stroke_color"],
            stroke_width=VIDEO_SETTINGS["text_stroke_width"],
        )
        .set_duration(voice_clip.duration)
        .set_position(("center", 0.8), relative=True)
    )

    video_clip = CompositeVideoClip([img_clip, txt_clip])
    
    return video_clip, voice_clip


def generate_reel(scenes_data: list, image_paths: list, output_filename: str):
    """
    Main function to orchestrate the video generation.
    """
    if not isinstance(scenes_data, list) or not scenes_data:
        print("❌ Invalid or empty scenes data.")
        return

    clips = []
    audio_clips = []
    
    for i, scene in enumerate(scenes_data):
        img_path = image_paths[i % len(image_paths)]
        
        if not os.path.exists(img_path):
            print(f"❌ Image not found for scene {i}: {img_path}")
            continue

        video_clip, audio_clip = create_scene_clip(
            image_path=img_path,
            voice_text=scene.get("voiceover", ""),
            caption_text=scene.get("text", ""),
            scene_id=i
        )
        
        clips.append(video_clip)
        audio_clips.append(audio_clip)

    if not clips:
        print("❌ No video clips were created.")
        return

    final_video = concatenate_videoclips(clips, method="compose")
    
    final_audio = concatenate_audioclips(audio_clips)
    
    music_path = "background.mp3"
    if os.path.exists(music_path):
        music_clip = AudioFileClip(music_path).fx(afx.volumex, 0.2)
        music_clip = music_clip.set_duration(final_video.duration)
        final_audio = CompositeAudioClip([final_audio, music_clip])

    final_video = final_video.set_audio(final_audio)

    final_video_path = os.path.join(OUTPUT_DIR, output_filename)
    try:
        final_video.write_videofile(
            final_video_path,
            fps=VIDEO_SETTINGS["fps"],
            codec=VIDEO_SETTINGS["codec"],
            audio_codec=VIDEO_SETTINGS["audio_codec"],
            temp_audiofile=os.path.join(VOICEOVER_DIR, "temp_audio.m4a"),
        )
        print(f"✅ Reel successfully generated at: {final_video_path}")
    except Exception as e:
        print(f"❌ Error during video export: {e}")


# -----------------------------------------------------------
# EXAMPLE USAGE
# -----------------------------------------------------------

if __name__ == "__main__":
    SCENES_JSON = """
    [
      {
        "scene": "Close-up of clay on a wheel",
        "voiceover": "It all begins with humble clay.",
        "text": "Every masterpiece starts simple"
      },
      {
        "scene": "Artisan shaping the pot",
        "voiceover": "Skilled hands give life to tradition.",
        "text": "Crafted with passion"
      },
      {
        "scene": "Shiny finished pot",
        "voiceover": "A treasure for your home.",
        "text": "Bring home tradition"
      }
    ]
    """
    
    scenes_data = json.loads(SCENES_JSON)
    image_paths = [
        "pottery_rawmaterial.jpg",
        "artisants.jpg",
        "pottery_finalproduct.jpg",
    ]

    generate_reel(scenes_data, image_paths, "artisan_reel.mp4")