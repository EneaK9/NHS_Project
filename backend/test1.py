import json
import os
import time
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
    global stop_processing
    print("\n⚠️  Translation interrupted! Saving progress...")
    stop_processing = True

signal.signal(signal.SIGINT, handle_exit)
signal.signal(signal.SIGTERM, handle_exit)

def save_progress():
    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump(list(completed_files), f, indent=2, ensure_ascii=False)
    print(f"💾 Progress saved: {len(completed_files)} files completed.")

def preserve_images(section):
    updated_paragraphs = []
    for para in section.get("paragraphs", []):
        if "<img" in para:
            updated_paragraphs.append(f"__IMG__{para}__IMG__")
        else:
            updated_paragraphs.append(para)
    section["paragraphs"] = updated_paragraphs
    return section

def restore_images(section):
    updated_paragraphs = []
    for para in section.get("paragraphs", []):
        if isinstance(para, str) and para.startswith("__IMG__") and para.endswith("__IMG__"):
            updated_paragraphs.append(para.replace("__IMG__", ""))
        else:
            updated_paragraphs.append(para)
    section["paragraphs"] = updated_paragraphs
    return section

def translate_text(full_text):
    global stop_processing

    if not full_text.strip():
        return full_text

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

    max_attempts = 5
    for attempt in range(max_attempts):
        if stop_processing:
            raise InterruptedError("Translation stopped by user.")

        try:
            start_time = time.time()
            response = requests.post(DEEPSEEK_API_URL, json=payload, headers=headers, timeout=60)

            if response.status_code == 200:
                result = response.json()
                translated_text = result.get("choices", [{}])[0].get("message", {}).get("content", "").strip()

                if not translated_text:
                    print("⚠️ Empty translation received, retrying...")
                    time.sleep(5)
                    continue

                elapsed_time = time.time() - start_time
                print(f"✅ Translated in {elapsed_time:.2f}s: {translated_text[:50]}...")
                return translated_text
            else:
                print(f"❌ API Error {response.status_code}: {response.text}")
                wait_time = 5 * (2 ** attempt)
                print(f"⏳ Waiting {wait_time}s before retry {attempt+1}/{max_attempts}...")
                time.sleep(wait_time)
        except requests.RequestException as e:
            print(f"❌ Translation request failed (Attempt {attempt + 1}/{max_attempts}): {e}")
            wait_time = 5 * (2 ** attempt)
            print(f"⏳ Waiting {wait_time}s before retry {attempt+1}/{max_attempts}...")
            time.sleep(wait_time)

    raise RuntimeError(f"Failed to translate text after {max_attempts} attempts.")

def translate_conditions():
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

            # --- Preserve <img> tags ---
            for section in data.get("sections", []):
                preserve_images(section)

            for sub in data.get("sublink_articles", []):
                for section in sub.get("sections", []):
                    preserve_images(section)

            # Translate the content in chunks if it's too long
            max_chunk_size = 2000  # Max token count per request, you can adjust as needed
            full_text = json.dumps(data, ensure_ascii=False)
            chunks = [full_text[i:i+max_chunk_size] for i in range(0, len(full_text), max_chunk_size)]

            translated_text = ""
            for chunk in chunks:
                chunk_translated = translate_text(chunk)
                translated_text += chunk_translated

            # Log the raw translated text to check its structure
            print(f"✅ Raw Translated Text: {translated_text[:200]}...")

            # Attempt to parse the translated JSON
            try:
                translated_article = json.loads(translated_text)
                print(f"✅ Successfully parsed translated JSON for: {filename}")
            except json.JSONDecodeError:
                print(f"❌ Failed to parse translated JSON for: {filename}")
                translated_article = data

            # --- Restore <img> tags ---
            for section in translated_article.get("sections", []):
                restore_images(section)

            for sub in translated_article.get("sublink_articles", []):
                for section in sub.get("sections", []):
                    restore_images(section)

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
            time.sleep(1)

        except InterruptedError:
            print(f"⚠️ Translation of {filename} was interrupted by user.")
            break
        except Exception as e:
            print(f"❌ Error processing {filename}: {str(e)}")
            print("⏳ Waiting 30 seconds before trying the next file...")
            time.sleep(30)
            continue

    if not stop_processing:
        print(f"🎉 All {total_files} files have been translated successfully!")
    else:
        print(f"⏹️ Translation process stopped. Completed {completed_count}/{total_files} files.")


if __name__ == "__main__":
    translate_conditions()
