import json
import time
from crawl4ai import CrawlerHub

BASE_URL = "https://www.nhs.uk/conditions/"
crawler = CrawlerHub()

def scrape_conditions():
    print("🔄 Scraping all NHS conditions and details...")

    # ✅ Step 1: Get the main NHS conditions page
    page = crawler.fetch_page(BASE_URL)  # Try fetching differently


    # ✅ Step 2: Find all condition links
    condition_links = page.find_all("a.nhsuk-card__link, a.nhsuk-list-panel__link")

    articles = []
    for link in condition_links:
        title = link.text.strip()
        url = link["href"] if link["href"].startswith("http") else BASE_URL + link["href"]

        print(f"📌 Found: {title} -> {url}")
        articles.append({"title": title, "url": url})

    # ✅ Save condition links
    with open("nhs_conditions.json", "w", encoding="utf-8") as f:
        json.dump(articles, f, indent=2)

    print(f"✅ {len(articles)} condition links scraped!")
    return articles

def scrape_condition_details(articles):
    print("🔄 Scraping all condition details...")

    detailed_articles = []

    for article in articles:
        print(f"📖 Scraping: {article['title']} ({article['url']})")
        page = crawler.get(article["url"])

        # ✅ Extract the full condition text
        content = page.find("div.nhsuk-main-wrapper").text.strip()

        # ✅ Extract any internal NHS links within the condition page
        internal_links = [link["href"] for link in page.find_all("a") if "nhs.uk" in link["href"]]

        detailed_articles.append({
            "title": article["title"],
            "url": article["url"],
            "content": content,
            "internal_links": internal_links
        })
        
        time.sleep(2)  # Prevent request blocking

    # ✅ Save full condition details
    with open("nhs_detailed_articles.json", "w", encoding="utf-8") as f:
        json.dump(detailed_articles, f, indent=2)

    print(f"✅ {len(detailed_articles)} condition pages scraped with full text!")
    return detailed_articles

if __name__ == "__main__":
    articles = scrape_conditions()
    scrape_condition_details(articles)
