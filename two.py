import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Path to your unpacked extension folder
extension_folder = "proxy_auth_plugin/"

options = Options()
options.add_argument(f"--load-extension={extension_folder}")

driver = webdriver.Chrome(options=options)

driver.get("https://httpbin.org/ip")

time.sleep(30)
