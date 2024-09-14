import os
import sys
from typing import List, Tuple

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException

# Adjusting the sys.path to include parent directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from tts import speak
from driver import chrome
from utils import sleep, mprint


class InstagramBot:
    def __init__(self):
        self.is_blocked = False  # Flag to indicate if the bot is blocked
        self.followed_users = []  # List to store followed users

    def numerize(self, str_num: str) -> int:
        """Convert a string with number suffixes (K, M) to an integer."""
        str_num = str_num.replace(",", "").upper()
        if str_num.endswith("K"):
            return int(float(str_num.rstrip("K")) * 1000)
        elif str_num.endswith("M"):
            return int(float(str_num.rstrip("M")) * 1_000_000)
        return int(str_num)

    def find_users(self, username: str, driver, scroll_count: int = 5) -> List[str]:
        """Retrieve followers of a user on Instagram."""
        users = []
        try:
            # Navigate to the user's Instagram page
            driver.get(f"https://www.instagram.com/{username}/")
            sleep(5, 7)

            # Click on the "followers" link
            driver.find_element(By.PARTIAL_LINK_TEXT, "followers").click()
            sleep(5, 7)

            # Locate the scrollable div containing the list of followers
            scrollable_div = driver.find_element(
                By.CSS_SELECTOR, 'div[role="dialog"] div:nth-of-type(4)'
            )

            # Scroll through the followers list to load more users
            for _ in range(scroll_count):
                sleep(2, 5)
                driver.execute_script(
                    "arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_div
                )

            # Extract unique user URLs from the list
            users = list(
                set(
                    link.get_attribute("href")
                    for link in scrollable_div.find_elements(By.TAG_NAME, "a")
                )
            )

        except TimeoutException:
            mprint("Page load timed out")  # Log if page load takes too long
        except Exception as e:
            mprint(f"Error in find_users: {e}")  # Log any other errors

        return users

    def check_user_status(self, driver) -> Tuple[bool, bool]:
        """Check if the user is already followed or if the account is private."""
        followed = bool(
            driver.find_elements(By.XPATH, "//button[div[div[text()='Following']]]")
        )
        private = bool(
            driver.find_elements(
                By.XPATH, "//*[contains(text(), 'This account is private')]"
            )
        )
        return followed, private

    def get_user_metrics(self, driver) -> Tuple[int, int, int]:
        """Get the number of posts, followers, and following counts."""
        try:
            post_count = self.numerize(
                driver.find_element(
                    By.XPATH, "//div[contains(text(), ' posts')]//span/span"
                ).text
            )
        except NoSuchElementException:
            post_count = 1  # Default value if post count is not found

        try:
            follower_count = self.numerize(
                driver.find_element(
                    By.XPATH, "//a[contains(text(), ' followers')]//span/span"
                ).text
            )
        except NoSuchElementException:
            follower_count = 0  # Default value if follower count is not found

        try:
            following_count = self.numerize(
                driver.find_element(
                    By.XPATH, "//a[contains(text(), ' following')]//span/span"
                ).text
            )
        except NoSuchElementException:
            following_count = 0  # Default value if following count is not found

        return post_count, follower_count, following_count

    def follow_user(
        self, url: str, driver, min_posts: int, max_followers: int, min_followings: int
    ) -> None:
        """Follow a user if they meet the specified criteria."""
        try:
            # Navigate to the user's profile
            driver.get(url)
            sleep(5, 10)

            # Check if the user is already followed or if the account is private
            followed, private = self.check_user_status(driver)
            if followed:
                mprint("User is already followed")
                return

            if private:
                mprint("User is private")
                return

            # Get the user's metrics (posts, followers, following counts)
            post_count, follower_count, following_count = self.get_user_metrics(driver)

            # Check if the user meets the criteria for following
            if not (
                post_count > min_posts
                and follower_count < max_followers
                and following_count > min_followings
            ):
                mprint("User does not meet the criteria for following")
                return

            # Click the "Follow" button
            follow_button = driver.find_element(
                By.XPATH, "//button[div[div[text()='Follow']]]"
            )
            follow_button.click()
            mprint(f"Successfully followed user: {url}")

            # Check if the bot is blocked by Instagram
            if driver.find_elements(
                By.XPATH, "//*[contains(text(), 'Try again later')]"
            ):
                self.is_blocked = True
                speak("Instagram has blocked further actions.")
                mprint("Blocked by Instagram. Automation stopped.")
                return

            # Add the user to the list of followed users
            self.followed_users.append(url)
            sleep(3, 5)

        except Exception as e:
            mprint(
                f"Error in follow_user: {e}"
            )  # Log any errors encountered during following
        finally:
            mprint(f"Execution completed for {url}")

    def log_followed_users(self) -> None:
        """Log all followed users."""
        if self.followed_users:
            mprint("List of followed users:")
            for user in self.followed_users:
                mprint(user)
        else:
            mprint("No users were followed.")


def main():
    """Main function to run the Instagram follow automation."""
    if len(sys.argv) < 6:
        mprint(
            "Please provide username, scroll_count, max_followers, min_followings, and min_posts"
        )
        sys.exit(1)

    username, scroll_count, max_followers, min_followings, min_posts = sys.argv[1:6]
    scroll_count = int(scroll_count)
    max_followers = int(max_followers)
    min_followings = int(min_followings)
    min_posts = int(min_posts)

    bot = InstagramBot()
    driver = None
    try:
        # Initialize the Chrome driver
        driver = chrome()
        speak("Instagram follow automation started!")

        # Find users to follow based on the provided username and scroll count
        users = bot.find_users(username, driver, scroll_count)
        for index, user in enumerate(users):
            if bot.is_blocked:
                break
            sleep(2, 5)
            mprint(f"\nProcessing User #{index + 1}")
            bot.follow_user(user, driver, min_posts, max_followers, min_followings)
    except Exception as e:
        mprint(
            f"Error in Instagram automation: {e}"
        )  # Log any errors during automation
    finally:
        if driver:
            driver.quit()  # Ensure the driver is properly closed
        bot.log_followed_users()  # Log followed users after automation completes
        mprint("Instagram Automation completed\n=========================\n")


if __name__ == "__main__":
    main()
