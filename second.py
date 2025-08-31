import math

from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()
driver.get("https://defillama.com/chains")
time.sleep(5)  # wait for React to render table

def run_scrolling():
    document_height = driver.execute_script("return document.body.scrollHeight")
    scroll_limit = 500
    times_to_scroll = math.ceil(document_height / scroll_limit)

    for i in range(times_to_scroll):
        # Scroll down by 500 pixels
        driver.execute_script("window.scrollBy(0, "+str(scroll_limit)+");")
        # Wait a bit for content to load
        time.sleep(0.2)

        # Get parent grid rows
        grid_rows = driver.find_elements(By.CSS_SELECTOR, "div[style*='grid-template-columns']")

        for row in grid_rows:
            try:
                # Columns of the row
                cells = row.find_elements(By.CSS_SELECTOR, "div[data-chainpage='true']")

                first_col = cells[0]

                # Row number
                number = first_col.find_element(By.CSS_SELECTOR, "span.shrink-0").text.strip()

                # Name (link)
                name = first_col.find_element(By.CSS_SELECTOR, "a").text.strip()

                # Protocols and TVL
                protocols = cells[1].text.strip()
                tvl = cells[2].text.strip()

                print(f"{number} | {name} | {protocols} | {tvl}")

            except Exception as e:
                continue
    print("✅ Finished slow scroll to end of page")


run_scrolling()

driver.quit()
