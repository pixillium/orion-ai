import time
import requests
from datetime import date

from tts import speak
from utils import mprint


def command_exec(command: str):
    command_handlers = {
        "time": lambda: speak(format_time()),
        "day": lambda: speak(date.today().strftime("%A in %d, %B")),
        "weather": lambda: speak(get_weather()),
    }

    for key, handler in command_handlers.items():
        if key in command:
            handler()
            return
        else:
            mprint("Command not found")


def format_time():
    current_time = time.localtime()
    hours = current_time.tm_hour
    minutes = current_time.tm_min
    seconds = current_time.tm_sec

    hour_word = f"{hours % 12 if hours % 12 != 0 else 12}"
    if minutes == 0:
        time_str = f"{hour_word} o'clock and {seconds} seconds"
    elif seconds == 0:
        time_str = f" {hour_word} {minutes}"
    else:
        time_str = f" {hour_word} {minutes} and {seconds} seconds"

    return time_str


def get_weather():
    response = requests.get(
        "https://api.openweathermap.org/data/2.5/weather?q=bangladesh&appid=e9252ace9aab313a5f838a01bf0dc527&units=metric"
    )
    weather = response.json().get("main", {}).get("temp", "unavailable")
    return weather
