import os
import json
import psycopg2
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database connection parameters
DATABASE_URL = os.getenv("DATABASE_URL")

# Path to translated JSON files
ALBANIAN_OUTPUT_FOLDER = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "backend", "translated_nhs")


def connect_to_db():
    import urllib.parse as urlparse
    url = urlparse.urlparse(DATABASE_URL)
    try:
        return psycopg2.connect(
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
        )
    except psycopg2.Error as e:  # Ensure to catch the correct exception
        print(f"❌ Database connection error: {e}")
        sys.exit(1)


def create_tables(conn):
    """Create tables for storing conditions and sections."""
    with conn.cursor() as cur:
        # Drop tables first to ensure clean schema (optional but safe)
        cur.execute("DROP TABLE IF EXISTS condition_sections_albanian;")
        cur.execute("DROP TABLE IF EXISTS conditions_albanian;")

        # Recreate with proper constraints
        cur.execute("""
        CREATE TABLE conditions_albanian (
            id SERIAL PRIMARY KEY,
            condition_name VARCHAR(255) NOT NULL,
            condition_slug VARCHAR(255) UNIQUE NOT NULL,
            url VARCHAR(500),
            full_json TEXT, 
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)

        cur.execute("""
        CREATE TABLE condition_sections_albanian (
            id SERIAL PRIMARY KEY,
            condition_slug VARCHAR(255) NOT NULL,
            section_name VARCHAR(255) NOT NULL,
            section_content TEXT,
            section_order INT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (condition_slug) REFERENCES conditions_albanian(condition_slug) ON DELETE CASCADE,
            UNIQUE (condition_slug, section_name)
        );
        """)

        conn.commit()
        print("✅ Database tables dropped & recreated with constraints")


def save_condition_to_db(conn, condition_data, filename):
    """Save condition and its sections into the database."""
    condition_slug = filename.replace('.json', '')
    condition_name = condition_data.get('title', condition_slug.replace('-', ' ').title())
    url = condition_data.get('url', '')
    
    # Convert full JSON to string
    full_json_str = json.dumps(condition_data, ensure_ascii=False)

    with conn.cursor() as cur:
        # Insert condition data
        cur.execute("""
        INSERT INTO conditions_albanian 
            (condition_name, condition_slug, url, full_json)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (condition_slug) DO UPDATE SET
            condition_name = EXCLUDED.condition_name,
            url = EXCLUDED.url,
            full_json = EXCLUDED.full_json;

        """, (condition_name, condition_slug, url, full_json_str))

        # Insert sections
        for index, section in enumerate(condition_data.get("sections", [])):
            section_title = section.get("title", "")
            section_content = "\n".join(section.get("paragraphs", []))  # Merge paragraphs into one text

            cur.execute("""
            INSERT INTO condition_sections_albanian 
            (condition_slug, section_name, section_content, section_order)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (condition_slug, section_name) DO UPDATE SET
            section_content = EXCLUDED.section_content,
            section_order = EXCLUDED.section_order;
            """, (condition_slug, section_title, section_content, index))

        conn.commit()

    return True


def import_all_translations():
    """Import all translated Albanian conditions into the database."""
    if not os.path.exists(ALBANIAN_OUTPUT_FOLDER):
        print(f"❌ Translated folder not found: {ALBANIAN_OUTPUT_FOLDER}")
        return False

    files = [f for f in os.listdir(ALBANIAN_OUTPUT_FOLDER) if f.endswith('.json')]
    total_files = len(files)

    if total_files == 0:
        print("❌ No translation files found")
        return False

    print(f"🔄 Found {total_files} translation files to import")

    # Connect to database
    conn = connect_to_db()
    create_tables(conn)

    success_count = 0
    for i, filename in enumerate(files, 1):
        file_path = os.path.join(ALBANIAN_OUTPUT_FOLDER, filename)
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                condition_data = json.load(file)

            if save_condition_to_db(conn, condition_data, filename):
                success_count += 1
                print(f"✅ Imported {i}/{total_files}: {filename}")
            else:
                print(f"⚠️ Failed to import {filename}")

        except Exception as e:
            print(f"❌ Error processing {filename}: {str(e)}")

    conn.close()
    print(f"🎉 Import complete! Successfully imported {success_count}/{total_files} conditions")
    return True


if __name__ == "__main__":
    print("📊 Starting import of Albanian translations to MySQL database...")
    import_all_translations()
