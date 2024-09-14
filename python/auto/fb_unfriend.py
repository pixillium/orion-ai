import os
import sys
from selenium.webdriver.common.by import By

# Adjusting the sys.path to include the parent directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from driver import chrome
from utils import sleep, mprint


class FacebookUnfollowBot:
    def __init__(self):
        self.driver = None

    def scroll_to_down(self, driver) -> None:
        """Scroll down the page to load more friends."""
        try:
            for _ in range(6):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                sleep(2, 5)

            # Scroll back to the top of the page
            driver.execute_script("window.scrollTo(0, 0);")
            mprint("Scrolling completed.")
        except Exception as e:
            mprint(f"Error during scrolling: {e}")

    def unfollow_all(self, driver) -> None:
        """Unfollow all friends listed on the page."""
        try:
            # Find all elements that represent friends options
            option_elements = driver.find_elements(
                By.XPATH, "//div[div[@aria-label='Friends']]"
            )
            if not option_elements:
                mprint(
                    "No friends options found. Make sure you are on the correct page."
                )
                return

            for index, option in enumerate(option_elements):
                mprint(f"Processing User #{index + 1}")
                option.click()
                sleep(1.5, 2.5)

                # Click on "Unfriend" button
                driver.find_element(
                    By.XPATH, "//span[text()='Unfriend']/ancestor::div[3]"
                ).click()
                sleep(2, 5)

                # Confirm the unfollow action
                driver.find_element(
                    By.CSS_SELECTOR, 'div[aria-label="Confirm"]'
                ).click()
                sleep(2, 5)

            mprint("Unfollowing process completed.")
        except Exception as e:
            mprint(f"Error during unfollowing: {e}")
        finally:
            mprint("Unfollowing all accounts.\n=========================\n")


def main():
    """Main function to execute the Facebook unfollow automation."""
    bot = FacebookUnfollowBot()
    try:
        bot.driver = chrome()
        bot.driver.get(
            "https://www.facebook.com/profile.php?id=61560492642646&sk=friends"
        )

        bot.scroll_to_down(bot.driver)
        bot.unfollow_all(bot.driver)
    except Exception as e:
        mprint(f"Error in Facebook unfollow automation: {e}")
        sys.exit(1)
    finally:
        if bot.driver:
            bot.driver.quit()  # Ensure the driver is properly closed
        mprint("Facebook Unfollow Automation completed\n=========================\n")


if __name__ == "__main__":
    main()
