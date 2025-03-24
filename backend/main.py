from flask import Flask, jsonify
import mysql.connector
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS so frontend can fetch data

# MySQL connection function
def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", "admin1234"),
            database=os.getenv("DB_NAME", "NHS")
        )
        return conn
    except mysql.connector.Error as e:
        print(f"❌ Database connection error: {e}")
        return None

@app.route("/")
def home():
    return "Backend is running successfully!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
