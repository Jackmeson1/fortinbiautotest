import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from src.utils import read_config
import os

# 创建 ChromeOptions 实例
chrome_options = Options()

project_root = os.path.abspath(os.path.dirname(__file__))
config_path = os.path.join(project_root, 'config', 'config.yaml')
cfg = read_config(config_path)

chrome_options.add_argument(f"user-data-dir={cfg['browser']['chrome_user_data_dir']}")
chrome_options.add_argument(f"profile-directory={cfg['browser']['chrome_profile_directory']}")

# 启动 Chrome 浏览器，并加载现有配置文件（包括所有已安装的插件）
driver = webdriver.Chrome(options=chrome_options)

# 测试浏览器中的某个操作
driver.get("https://www.dropbox.com")
time.sleep(2)
driver.get("https://www.cisco.com")
time.sleep(200)
# 关闭浏览器
driver.quit()
