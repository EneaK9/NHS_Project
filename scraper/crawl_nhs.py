import asyncio
import json
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
from crawl4ai.deep_crawling import BFSDeepCrawlStrategy
from crawl4ai.content_scraping_strategy import LXMLWebScrapingStrategy
from bs4 import BeautifulSoup

OUTPUT_FILE = "nhs_test_single.json"

async def scrape_nhs():
    config = CrawlerRunConfig(
        deep_crawl_strategy=BFSDeepCrawlStrategy(
            max_depth=1,
            include_external=False
        ),
        scraping_strategy=LXMLWebScrapingStrategy(),
        verbose=True
    )

    async with AsyncWebCrawler() as crawler:
        print("🔄 Crawling single NHS condition...")
        results = await crawler.arun("https://www.nhs.uk/conditions/abdominal-aortic-aneurysm/", 
                                   config=config, 
                                   max_requests=1)

        if results:
            result = results[0]
            soup = BeautifulSoup(result.html, 'html.parser')
            
            main_content = soup.find('main', id='maincontent')
            
            if main_content:
                # Organize content by sections
                content_sections = []
                current_section = {"title": "Overview", "paragraphs": []}
                
                for elem in main_content.find_all(['h2', 'h3', 'p']):
                    if elem.name in ['h2', 'h3']:
                        # Save previous section if it has content
                        if current_section["paragraphs"]:
                            content_sections.append(current_section)
                        # Start new section
                        current_section = {
                            "title": elem.get_text(strip=True),
                            "paragraphs": []
                        }
                    elif elem.name == 'p':
                        text = elem.get_text(strip=True)
                        if text:  # Only add non-empty paragraphs
                            current_section["paragraphs"].append(text)
                
                # Add the last section
                if current_section["paragraphs"]:
                    content_sections.append(current_section)
                
                article = {
                    "title": result.metadata.get("title", "No Title").split(" - ")[0],  # Remove "- NHS" suffix
                    "url": result.url,
                    "sections": content_sections
                }
            else:
                article = {
                    "title": result.metadata.get("title", "No Title"),
                    "url": result.url,
                    "sections": [{"title": "Error", "paragraphs": ["No content found"]}]
                }

            print(f"📖 Saving article: {article['title']}")
            with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
                json.dump(article, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Test article saved with {len(article['sections'])} sections")

if __name__ == "__main__":
    asyncio.run(scrape_nhs())
