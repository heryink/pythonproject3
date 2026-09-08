import os
import time
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import requests

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configuration Settings
START_URL = "https://platform.claude.com/docs/en/home"
BASE_DOMAIN = "platform.claude.com"
OUTPUT_DIR = r"C:\Users\USER\Documents\AI_Docs\Anthropic_Claude"

# Create output folders for offline files and assets
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(os.path.join(OUTPUT_DIR, "assets"), exist_ok=True)

# Headless Chrome Settings (runs silently in the background)
chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--log-level=3")

driver = webdriver.Chrome(options=chrome_options)

# Trackers to handle link navigation and prevent infinite loops
visited_urls = set()
url_queue = [START_URL]


def clean_filename(url):
    """Converts a web URL path into a safe, organized local filename."""
    path = urlparse(url).path
    if path.endswith('/') or path.endswith('/home'):
        return "index.html"
    return path.strip('/').replace('/', '_') + ".html"


def download_asset(asset_url):
    """Downloads images and CSS stylesheets locally to preserve site styling."""
    try:
        parsed_asset = urlparse(asset_url)
        filename = os.path.basename(parsed_asset.path)
        if not filename:
            return asset_url

        local_path = os.path.join(OUTPUT_DIR, "assets", filename)
        relative_path = f"assets/{filename}"

        # Cache protection: only download if the file doesn't exist locally
        if not os.path.exists(local_path):
            response = requests.get(asset_url, timeout=10)
            if response.status_code == 200:
                with open(local_path, 'wb') as f:
                    f.write(response.content)

        return relative_path
    except Exception:
        return asset_url  # Web fallback if download fails


print("🚀 Starting Anthropic Documentation Downloader...")

try:
    while url_queue:
        current_url = url_queue.pop(0)

        if current_url in visited_urls:
            continue

        print(f"📄 Scraping Page: {current_url}")
        visited_urls.add(current_url)

        # Load page in headless browser
        driver.get(current_url)

        try:
            # Wait up to 10 seconds for the main content frame to render via JavaScript
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "main"))
            )
            time.sleep(1.5)  # Short delay to allow code snippets to finish parsing
        except Exception:
            print(f"⚠️ Warning: Timeout on {current_url}. Scraping current fallback state.")

        # Parse fully rendered page source code
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Link Discovery and Rewriting Loop
        for link in soup.find_all('a', href=True):
            href = link['href']
            absolute_url = urljoin(current_url, href).split('#')[0].rstrip('/')

            # Keep crawler restricted inside the official documentation boundaries
            if BASE_DOMAIN in absolute_url and "/docs/" in absolute_url:
                if absolute_url not in visited_urls and absolute_url not in url_queue:
                    url_queue.append(absolute_url)

                # Rewrite link to point to the local file instead of the web
                link['href'] = clean_filename(absolute_url)

        # Localize CSS styles
        for link_tag in soup.find_all('link', rel='stylesheet', href=True):
            abs_css = urljoin(current_url, link_tag['href'])
            link_tag['href'] = download_asset(abs_css)

        # Localize image components
        for img_tag in soup.find_all('img', src=True):
            abs_img = urljoin(current_url, img_tag['src'])
            img_tag['src'] = download_asset(abs_img)

        # Write final modified HTML layout directly to your Documents folder
        output_filename = clean_filename(current_url)
        output_file_path = os.path.join(OUTPUT_DIR, output_filename)

        with open(output_file_path, 'w', encoding='utf-8') as f:
            f.write(str(soup))

    print(f"\n🎉 Download Completed! Files saved to: {OUTPUT_DIR}")
    print("💡 Double-click 'index.html' inside that folder to start reading completely offline.")

finally:
    # Safely close down background browser threads to free up system memory
    driver.quit()