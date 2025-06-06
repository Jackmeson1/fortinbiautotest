
import os

import unittest

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
        self.driver.get("https://www.google.com")

        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

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
