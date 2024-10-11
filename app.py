from flask import Flask, render_template, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)

# Load Manhwa data from JSON file
def load_manhwa_data():
    data_file = os.path.join(app.root_path, 'data', 'manhwa_data.json')
    with open(data_file, 'r', encoding='utf-8') as f:
        return json.load(f)

@app.route('/')
def index():
    manhwas = load_manhwa_data()
    total_manhwas = len(manhwas)
    current_year = datetime.now().year
    return render_template('index.html', total=total_manhwas, manhwas=manhwas, current_year=current_year)

# Optional: API endpoint to get Manhwa data in JSON
@app.route('/api/manhwas')
def api_manhwas():
    manhwas = load_manhwa_data()
    return jsonify(manhwas)

if __name__ == '__main__':
    app.run()
