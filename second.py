from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


# formulate the proxy url with authentication
proxy_url = f"http://brd-customer-hl_efffca31-zone-freemium:ptnrsv5iq569@brd.superproxy.io:33335"

# set selenium-wire options to use the proxy
seleniumwire_options = {
    "proxy": {
        "http": proxy_url,
        "https": proxy_url
    },
}

# set Chrome options to run in headless mode
options = Options()
#options.add_argument("--headless=new")

# initialize the Chrome driver with service, selenium-wire options, and chrome options
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    seleniumwire_options=seleniumwire_options,
    options=options
)

# navigate to the target webpage
driver.get("https://httpbin.io/ip")

# print the body content of the target webpage
print(driver.find_element(By.TAG_NAME, "body").text)

# release the resources and close the browser
driver.quit()