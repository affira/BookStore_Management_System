import sqlite3
import os

# Function to get a connection to the database
def get_db_connection():
    
    # Get the project root directory
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    db_path = os.path.join(root_dir, 'db', 'bookstore.db')
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # To access columns by name (not just index)
    return conn
