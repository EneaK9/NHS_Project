import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask import Flask
from flask_cors import CORS
from routes.conditions import conditions_bp  # Import the blueprint for API routes

app = Flask(__name__)
CORS(app)

# Register your API blueprints
app.register_blueprint(conditions_bp, url_prefix="/api")

@app.route("/")
def home():
    return "Backend is running successfully on Render!"

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)
