import sqlite3
import pandas as pd

# Load the data from the CSV file
data = pd.read_csv('data/updated_dataset_new.csv')

# Connect to the database (creates it if it doesn't exist)
conn = sqlite3.connect('fragranceFitter.db')

# Create a cursor
c = conn.cursor()

# Create the tables
c.execute('''
    CREATE TABLE IF NOT EXISTS perfumes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        brand TEXT,
        description TEXT,
        image_url TEXT
    )
''')

c.execute('''
    CREATE TABLE IF NOT EXISTS reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        perfume_id INTEGER NOT NULL,
        user_name TEXT NOT NULL,
        reviews TEXT NOT NULL,
        date_posted TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (perfume_id) REFERENCES perfumes(id)
    )
''')

# Function to insert a record
def insert_record(name, brand, description, image_url):
    c.execute('INSERT INTO perfumes (name, brand, description, image_url) VALUES (?, ?, ?, ?)', (name, brand, description, image_url))

# Insert data from the CSV file
for index, row in data.iterrows():
    name = row['Name']
    brand = row['Brand'] if pd.notna(row['Brand']) else None
    description = row['Description'] if pd.notna(row['Description']) else None
    image_url = row['Image URL'] if pd.notna(row['Image URL']) else None
    insert_record(name, brand, description, image_url)

# Commit the transaction and close the connection
conn.commit()
conn.close()

print("Data insertion complete.") 