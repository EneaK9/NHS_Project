import json
import os
import time
import re
import requests
import signal
import sys

# DeepSeek API Configuration
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"
DEEPSEEK_API_KEY = "sk-2d15e5aabdc34727bf241bcff5352018"

# Paths
NHS_DATASET_FOLDER = os.path.abspath(os.path.join(os.getcwd(), "..", "scraper", "nhs_conditions_dataset"))
TRANSLATED_FOLDER = "translated_nhs"
PROGRESS_FILE = "progress.json"

# Ensure output directory exists
os.makedirs(TRANSLATED_FOLDER, exist_ok=True)

# **Track completed files** to prevent duplicates
completed_files = set(os.listdir(TRANSLATED_FOLDER))

# **Load progress tracking file**
if os.path.exists(PROGRESS_FILE):
    with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
        try:
            completed_files.update(json.load(f))
        except json.JSONDecodeError:
            print("⚠️ Progress file is corrupted. Resetting progress tracking.")

# Stop signal handler
stop_processing = False  # Flag to stop safely

def handle_exit(sig, frame):
    """Handles Ctrl+C interruption and saves progress."""
    global stop_processing
    print("\n⚠️  Translation interrupted! Saving progress...")
    stop_processing = True  # Set flag to break loop

signal.signal(signal.SIGINT, handle_exit)
signal.signal(signal.SIGTERM, handle_exit)

def save_progress():
    """Saves completed files to a progress tracking file."""
    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump(list(completed_files), f, indent=2, ensure_ascii=False)
    print(f"💾 Progress saved: {len(completed_files)} files completed.")

def translate_text(full_text):
    """Translate entire JSON content using DeepSeek API (one call per file)."""
    global stop_processing
    
    if not full_text.strip():
        return full_text  # Skip empty texts
    
    if stop_processing:
        raise InterruptedError("Translation stopped by user.")  

    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "Translate the following medical text from English to Albanian."},
            {"role": "user", "content": full_text}
        ]
    }

    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }

    max_attempts = 5  # Increase max attempts
    for attempt in range(max_attempts):
        if stop_processing:
            raise InterruptedError("Translation stopped by user.")
            
        try:
            start_time = time.time()
            response = requests.post(DEEPSEEK_API_URL, json=payload, headers=headers, timeout=120)

            if response.status_code == 200:
                result = response.json()
                translated_text = result.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
                
                if not translated_text:
                    print(f"⚠️ Empty translation received, retrying...")
                    time.sleep(5)  # Longer wait before retry
                    continue
                    
                elapsed_time = time.time() - start_time
                print(f"✅ Translated in {elapsed_time:.2f}s: {translated_text[:50]}...")
                return translated_text
            else:
                print(f"❌ API Error {response.status_code}: {response.text}")
                wait_time = 5 * (2 ** attempt)  # 5, 10, 20, 40, 80 seconds
                print(f"⏳ Waiting {wait_time}s before retry {attempt+1}/{max_attempts}...")
                time.sleep(wait_time)
        except requests.RequestException as e:
            print(f"❌ Translation request failed (Attempt {attempt + 1}/{max_attempts}): {e}")
            wait_time = 5 * (2 ** attempt)
            print(f"⏳ Waiting {wait_time}s before retry {attempt+1}/{max_attempts}...")
            time.sleep(wait_time)
            
    raise RuntimeError(f"Failed to translate text after {max_attempts} attempts.")

def translate_conditions():
    """Main function to translate all conditions."""
    files_to_translate = [f for f in os.listdir(NHS_DATASET_FOLDER) if f.endswith(".json")]
    print(f"📌 Found {len(files_to_translate)} condition files to translate.")
    
    total_files = len(files_to_translate)
    completed_count = len(completed_files)
    
    print(f"🔄 Starting translation: {completed_count}/{total_files} files already completed")

    for filename in files_to_translate:
        if filename in completed_files:
            print(f"⏩ Skipping already translated: {filename}")
            continue
            
        if stop_processing:
            print(f"🛑 Process stopped. Progress saved: {completed_count}/{total_files} files translated.")
            break

        file_path = os.path.join(NHS_DATASET_FOLDER, filename)
        print(f"🔄 Translating: {filename.replace('_', ' ').replace('.json', '').title()}")

        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            
            # Translate the content
            try:
                full_text = json.dumps(data, ensure_ascii=False)
                translated_text = translate_text(full_text)

                try:
                    translated_article = json.loads(translated_text)
                except json.JSONDecodeError:
                    print(f"❌ Failed to parse translated JSON for: {filename}")
                    translated_article = data  # Keep original if parsing fails

                if stop_processing:
                    print(f"⚠️ Skipping save for {filename} due to interruption.")
                    continue

                translated_file_path = os.path.join(TRANSLATED_FOLDER, filename)
                with open(translated_file_path, "w", encoding="utf-8") as f:
                    json.dump(translated_article, f, indent=2, ensure_ascii=False)

                completed_files.add(filename)
                completed_count += 1
                print(f"✅ Translated and saved: {filename} ({completed_count}/{total_files})")

                save_progress()
                
                time.sleep(1)  # Small pause between files
                
            except InterruptedError:
                print(f"⚠️ Translation of {filename} was interrupted by user.")
                break
            except Exception as e:
                print(f"❌ Error translating {filename}: {str(e)}")
                print("⏳ Waiting 30 seconds before trying the next file...")
                time.sleep(30)  
                continue
                
        except Exception as e:
            print(f"❌ Error processing {filename}: {str(e)}")
            continue

    if not stop_processing:
        print(f"🎉 All {total_files} files have been translated successfully!")
    else:
        print(f"⏹️ Translation process stopped. Completed {completed_count}/{total_files} files.")

if __name__ == "__main__":
    translate_conditions()
