
import os
import unittest

import time

import unittest


import psutil  # You'll need to install this package: pip install psutil

from src.utils import read_config



class TestBrowserIsolation(unittest.TestCase):
    def setUp(self):
        """Initialize WebDriver before each test case."""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.abspath(os.path.join(current_dir, '..'))
        config_path = os.path.join(project_root, 'config', 'config.yaml')
        config = read_config(config_path)


        option = webdriver.ChromeOptions()
        option.add_argument(f"--user-data-dir={config['browser']['chrome_user_data_dir']}")
        option.add_argument(f"--profile-directory={config['browser']['chrome_profile_directory']}")

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

            for proc in psutil.process_iter(["name"]):
                print(proc.info["name"].lower())
                if "rdp" in proc.info["name"].lower():
                    rdp_exist = True
                    break

            self.assertTrue(rdp_exist, "RDP process does not exist.")

        except Exception as e:
            # Mark the test as failed if any exception occurs
            self.fail(f"Test failed due to {e}")


if __name__ == "__main__":
    unittest.main()
