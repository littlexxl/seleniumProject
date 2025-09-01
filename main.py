from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import (
    WebDriverException,
    NoSuchElementException
)

import math, time, csv, yaml, sys, logging
from logging.handlers import RotatingFileHandler

# ----------------------------
# Load configuration
# ----------------------------
try:
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)
except Exception as e:
    print(f"Could not load config.yaml: {e}")
    sys.exit(1)

SCRAPE_INTERVAL = config.get("update_time") * 60

# ----------------------------
# Logging Configuration
# ----------------------------
log_formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")

# Log to file (rotating so it doesn’t grow forever)
file_handler = RotatingFileHandler(
    "scraper.log", maxBytes=5*1024*1024, backupCount=3, encoding="utf-8"
)
file_handler.setFormatter(log_formatter)
file_handler.setLevel(logging.INFO)
# Main logger setup (NO console handler)
logging.basicConfig(level=logging.DEBUG, handlers=[file_handler])
logger = logging.getLogger("Scraper")
# ----------------------------


# Set Chrome options
# Replace with your working proxy
proxy = "brd-customer-hl_efffca31-zone-freemium:ptnrsv5iq569@brd.superproxy.io:33335"

# Selenium Wire options for the proxy
seleniumwire_options = {
    'proxy': {
      #  'http': f'http://{proxy}',
        'https': f'https://{proxy}',
        'no_proxy': 'localhost,127.0.0.1'  # optional
    }
}

# Chrome options
chrome_options = Options()

def run_scraping():
    try:
        driver = webdriver.Chrome(
            options=chrome_options,
            seleniumwire_options=seleniumwire_options
        )
        driver.get("https://defillama.com/chains")
    except WebDriverException as e:
        logger.error(f"Browser error: {e}")
        sys.exit(1)

    try:
        document_height = driver.execute_script("return document.body.scrollHeight")
    except Exception as e:
        logger.error(f"Could not get page height: {e}")
        driver.quit()
        sys.exit(1)

    scroll_limit = 500
    times_to_scroll = math.ceil(document_height / scroll_limit)
    biden_time = 0.2 # time_to_sleep

    # keeping data
    data = []
    seen_ids = set()  # keep track of IDs to avoid duplicates
    try:
        for i in range(times_to_scroll):
            # Scroll down by 500 pixels

            try:
                driver.execute_script(f"window.scrollBy(0, {scroll_limit});")
            except WebDriverException as e:
                logger.error(f"Scroll failed: {e}")
                break

            # Wait a bit for content to load
            try:
                whole_table = driver.find_elements(By.CSS_SELECTOR, "#table-wrapper > div:nth-child(3)")
            except NoSuchElementException:
                logger.error("Table not found, continuing...")
                continue

            for iterate in whole_table:
                try:
                    grid_rows = iterate.find_elements(By.CSS_SELECTOR, "div[style*='grid-template-columns']")

                    for row in grid_rows:
                        try:
                            cells = row.find_elements(By.CSS_SELECTOR, "div[data-chainpage='true']")
                            if len(cells) < 3:
                                continue  # skip incomplete rows

                            # First column: number + name
                            first_col = cells[0]

                            number = first_col.find_element(By.CSS_SELECTOR, "span.shrink-0").text.strip()
                            name = first_col.find_element(By.CSS_SELECTOR, "a").text.strip()

                            # Skip if this ID is already processed
                            if number in seen_ids:
                                continue

                            protocols = cells[1].text.strip()
                            tvl = cells[2].text.strip()

                            data.append([name, protocols, tvl])
                            seen_ids.add(number)
                        except Exception as e:
                            continue
                    time.sleep(biden_time)
                except Exception as e:
                    continue


    except Exception as e:
        logger.error(f"Unexpected error while scraping: {e}")
    finally:
        driver.quit()

    with open("chains_data.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Name", "Protocols", "TVL"])
        writer.writerows(data)

    logger.info(f"Scraped {len(data)} rows. Data saved to chains_data.csv")


# ----------------------------
# Main Loop
# ----------------------------
if __name__ == "__main__":
    logger.info(f"Scraper started.")
    while True:
        run_scraping()
        logger.info(f"Waiting {SCRAPE_INTERVAL/60} minutes until next scrape...")
        time.sleep(SCRAPE_INTERVAL)