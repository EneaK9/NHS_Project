import asyncio
import json
import signal
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

OUTPUT_FILE = "nhs_conditions.json"
scraped_articles = []  # Store scraped data live

# Handle graceful shutdown to save progress
def handle_exit(sig, frame):
    print("⚠️  Scraper interrupted! Saving progress...")
    write_to_file(scraped_articles)
    exit(0)

# Register signal handlers for safe exit
signal.signal(signal.SIGINT, handle_exit)
signal.signal(signal.SIGTERM, handle_exit)

async def save_progress():
    """Save progress live while scraping in a non-blocking way."""
    await asyncio.to_thread(write_to_file, scraped_articles)

def write_to_file(data):
    """Write data to a file immediately."""
    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
    print(f"💾 Live Save: {len(data)} articles stored.")

async def fetch_html(url, page):
    """Fetch HTML content using Playwright."""
    try:
        await page.goto(url, wait_until="domcontentloaded")
        return await page.content()
    except Exception as e:
        print(f"❌ Error fetching {url}: {e}")
        return None

async def scrape_nhs_article(url, page):
    """Scrape an NHS condition article page and extract structured data."""
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
    
    for elem in soup.find_all(['h2', 'h3', 'p']):
        if elem.name in ['h2', 'h3']:
            if current_section["paragraphs"]:
                content_sections.append(current_section)
            current_section = {"title": elem.get_text(strip=True), "paragraphs": []}
        elif elem.name == 'p':
            text = elem.get_text(strip=True)
            if text:
                current_section["paragraphs"].append(text)
    
    if current_section["paragraphs"]:
        content_sections.append(current_section)
    
    # Extract internal links
    sublinks = []
    for link in soup.find_all('a', href=True):
        href = link['href']
        if href.startswith('/conditions/'):
            sublinks.append({"title": link.text.strip(), "link": f"https://www.nhs.uk{href}"})
    
    return {
        "title": title,
        "url": url,
        "sections": content_sections,
        "sublinks": sublinks
    }

async def scrape_nhs_conditions():
    """Scrape all condition articles from NHS Health A-Z using Playwright."""
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
        
        condition_links = [f"https://www.nhs.uk{link['href']}" for link in soup.select('a[href^="/conditions/"][href!="/conditions/"]')]
        print(f"📌 Found {len(condition_links)} condition articles to crawl.")
        
        for article_url in condition_links:
            article_data = await scrape_nhs_article(article_url, page)
            if article_data:
                scraped_articles.append(article_data)
                await save_progress()  # Save live progress asynchronously
        
        await browser.close()
        return scraped_articles

async def main():
    await scrape_nhs_conditions()
    write_to_file(scraped_articles)  # Final save
    print(f"✅ Scraping complete. Data saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    asyncio.run(main())