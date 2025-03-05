import json
import psycopg2
import os

# Load environment variables
DB_URL = os.getenv("DATABASE_URL")

# Connect to PostgreSQL
conn = psycopg2.connect(DB_URL)
cursor = conn.cursor()

def store_in_db():
    with open("backend/translated_articles.json", "r", encoding="utf-8") as f:
        articles = json.load(f)

    for article in articles:
        print(f"📝 Storing: {article['translated_title']}")

        cursor.execute(
            """
            INSERT INTO articles (title, translated_title, url, content, translated_content)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (article["title"], article["translated_title"], article["url"], article["content"], article["translated_content"])
        )

    conn.commit()
    print("✅ All articles stored in PostgreSQL!")

    cursor.close()
    conn.close()

if __name__ == "__main__":
    store_in_db()
