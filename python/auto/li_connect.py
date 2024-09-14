import os
import sys

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

# Adjusting the sys.path to include the parent directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from tts import speak
from driver import chrome
from utils import sleep, mprint


class LinkedInConnector:
    def __init__(self):
        self.driver = None
        self.current_page = 1
        self.current_user = 1

    def li_connect(self, max_pages: int = 1, keywords: str = "") -> None:
        """Connect to LinkedIn profiles based on the search keywords."""
        try:
            for _ in range(max_pages):
                # Load the LinkedIn search results page
                self.driver.get(
                    f"https://www.linkedin.com/search/results/people/?keywords={keywords}&page={self.current_page}"
                )

                # Find all "Connect" buttons on the page
                try:
                    connect_btns = self.driver.find_elements(
                        By.XPATH, '//button[span[text()="Connect"]]'
                    )
                except NoSuchElementException:
                    connect_btns = None

                if not connect_btns:
                    mprint(
                        "No 'Connect' buttons found. Make sure the page is loaded correctly."
                    )
                    break

                # Click on each "Connect" button
                for btn in connect_btns:
                    mprint(f"Processing User #{self.current_user}")
                    btn.click()
                    sleep(1.5, 3)

                    # Click the "Send without a note" button
                    self.driver.find_element(
                        By.XPATH, '//button[span[text()="Send without a note"]]'
                    ).click()
                    self.current_user += 1
                    sleep(2, 5)

                # Move to the next page
                self.current_page += 1

        except Exception as e:
            mprint(f"Error in li_connect: {e}")
        finally:
            mprint("LinkedIn Automation Completed!\n=========================\n")


def main():
    """Main function to execute the LinkedIn connection automation."""
    if len(sys.argv) < 3:
        mprint("Usage: script.py <keywords> <pages>")
        sys.exit(1)

    keywords = sys.argv[1]
    pages = int(sys.argv[2])

    connector = LinkedInConnector()
    try:
        connector.driver = chrome()
        speak("Starting LinkedIn connection automation...")
        connector.li_connect(max_pages=pages, keywords=keywords)
    except Exception as e:
        mprint(f"Error in LinkedIn automation: {e}")
        sys.exit(1)
    finally:
        if connector.driver:
            connector.driver.quit()  # Ensure the driver is properly closed
        mprint("LinkedIn Automation completed\n=========================\n")


if __name__ == "__main__":
    main()
