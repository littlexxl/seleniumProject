import time
import zipfile

from selenium import webdriver

proxy_host = "brd.superproxy.io"
proxy_port = "33335"
proxy_user = "brd-customer-hl_efffca31-zone-freemium"
proxy_pass = "ptnrsv5iq569"

manifest_json = """
{
    "version": "1.0.0",
    "manifest_version": 3,
    "name": "Chrome Proxy Authentication",
    "permissions": [
        "proxy",
        "tabs",
        "unlimitedStorage",
        "storage",
        "webRequest",
        "webRequestAuthProvider"
    ],
    "host_permissions": [
        "<all_urls>"
    ],
    "background": {
        "service_worker": "background.js"
    },
    "minimum_chrome_version": "108"
}
"""

background_js = f"""
var config = {{
    mode: "fixed_servers",
    rules: {{
      singleProxy: {{
        scheme: "http",
        host: "{proxy_host}",
        port: parseInt({proxy_port})
      }},
      bypassList: ["localhost"]
    }}
}};
chrome.proxy.settings.set({{value: config, scope: "regular"}}, function() {{}});
function callbackFn(details) {{
    return {{
        authCredentials: {{
            username: "{proxy_user}",
            password: "{proxy_pass}"
        }}
    }};
}}
chrome.webRequest.onAuthRequired.addListener(
    callbackFn,
    {{urls: ["<all_urls>"]}},
    ["blocking"]
);
"""

with zipfile.ZipFile("proxy_auth_plugin.zip", "w") as zp:
    zp.writestr("manifest.json", manifest_json)
    zp.writestr("background.js", background_js)

chrome_options = webdriver.ChromeOptions()
chrome_options.add_extension("proxy_auth_plugin.zip")

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://httpbin.org/ip")

time.sleep(30)
