import asyncio
import json
import signal
import re
import os
from collections import deque, defaultdict
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

OUTPUT_DIR = "nhs_conditions_dataset"  # Directory for condition JSON files
CACHE_FILE = "cache.json"  # File to store visited links
visited_urls = set()  # Track visited URLs to avoid duplicate scraping
cache_data = defaultdict(lambda: {"sublinks": []})  # Cache structure per condition

# Load cache
if os.path.exists(CACHE_FILE):
    try:
        with open(CACHE_FILE, "r", encoding="utf-8") as file:
            loaded_cache = json.load(file)
            if isinstance(loaded_cache, dict):
                cache_data.update(loaded_cache)
                visited_urls.update(cache_data.keys())  # Add all main condition links
    except (json.JSONDecodeError, ValueError):
        print("⚠️ Cache file is corrupted. Resetting cache.")

# Create output directory if it doesn't exist
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Handle graceful shutdown
def handle_exit(sig, frame):
    print("⚠️  Scraper interrupted! Saving progress...")
    save_cache()
    exit(0)

signal.signal(signal.SIGINT, handle_exit)
signal.signal(signal.SIGTERM, handle_exit)

def save_cache():
    """Save the structured cache file **only after a condition is fully saved**."""
    with open(CACHE_FILE, "w", encoding="utf-8") as file:
        json.dump(dict(cache_data), file, indent=4, ensure_ascii=False)
    print(f"💾 Cache updated. Total conditions stored: {len(cache_data)}")

async def fetch_html(url, page):
    """Fetch HTML content using Playwright."""
    try:
        await page.goto(url, wait_until="domcontentloaded")
        return await page.content()
    except Exception as e:
        print(f"❌ Error fetching {url}: {e}")
        return None

def sanitize_filename(title):
    """Convert condition title to a safe filename (lowercase, no spaces/special chars)."""
    return re.sub(r'[^a-z0-9]+', '_', title.lower().strip())

async def save_condition_to_file(condition_data):
    """Save each condition as a separate JSON file."""
    title_filename = sanitize_filename(condition_data["title"])
    file_path = os.path.join(OUTPUT_DIR, f"{title_filename}.json")
    
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(condition_data, file, indent=4, ensure_ascii=False)
    
    print(f"💾 Saved: {file_path}")

async def scrape_nhs_article(url, page):
    """Scrape an NHS condition article page and extract structured data."""
    if url in visited_urls:
        return None  # Prevent duplicate visits
    visited_urls.add(url)
    
    print(f"🔍 Fetching condition article: {url}")
    
    html = await fetch_html(url, page)
    if not html:
        return None
    
    soup = BeautifulSoup(html, 'html.parser')
    
    # Extract main title
    title = soup.find('h1').text.strip() if soup.find('h1') else "No Title"
    
    # Extract main content sections
    content_sections = []
    current_section = {"title": "Overview", "paragraphs": []}
    
    for elem in soup.find_all(['h2', 'h3', 'p', 'img']):
        if elem.name in ['h2', 'h3']:
            if current_section["paragraphs"]:
                content_sections.append(current_section)
            current_section = {"title": elem.get_text(strip=True), "paragraphs": []}
        elif elem.name == 'p':
            text = elem.get_text(strip=True)
            if text:
                current_section["paragraphs"].append(text)
        elif elem.name == 'img' and elem.get("src"):
            img_tag = str(elem)  # keep the entire <img ...> tag as-is
            current_section["paragraphs"].append(img_tag)

    if current_section["paragraphs"]:
        content_sections.append(current_section)
    
    # **Extract sublinks from NHS structures**
    sublinks = []
    for link in soup.find_all('a', href=True):
        href = link['href'].strip()
        if href.startswith("/conditions/") and not href.startswith("/conditions/#"):
            full_link = f"https://www.nhs.uk{href}"
            if full_link not in visited_urls:
                sublinks.append(full_link)

    # **Only update cache AFTER successfully saving the file**
    article_data = {
        "title": title,
        "url": url,
        "sections": content_sections,
        "sublinks": sublinks if sublinks else None,
        "sublink_articles": []  # Will be filled after crawling
    }

    await save_condition_to_file(article_data)  # Save first
    cache_data[url]["sublinks"] = sublinks if sublinks else []
    save_cache()  # Now update cache

    # **Crawl sublinks AFTER saving the condition**
    sublink_queue = deque(sublinks)
    while sublink_queue:
        sublink = sublink_queue.popleft()
        if sublink not in visited_urls:
            sub_article = await scrape_nhs_article(sublink, page)
            if sub_article:
                article_data["sublink_articles"].append(sub_article)

    # **Update condition file with sublink articles AFTER all sublinks are processed**
    await save_condition_to_file(article_data)
    
    return article_data

async def scrape_nhs_conditions():
    """Scrape all condition articles from NHS Health A-Z using Playwright in A-Z order."""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        print("🔍 Fetching NHS conditions page...")
        html = await fetch_html("https://www.nhs.uk/conditions/", page)
        
        if not html:
            print("❌ No HTML content retrieved from NHS conditions page.")
            await browser.close()
            return []
        
        soup = BeautifulSoup(html, 'html.parser')
        
        # **Extract conditions in strict A-Z order**
        condition_links = deque(
            sorted([
                f"https://www.nhs.uk{link['href']}" for link in soup.select('a[href^="/conditions/"]')
                if not link['href'].startswith("/conditions/#")  # Skip `#A, #B, #C...` links
            ])
        )
        
        print(f"📌 Found {len(condition_links)} condition articles to crawl.")
        
        while condition_links:
            article_url = condition_links.popleft()
            if article_url not in visited_urls:
                await scrape_nhs_article(article_url, page)

        await browser.close()
        save_cache()  # Save cache when done

async def main():
    await scrape_nhs_conditions()
    print(f"✅ Scraping complete. Files saved in `{OUTPUT_DIR}` and `{CACHE_FILE}` updated.")

if __name__ == "__main__":
    asyncio.run(main())
