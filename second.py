from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    WebDriverException,
    NoSuchElementException,
    StaleElementReferenceException,
)
import math, time, csv, yaml, sys, os

def run_scraping():
    try:
        driver = webdriver.Chrome()
        driver.get("https://defillama.com/chains")
    except WebDriverException as e:
        print(f"Browser error: {e}")
        sys.exit(1)

    try:
        document_height = driver.execute_script("return document.body.scrollHeight")
    except Exception as e:
        print(f"Could not get page height: {e}")
        driver.quit()
        sys.exit(1)

    scroll_limit = 500
    times_to_scroll = math.ceil(document_height / scroll_limit)
    biden_time = 0.2

    data = []
    seen_ids = set()

    try:
        for i in range(times_to_scroll):
            try:
                driver.execute_script(f"window.scrollBy(0, {scroll_limit});")
            except WebDriverException as e:
                print(f"Scroll failed: {e}")
                break

            try:
                main_table = driver.find_elements(By.CSS_SELECTOR, "#table-wrapper > div:nth-child(3)")
            except NoSuchElementException:
                print("Table not found, continuing...")
                continue

            for iterate in main_table:
                try:
                    grid_rows = iterate.find_elements(By.CSS_SELECTOR, "div[style*='grid-template-columns']")
                except StaleElementReferenceException:
                    print("Table changed during scraping, skipping iteration...")
                    continue

                for row in grid_rows:
                    try:
                        cells = row.find_elements(By.CSS_SELECTOR, "div[data-chainpage='true']")
                        if len(cells) < 3:
                            continue # skip incomplete rows

                        first_col = cells[0]
                        number = first_col.find_element(By.CSS_SELECTOR, "span.shrink-0").text.strip()
                        name = first_col.find_element(By.CSS_SELECTOR, "a").text.strip()

                        if number in seen_ids:
                            continue

                        protocols = cells[1].text.strip()
                        tvl = cells[2].text.strip()

                        data.append([name, protocols, tvl])
                        seen_ids.add(number)

                    except Exception as e:
                        print(f"Error parsing row: {e}")
                        continue

            time.sleep(biden_time)

    except Exception as e:
        print(f"Unexpected error while scraping: {e}")
    finally:
        driver.quit()

    if not data:
        print("No data scraped. Exiting...")
        return

    try:
        with open("chains_data.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Name", "Protocols", "TVL"])
            writer.writerows(data)
        print(f"✅ Scraped {len(data)} rows. Data saved to chains_data.csv")
    except OSError as e:
        print(f"❌ File write error: {e}")


if __name__ == "__main__":
    run_scraping()
