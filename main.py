from selenium import webdriver
from selenium.webdriver.common.by import By
import math, time, csv, yaml

driver = webdriver.Chrome()
driver.get("https://defillama.com/chains")

def run_scraping():
    document_height = driver.execute_script("return document.body.scrollHeight")
    scroll_limit = 500
    times_to_scroll = math.ceil(document_height / scroll_limit)
    biden_time = 0.2

    # keeping data
    data = []
    seen_ids = set()  # keep track of IDs to avoid duplicates

    for i in range(times_to_scroll):
        # Scroll down by 500 pixels
        driver.execute_script("window.scrollBy(0, "+str(scroll_limit)+");")
        # Wait a bit for content to load
        whole_table = driver.find_elements(By.CSS_SELECTOR, "#table-wrapper > div:nth-child(3)")

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

    print("✅ Finished slow scroll to end of page")

    with open("chains_data.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Name", "Protocols", "TVL"])
        writer.writerows(data)

    print(f"✅ Scraped {len(data)} rows. Data saved to chains_data.csv")

run_scraping()

driver.quit()
