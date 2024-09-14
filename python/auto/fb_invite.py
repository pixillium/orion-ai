import os
import sys

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

# Adjusting the sys.path to include the parent directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from tts import speak
from driver import chrome
from utils import sleep, mprint


class FacebookBot:
    def __init__(self):
        self.driver = None

    def scroll_to_down(
        self, driver, scroll_count: int = 10, group_id: str = ""
    ) -> None:
        """Scroll down the Facebook group members page to load more users."""
        try:
            driver.get(f"https://www.facebook.com/groups/{group_id}/members/")
            for _ in range(scroll_count):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                sleep(2, 5)

            # Scroll back to the top of the page
            driver.execute_script("window.scrollTo(0, 0);")
            sleep(2, 5)
            mprint("Scrolling completed.")
        except Exception as e:
            mprint(f"Error scrolling down: {e}")

    def invite_all(self, driver) -> None:
        """Invite all visible users on the page."""
        try:
            invite_btns = driver.find_elements(
                By.CSS_SELECTOR, 'div[aria-label="Add friend"]'
            )
            if not invite_btns:
                mprint(
                    "No invite buttons found. Make sure you are on the correct page."
                )
                return

            for index, btn in enumerate(invite_btns):
                mprint(f"Inviting User #{index + 1}")
                btn.click()
                sleep(0.5, 1)
                try:
                    # Close any private profile notification
                    driver.find_element(
                        By.XPATH, "//div[div[@aria-label='Close']]"
                    ).click()
                    mprint("Profile is private or invitation was not successful")
                except NoSuchElementException:
                    pass
                sleep(2, 5)

            mprint("Invitation process completed.")
        except Exception as e:
            mprint(f"Error inviting users: {e}")
        finally:
            mprint("Invite all users process finished\n=========================\n")


def main():
    """Main function to execute the Facebook group invitation automation."""
    if len(sys.argv) < 3:
        mprint("Please provide group ID and scroll count.")
        sys.exit(1)

    group_id = sys.argv[1]
    scroll_count = int(sys.argv[2])

    bot = FacebookBot()
    try:
        bot.driver = chrome()
        speak("Starting Facebook invite automation.")
        bot.scroll_to_down(bot.driver, scroll_count, group_id)
        bot.invite_all(bot.driver)
    except Exception as e:
        mprint(f"Error during Facebook invitation automation: {e}")
        sys.exit(1)
    finally:
        if bot.driver:
            bot.driver.quit()  # Ensure the driver is properly closed
        mprint("Facebook Automation completed\n=========================\n")


if __name__ == "__main__":
    main()
