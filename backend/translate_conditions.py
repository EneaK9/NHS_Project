import json
import requests
import time

TRANSLATION_API = "http://localhost:5000/translate"

def translate_text(text):
    try:
        response = requests.post(TRANSLATION_API, json={"text": text})
        return response.json()["translated"]
    except Exception as e:
        print(f"❌ Translation failed: {e}")
        return text  # Fallback to original text

def translate_articles():
    with open("scraper/nhs_conditions.json", "r", encoding="utf-8") as f:
        articles = json.load(f)

    translated_articles = []
    
    for article in articles:
        print(f"🔄 Translating: {article['title']}")
        
        translated_title = translate_text(article["title"])
        translated_content = translate_text(article["content"])

        translated_articles.append({
            "title": article["title"],
            "translated_title": translated_title,
            "url": article["url"],
            "content": article["content"],
            "translated_content": translated_content
        })
        
        time.sleep(1)  # Prevent API rate limits

    with open("backend/translated_articles.json", "w", encoding="utf-8") as f:
        json.dump(translated_articles, f, indent=2)

    print("✅ All articles translated and saved!")

if __name__ == "__main__":
    translate_articles()
