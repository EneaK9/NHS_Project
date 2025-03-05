import time
import json
from playwright.sync_api import sync_playwright

BASE_URL = "https://www.nhs.uk/conditions/"

def scrape_conditions():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Set headless=True to run in background
        page = browser.new_page()

        print("🔄 Scraping NHS conditions...")
        page.goto(BASE_URL, wait_until="domcontentloaded")

        # ✅ Ensure elements are loaded before scraping
        page.wait_for_selector("a.nhsuk-link, a.nhsuk-card__link", timeout=15000)

        # ✅ Extract all condition links
        conditions = page.evaluate('''() => {
            return Array.from(document.querySelectorAll("a.nhsuk-link, a.nhsuk-card__link"))
                .map(link => ({
                    title: link.innerText.trim(),
                    url: link.href.startsWith("http") ? link.href : `https://www.nhs.uk${link.getAttribute("href")}`
                }));
        }''')

        print(f"✅ Found {len(conditions)} conditions!")

        if len(conditions) == 0:
            print("❌ No conditions found. Check if the page structure has changed.")
        else:
            detailed_articles = []

            for condition in conditions:
                print(f"📖 Scraping: {condition['title']} ({condition['url']})")
                page.goto(condition['url'], wait_until="domcontentloaded")

                try:
                    content = page.locator("div.nhsuk-main-wrapper").inner_text()
                except:
                    content = "❌ No content found"

                detailed_articles.append({
                    "title": condition["title"],
                    "url": condition["url"],
                    "content": content
                })

                time.sleep(2)  # Prevent getting blocked

            with open("nhs_conditions.json", "w", encoding="utf-8") as f:
                json.dump(detailed_articles, f, indent=2)

            print("✅ Conditions scraped and saved!")

        browser.close()

if __name__ == "__main__":
    scrape_conditions()
