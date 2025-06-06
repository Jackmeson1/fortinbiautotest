import os
import unittest
from selenium import webdriver
import time
from src.utils import read_config

class TestBlock(unittest.TestCase):

    def setUp(self):
        # Replace with the path to your own Chromedriver
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.abspath(os.path.join(current_dir, '..'))
        config_path = os.path.join(project_root, 'config', 'config.yaml')
        config = read_config(config_path)

        options = webdriver.ChromeOptions()
        options.add_argument(f"--profile-directory={config['browser']['chrome_profile_directory']}")
        options.add_argument(f"--user-data-dir={config['browser']['chrome_user_data_dir']}")
        self.driver = webdriver.Chrome(options=options)

    def test_block(self):
        self.driver.get('https://www.google.com')

        # Wait for the page to load and possibly redirect. You can use WebDriverWait for better waiting mechanism
        time.sleep(10)

        current_url = self.driver.current_url
        expected_url = 'extension://gdiglidgaoimfbhfkelnlgnpghggbmbb/res/html/gatewayPage.html?action=2&reason=Policy&requestId=148&url=https%253A%252F%252Fwww.google.com%252F'

        self.assertEqual(current_url, expected_url, f"Expected URL: {expected_url}, Current URL: {current_url}")

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
