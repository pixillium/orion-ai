import os
import sys
from selenium.webdriver.common.by import By

# Adjusting the sys.path to include the parent directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from tts import speak
from driver import chrome
from utils import sleep, mprint


class TwitterFollowerBot:
    def __init__(self):
        self.driver = None

    def follow_users(self, driver) -> None:
        """Follow all users found on the Twitter follow page."""
        try:
            # Find all "Follow" buttons on the page
            follow_buttons = driver.find_elements(
                By.XPATH, "//button//div//span//span[text()='Follow']"
            )
            if not follow_buttons:
                mprint(
                    "No 'Follow' buttons found. Make sure the page is loaded correctly."
                )
                return

            # Click each "Follow" button
            for index, button in enumerate(follow_buttons):
                mprint(f"Processing User #{index + 1}")
                button.click()
                sleep(2, 5)  # Wait between clicks

            mprint("Successfully followed all users.")
        except Exception as e:
            mprint(f"Error in follow_users: {e}")
        finally:
            mprint("Follow process completed\n=========================\n")


def main():
    """Main function to execute the Twitter follow automation."""
    bot = TwitterFollowerBot()
    try:
        bot.driver = chrome()
        speak("Starting Twitter follow automation.")
        bot.driver.get("https://x.com/i/connect_people")
        sleep(3, 5)  # Wait for the page to load
        bot.follow_users(bot.driver)
    except Exception as e:
        mprint(f"Error during Twitter follow automation: {e}")
        sys.exit(1)
    finally:
        if bot.driver:
            bot.driver.quit()  # Ensure the driver is properly closed
        mprint("Twitter Follow Automation completed\n=========================\n")


if __name__ == "__main__":
    main()
