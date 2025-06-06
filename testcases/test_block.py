import unittest
import time
from selenium import webdriver
from urllib.parse import urlparse

class TestBlock(unittest.TestCase):

    def setUp(self):
        # Replace with the path to your own Chromedriver
        options = webdriver.ChromeOptions()
        options.add_argument(r'--profile-directory=Profile 3')
        options.add_argument(r'--user-data-dir=' + r'C:\Users\test\AppData\Local\Google\Chrome\User Data')
        self.driver = webdriver.Chrome(options=options)

    def test_block(self):
        self.driver.get('https://www.google.com')

        # Wait for the page to load and possibly redirect. You can use WebDriverWait for better waiting mechanism
        time.sleep(10)

        current_url = self.driver.current_url

        parsed = urlparse(current_url)
        self.assertEqual(parsed.scheme, 'extension', f"Unexpected scheme in URL: {current_url}")
        self.assertTrue(parsed.path.endswith('gatewayPage.html'),
                        f"Unexpected path in URL: {current_url}")

        # Check that the page contains an indicator of the block reason
        self.assertIn('Policy', self.driver.page_source)

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
