from flask import Flask, jsonify
import mysql.connector
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS so frontend can fetch data

# MySQL connection function
def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", "admin1234"),
        database=os.getenv("DB_NAME", "NHS")
    )

@app.route("/")
def home():
    return "Backend is running successfully!"

@app.route("/api/conditions", methods=["GET"])
def get_conditions():
    """Fetch all conditions (translated) from MySQL"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT condition_name, condition_slug, url FROM conditions_albanian;")
    conditions = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(conditions)

@app.route("/api/conditions/<slug>", methods=["GET"])
def get_condition(slug):
    """Fetch a single translated condition with sections"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Get main condition info
    cursor.execute("SELECT * FROM conditions_albanian WHERE condition_slug = %s;", (slug,))
    condition = cursor.fetchone()

    # Get sections for this condition
    cursor.execute("SELECT section_name, section_content FROM condition_sections_albanian WHERE condition_slug = %s ORDER BY section_order;", (slug,))
    sections = cursor.fetchall()

    cursor.close()
    conn.close()

    if not condition:
        return jsonify({"error": "Condition not found"}), 404

    # Add sections into condition response
    condition["sections"] = sections
    return jsonify(condition)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
