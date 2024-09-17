from tts import speak
from utils import mprint
from command_exec import command_exec
import speech_recognition as sr

NOT_RECOGNIZED = 0
STATE = True


def recognize_speech():
    global NOT_RECOGNIZED
    global STATE

    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        recognizer.pause_threshold = 0.5
        recognizer.energy_threshold = 300
        recognizer.dynamic_energy_threshold = True
        recognizer.non_speaking_duration = 0.5
        recognizer.dynamic_energy_adjustment_ratio = 1.5

    while STATE:
        try:
            with mic as source:
                audio = recognizer.listen(source)
            text = recognizer.recognize_google(audio).lower()

            if text:
                if (
                    text.startswith("exit")
                    or text.startswith("quit")
                    or text.startswith("stop")
                ):
                    mprint(f"Exiting, Sir ...\n")
                    speak("Exiting, Sir!")
                    STATE = False
                    break
                else:
                    command_exec(text)

            NOT_RECOGNIZED = 0
        except sr.UnknownValueError:
            if NOT_RECOGNIZED == 3:
                pass
            else:
                NOT_RECOGNIZED += 1
                mprint("Google Speech Recognition could not understand audio")

        except sr.RequestError as e:
            speak("Error in Speeech Recognition service.")
            mprint(f"Could not request results {e}\n")


if __name__ == "__main__":
    recognize_speech()
