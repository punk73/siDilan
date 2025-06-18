from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import json
from dotenv import load_dotenv
import os

load_dotenv('.env', override=True)
# Set your real chromedriver path
CHROMEDRIVER_PATH = os.getenv('CHROMEDRIVER_PATH')

# Set up options
options = Options()
options.add_argument('--headless')  # Optional: run without opening browser window
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')

# Set up Selenium Wire with Chrome
service = Service(CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service, options=options)

results = {}

try:
    base_url = "https://cctv.purwakartakab.go.id/"
    driver.get(base_url)

    time.sleep(3)  # Wait for dynamic content to load

    soup = BeautifulSoup(driver.page_source, "html.parser")

    grid = soup.select_one('.grid')
    links = grid.find_all("a", href=True) if grid else []

    print(f"Found {len(links)} links.")

    for a in links:
        title = a.get("title", "no-title").strip()
        href = a['href']
        full_link = href if href.startswith("http") else base_url.rstrip("/") + href

        print(f"\n🔗 Visiting: {full_link} | Title: {title}")
        driver.get(full_link)

        time.sleep(3)  # Wait for network requests to load

        # Access captured requests
        m3u8_url = None
        for request in driver.requests:
            if request.response and ".m3u8" in request.url:
                m3u8_url = request.url
                break

        if m3u8_url:
            print(f"✅ Found m3u8: {m3u8_url}")
            results[title] = m3u8_url
        else:
            print("❌ No m3u8 found.")

finally:
    driver.quit()

# Save to JSON
with open("scrap_result.json", "w") as f:
    json.dump(results, f, indent=4)

print("\n✅ All done. Results saved to data.json.")