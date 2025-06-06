import unittest
from selenium import webdriver
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class TestBlock(unittest.TestCase):

    def setUp(self):
        # Replace with the path to your own Chromedriver
        options = webdriver.ChromeOptions()
        options.add_argument(r'--profile-directory=Profile 3')
        options.add_argument(r'--user-data-dir=' + r'C:\Users\test\AppData\Local\Google\Chrome\User Data')
        self.driver = webdriver.Chrome(options=options)

    def test_block(self):
        self.driver.get('https://www.google.com')

        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        current_url = self.driver.current_url
        expected_url = 'extension://gdiglidgaoimfbhfkelnlgnpghggbmbb/res/html/gatewayPage.html?action=2&reason=Policy&requestId=148&url=https%253A%252F%252Fwww.google.com%252F'

        self.assertEqual(current_url, expected_url, f"Expected URL: {expected_url}, Current URL: {current_url}")

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
