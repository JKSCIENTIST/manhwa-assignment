import json
import pyodbc
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Database connection details from .env file
server = os.getenv('DB_SERVER')
database = os.getenv('DB_NAME')
username = os.getenv('DB_USERNAME')
password = os.getenv('DB_PASSWORD')
driver = os.getenv('DB_DRIVER')

# Establish connection to Azure SQL Database
connection_string = f'DRIVER={driver};SERVER={server};PORT=1433;DATABASE={database};UID={username};PWD={password}'
conn = pyodbc.connect(connection_string)
cursor = conn.cursor()

# Create the table (if not exists) for storing the data
cursor.execute('''
    IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='anime' AND xtype='U')
    CREATE TABLE anime (
        id INT PRIMARY KEY,
        title NVARCHAR(255),
        genre NVARCHAR(255),
        description NVARCHAR(MAX),
        image_url NVARCHAR(255),
        imdb_url NVARCHAR(255)
    )
''')

# Read the JSON file
with open('manhwa_data.json', 'r') as json_file:
    data = json.load(json_file)

# Insert the JSON data into the SQL table
for item in data:
    # Check if the record already exists
    cursor.execute('SELECT COUNT(*) FROM anime WHERE id = ?', item['id'])
    (exists,) = cursor.fetchone()

    if exists == 0:  # Insert only if the record does not exist
        cursor.execute('''
            INSERT INTO anime (id, title, genre, description, image_url, imdb_url) 
            VALUES (?, ?, ?, ?, ?, ?)
        ''', 
        item['id'], 
        item['title'], 
        item['genre'], 
        item['description'], 
        item['image_url'], 
        item['imdb_url'])
        print(f"Record with ID {item['id']} inserted successfully.")
    else:
        print(f"Record with ID {item['id']} already exists. Skipping insertion.")

# Commit the transaction
conn.commit()

# Close the connection
cursor.close()
conn.close()

print("Data successfully processed.")
