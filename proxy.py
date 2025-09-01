import time
import zipfile
from selenium import webdriver

# Proxy details
PROXY_HOST = "brd.superproxy.io"
PROXY_PORT = "33335"
PROXY_USER = "brd-customer-hl_efffca31-zone-freemium"
PROXY_PASS = "ptnrsv5iq569"

# Manifest V3
manifest_json = """
{
  "name": "Proxy Auth Extension",
  "version": "1.0.0",
  "manifest_version": 3,
  "permissions": [
    "proxy",
    "storage",
    "webRequest",
    "webRequestAuthProvider",
    "webRequestBlocking"
  ],
  "background": {
    "service_worker": "background.js"
  },
  "host_permissions": [
    "<all_urls>"
  ]
}
"""

background_js = f"""
chrome.proxy.settings.set(
  {{value: {{
    mode: "fixed_servers",
    rules: {{
      singleProxy: {{
        scheme: "http",
        host: "{PROXY_HOST}",
        port: parseInt({PROXY_PORT})
      }},
      bypassList: ["localhost"]
    }}
  }}, scope: "regular"}},
  function() {{}}
);

chrome.webRequest.onAuthRequired.addListener(
  (details) => {{
    return {{authCredentials: {{username: "{PROXY_USER}", password: "{PROXY_PASS}"}}}};
  }},
  {{urls: ["<all_urls>"]}},
  ["blocking"]
);
"""

pluginfile = "proxy_auth_plugin.zip"
with zipfile.ZipFile(pluginfile, 'w') as zp:
    zp.writestr("manifest.json", manifest_json)
    zp.writestr("background.js", background_js)

options = webdriver.ChromeOptions()
options.add_extension(pluginfile)

driver = webdriver.Chrome(options=options)
driver.get("https://httpbin.org/ip")

time.sleep(30)