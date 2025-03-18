import json
import os
import time
import re
import requests

# Groq AI Translation API Endpoint (Replace with the actual API URL if needed)
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_API_KEY = "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"  # Replace with your actual API key

NHS_DATASET_FOLDER = os.path.abspath(os.path.join(os.getcwd(), "..", "scraper", "nhs_conditions_dataset"))
TRANSLATED_FOLDER = "translated_nhs"

# Ensure output directory exists
os.makedirs(TRANSLATED_FOLDER, exist_ok=True)

def translate_text(text):
    if not text.strip():
        return text  # Skip empty texts
    try:
        response = requests.post(
            GROQ_API_URL,
            headers={"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"},
            json={
                "model": "llama-3.3-70b-versatile",  # Ensure you use the correct model name
                "messages": [
                    {"role": "system", "content": "Translate the following text from English to Albanian without adding additional notes or explanations."},
                    {"role": "user", "content": text}
                ]
            }
        )
        if response.status_code == 200:
            return response.json().get("choices", [{}])[0].get("message", {}).get("content", text).strip()
        else:
            print(f"❌ Translation API Error {response.status_code}: {response.text}")
            return text
    except Exception as e:
        print(f"❌ Translation request failed: {e}")
        return text

def process_url(original_url):
    match = re.search(r"nhs.uk/(.*)", original_url)
    if match:
        shortened_url = match.group(1)  # Extract path after "nhs.uk/"
        return translate_text(shortened_url.replace("-", " ")).replace(" ", "-")  # Translate & format
    return original_url  # Fallback to original URL if no match

def process_sublinks(sublinks):
    translated_sublinks = []
    if not isinstance(sublinks, list):
        return translated_sublinks  # Ensure it's always a list
    
    for sublink in sublinks:
        if isinstance(sublink, dict):  # Ensure sublink is a dictionary
            translated_sublinks.append({
                "title": translate_text(sublink.get("title", "")),
                "url": process_url(sublink.get("url", ""))
            })
    return translated_sublinks

def translate_conditions():
    for filename in os.listdir(NHS_DATASET_FOLDER):
        if filename.endswith(".json"):  # Process only JSON files
            translated_file_path = os.path.join(TRANSLATED_FOLDER, filename)
            if os.path.exists(translated_file_path):
                print(f"⚠️ Skipping {filename}, already translated.")
                continue
            
            file_path = os.path.join(NHS_DATASET_FOLDER, filename)
            
            with open(file_path, "r", encoding="utf-8") as f:
                article = json.load(f)
            
            print(f"🔄 Translating: {article.get('title', 'Unknown Title')}")
            
            translated_title = translate_text(article.get("title", ""))
            translated_content = translate_text(article.get("content", ""))  # Handle missing content
            translated_url = process_url(article.get("url", ""))
            translated_sublinks = process_sublinks(article.get("sublinks", []))

            translated_article = {
                "title": translated_title,
                "url": translated_url,
                "content": translated_content,
                "sublinks": translated_sublinks
            }
            
            with open(translated_file_path, "w", encoding="utf-8") as f:
                json.dump(translated_article, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Translated and saved: {filename}")
            
            time.sleep(1)  # Prevent issues with too many file writes

if __name__ == "__main__":
    translate_conditions()
