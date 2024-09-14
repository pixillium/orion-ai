import sys
import time
import random


def sleep(min_seconds: float, max_seconds: float) -> None:
    """Pause execution for a random duration between min_seconds and max_seconds."""
    time.sleep(random.uniform(min_seconds, max_seconds))


def mprint(str: str) -> None:
    """Print a string to the console."""
    sys.stdout.write(f"{str}\n")
    sys.stdout.flush()
