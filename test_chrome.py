import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# 创建 ChromeOptions 实例
chrome_options = Options()

# 设置用户配置文件路径（例如 Windows 系统的默认 Profile 路径）
chrome_options.add_argument(r"user-data-dir=C:\Users\test\AppData\Local\Google\Chrome\User Data")

# 如果你有多个配置文件，可以指定特定的 Profile 文件夹
chrome_options.add_argument("profile-directory=Profile 1")

# 启动 Chrome 浏览器，并加载现有配置文件（包括所有已安装的插件）
driver = webdriver.Chrome(options=chrome_options)

# 测试浏览器中的某个操作
driver.get("https://www.dropbox.com")
time.sleep(2)
driver.get("https://www.cisco.com")
time.sleep(200)
# 关闭浏览器
driver.quit()
