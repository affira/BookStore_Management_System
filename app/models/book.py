from app.connection import get_db_connection

# Function to fetch all books
def get_all_books():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Books")
    books = cursor.fetchall()
    conn.close()
    return books

# Function to fetch a single book by ID
def get_book_by_id(book_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Books WHERE BookID = ?", (book_id,))
    book = cursor.fetchone()
    conn.close()
    return book

# Function to add a new book
def add_book(title, author, price):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Books (Title, Author, Price) VALUES (?, ?, ?)", (title, author, price))
    conn.commit()
    new_book_id = cursor.lastrowid  # Get the last inserted ID
    conn.close()
    return new_book_id

# Function to update a book
def update_book(book_id, title, author, price):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE Books
        SET Title = ?, Author = ?, Price = ?
        WHERE BookID = ?
    """, (title, author, price, book_id))
    affected = cursor.rowcount  # Get number of rows affected
    conn.commit()
    conn.close()
    return affected > 0  # Return True if at least one row was updated

# Function to delete a book
def delete_book(book_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Books WHERE BookID = ?", (book_id,))
    affected = cursor.rowcount  # Get number of rows affected
    conn.commit()
    conn.close()
    return affected > 0  # Return True if at least one row was deleted