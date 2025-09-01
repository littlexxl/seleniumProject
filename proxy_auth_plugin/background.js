
chrome.proxy.settings.set(
  {value: {
    mode: "fixed_servers",
    rules: {
      singleProxy: {
        scheme: "http",
        host: "brd.superproxy.io",
        port: parseInt(33335)
      },
      bypassList: ["localhost"]
    }
  }, scope: "regular"},
  function() {}
);

chrome.webRequest.onAuthRequired.addListener(
  (details) => {
    return {authCredentials: {username: "brd-customer-hl_efffca31-zone-freemium", password: "ptnrsv5iq569"}};
  },
  {urls: ["<all_urls>"]},
  ["blocking"]
);
