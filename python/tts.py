import sys
import pyttsx3
from utils import mprint


def init_tts_engine():
    """Initialize and configure the text-to-speech engine."""
    try:
        tts_engine = pyttsx3.init()
        voices = tts_engine.getProperty("voices")

        if not voices:
            raise RuntimeError("No voices available for TTS engine.")

        tts_engine.setProperty("voice", voices[0].id)
        tts_engine.setProperty("rate", 135)
        return tts_engine
    except Exception as e:
        mprint(f"[ERROR] Failed to initialize TTS engine: {e}")
        raise


def speak(text):
    """Convert text to speech."""
    if not isinstance(text, str):
        raise ValueError("The 'text' parameter must be a string.")

    try:
        tts_engine = init_tts_engine()
        tts_engine.say(text)
        tts_engine.runAndWait()
    except Exception as e:
        mprint(f"[ERROR] Failed to speak text: {e}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        text_to_speak = sys.argv[1]
        speak(text_to_speak)
    else:
        mprint(f"[ERROR] No text provided to speak.")
