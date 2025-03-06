import sqlite3

# Function to get a connection to the database
def get_db_connection():
    conn = sqlite3.connect("bookstore.db")
    conn.row_factory = sqlite3.Row  # To access columns by name (not just index)
    return conn
