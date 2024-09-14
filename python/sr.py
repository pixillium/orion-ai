from tts import speak
from utils import mprint
import speech_recognition as sr

not_recognized = 0


def recognize_speech():
    global not_recognized

    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        recognizer.pause_threshold = 0.5
        recognizer.energy_threshold = 300
        recognizer.dynamic_energy_threshold = True
        recognizer.non_speaking_duration = 0.5
        recognizer.dynamic_energy_adjustment_ratio = 1.5

    while True:
        try:
            with mic as source:
                audio = recognizer.listen(source)
            text = recognizer.recognize_google(audio)

            not_recognized = 0
            mprint(f"Listening ...\nRecognized: {text}\n")
        except sr.UnknownValueError:
            if not_recognized == 3:
                pass
            else:
                not_recognized += 1
                mprint("Google Speech Recognition could not understand audio")

        except sr.RequestError as e:
            speak("Error in Speeech Recognition service.")
            mprint(f"Could not request results {e}\n")


if __name__ == "__main__":
    recognize_speech()
