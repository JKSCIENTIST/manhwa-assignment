from flask import Flask, render_template, jsonify
import pyodbc
import os
from datetime import datetime
from dotenv import load_dotenv

app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

# Function to establish a connection to the Azure SQL Database
def get_db_connection():
    server = os.getenv('DB_SERVER')
    database = os.getenv('DB_NAME')
    username = os.getenv('DB_USERNAME')
    password = os.getenv('DB_PASSWORD')
    driver = os.getenv('DB_DRIVER')
    
    connection_string = f'DRIVER={driver};SERVER={server};PORT=1433;DATABASE={database};UID={username};PWD={password}'
    try:
        conn = pyodbc.connect(connection_string)
        return conn
    except pyodbc.Error as e:
        app.logger.error(f"Error connecting to database: {e}")
        return None

# Function to load Manhwa data from the database
def load_manhwa_data():
    conn = get_db_connection()
    if conn is None:
        return []
    
    cursor = conn.cursor()
    
    try:
        # Adjust the SQL query based on your table structure
        cursor.execute("SELECT id, title, genre, description, image_url, imdb_url FROM anime")
        rows = cursor.fetchall()
        
        # Convert fetched data into a list of dictionaries
        manhwas = []
        for row in rows:
            manhwa = {
                "id": row.id,
                "title": row.title,
                "genre": row.genre,
                "description": row.description,
                "image_url": row.image_url,
                "imdb_url": row.imdb_url
            }
            manhwas.append(manhwa)
        
        return manhwas
    except pyodbc.Error as e:
        app.logger.error(f"Error fetching data: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

@app.route('/')
def index():
    manhwas = load_manhwa_data()
    total_manhwas = len(manhwas)
    current_year = datetime.now().year
    return render_template('index.html', total=total_manhwas, manhwas=manhwas, current_year=current_year)

# API endpoint to get Manhwa data in JSON
@app.route('/api/manhwas')
def api_manhwas():
    manhwas = load_manhwa_data()
    return jsonify(manhwas)

# Remove the following lines if present, as Azure App Service uses a production server
if __name__ == '__main__':
    app.run()


