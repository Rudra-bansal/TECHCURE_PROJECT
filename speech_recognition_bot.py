import speech_recognition as sr
from googletrans import Translator
import pyttsx3
from nltk.tokenize import sent_tokenize
import nltk
nltk.download('punkt')


# Function to get speech input in Hindi
def get_speech_input():
    recognizer = sr.Recognizer()

    # List available microphones
    mic_list = sr.Microphone.list_microphone_names()
    print("Available Microphones:")
    for i, mic_name in enumerate(mic_list):
        print(f"{i}: {mic_name}")

    # Use default microphone (change index after checking list above)
    mic_index = 0  

    print("\n🎤 Please speak your product story in Hindi...")

    with sr.Microphone(device_index=mic_index) as source:
        recognizer.adjust_for_ambient_noise(source, duration=15)
        try:
            audio = recognizer.listen(source, timeout=15, phrase_time_limit=10)
        except sr.WaitTimeoutError:
            print("⏳ No speech detected within timeout. Try again.")
            return None

    try:
        text = recognizer.recognize_google(audio, language="hi-IN")
        print(f"🎤 Your product story (Hindi): {text}")
        return text
    except sr.UnknownValueError:
        print("❌ Sorry, I could not understand the audio (unclear speech).")
    except sr.RequestError:
        print("⚠️ Could not connect to Google Speech Recognition service.")
    return None


# Function to translate Hindi → English
def translate_text_to_english(text):
    translator = Translator()
    translation = translator.translate(text, src='hi', dest='en')
    return translation.text


# Function to narrate the translated story in English
def narrate_story(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 1)

    voices = engine.getProperty('voices')
    for voice in voices:
        if "English" in voice.name:
            engine.setProperty('voice', voice.id)
            break

    engine.say(text)
    engine.runAndWait()


# Function to generate subtitles
def generate_subtitles(text):
    for sentence in sent_tokenize(text):
        print(f"📺 Subtitle: {sentence}")


# Main chatbot function
def chatbot():
    story_in_hindi = get_speech_input()
    if story_in_hindi:
        story_in_english = translate_text_to_english(story_in_hindi)
        print(f"✅ Translated story (English): {story_in_english}")
        narrate_story(story_in_english)
        generate_subtitles(story_in_english)


if __name__ == "__main__":
    chatbot()






