import unittest
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
import psutil  # You'll need to install this package: pip install psutil


class TestBrowserIsolation(unittest.TestCase):
    def setUp(self):
        """Initialize WebDriver before each test case."""
        option = webdriver.ChromeOptions()

        option.add_argument(r'--user-data-dir=' + r'C:\Users\test\AppData\Local\Google\Chrome\User Data')
        option.add_argument(r'--profile-directory=Profile 3')
        self.driver = webdriver.Chrome(options=option)

    def tearDown(self):
        """Clean up resources after each test case."""

        self.driver.quit()
        # os.system('taskkill /F /IM chrome.exe')
        # os.system('wsl -d fortinbi-isolator kill_chrome.sh')

    def test_browser_isolation(self):
        """Test if Chrome can open a website and if RDP process exists."""

        try:
            # Navigate to YouTube Canada site
            self.driver.get(r"https:\\www.dropbox.com")

            WebDriverWait(self.driver, 20).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )

            # Assert if an RDP process exists in Windows processes
            rdp_exist = False

            for proc in psutil.process_iter(['name']):
                print(proc.info['name'].lower())
                if 'rdp' in proc.info['name'].lower():
                    rdp_exist = True
                    break

            self.assertTrue(rdp_exist, "RDP process does not exist.")

        except Exception as e:
            # Mark the test as failed if any exception occurs
            self.fail(f"Test failed due to {e}")


if __name__ == '__main__':
    unittest.main()
