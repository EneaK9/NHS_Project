import os
import json
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)

# Enable CORS for all origins
CORS(app)

# Define the path to the translated dataset folder
dataset_folder = os.path.join(os.getcwd(), "translated_nhs1")

# Function to generate slug from title if slug is missing
def generate_slug(title):
    return title.replace(" ", "_").lower()

# Read and serve all translated JSON files from the folder
@app.route('/api/translated-conditions', methods=['GET'])
def get_translated_conditions():
    conditions = []
    try:
        for filename in os.listdir(dataset_folder):
            if filename.endswith('.json'):
                file_path = os.path.join(dataset_folder, filename)
                with open(file_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    # Generate the slug if missing
                    if 'condition_slug' not in data:
                        data['condition_slug'] = generate_slug(data['title'])
                    conditions.append(data)
    except Exception as e:
        return jsonify({'error': f'Failed to read dataset folder: {str(e)}'}), 500
    return jsonify(conditions)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
