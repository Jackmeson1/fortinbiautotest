import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from src.utils import read_config
import os

# Create a ChromeOptions instance
chrome_options = Options()


project_root = os.path.abspath(os.path.dirname(__file__))
config_path = os.path.join(project_root, 'config', 'config.yaml')
cfg = read_config(config_path)


chrome_options.add_argument(f"user-data-dir={cfg['browser']['chrome_user_data_dir']}")
chrome_options.add_argument(f"profile-directory={cfg['browser']['chrome_profile_directory']}")

# Launch Chrome using the existing profile (including all installed extensions)
driver = webdriver.Chrome(options=chrome_options)

# Test an action in the browser
driver.get("https://www.dropbox.com")
time.sleep(2)
driver.get("https://www.cisco.com")
time.sleep(200)
# Close the browser
driver.quit()
