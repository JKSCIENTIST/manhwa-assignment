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

# Fetch data from the anime table
cursor.execute("SELECT * FROM anime")
rows = cursor.fetchall()

# Display the fetched data
for row in rows:
    print(f'ID: {row.id}, Title: {row.title}, Genre: {row.genre}, Description: {row.description}, Image URL: {row.image_url}, IMDb URL: {row.imdb_url}')

# Close the connection
cursor.close()
conn.close()
