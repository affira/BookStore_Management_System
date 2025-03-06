from fastapi import FastAPI
import sqlite3

app = FastAPI()

# Helper function to get a connection to the database
def get_db_connection():
    conn = sqlite3.connect("bookstore.db")
    conn.row_factory = sqlite3.Row  # To access columns by name (not just index)
    return conn

# Route to add a new book
@app.post("/books/")
async def add_book(title: str, author: str, price: float):
    conn = get_db_connection()
    cursor = conn.cursor()
    new_book = (title, author, price)
    cursor.execute("INSERT INTO Books (Title, Author, Price) VALUES (?, ?, ?)", new_book)
    conn.commit()
    conn.close()
    return {"message": "✅ New book added successfully!"}

# Route to get all books
@app.get("/books/")
async def get_books():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Books")
    books = cursor.fetchall()
    conn.close()
    return books

# Route to get a book by its ID
@app.get("/books/{book_id}")
async def get_book(book_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Books WHERE BookID = ?", (book_id,))
    book = cursor.fetchone()
    conn.close()
    if book:
        return {"ID": book[0], "Title": book[1], "Author": book[2], "Price": book[3]}
    return {"error": "Book not found"}

# Route to update a book by its ID
@app.put("/books/{book_id}")
async def update_book(book_id: int, title: str, author: str, price: float):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Update book details in the Books table
    cursor.execute("""
        UPDATE Books
        SET Title = ?, Author = ?, Price = ?
        WHERE BookID = ?
    """, (title, author, price, book_id))
    
    conn.commit()
    conn.close()
    
    # Check if the book was updated
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Books WHERE BookID = ?", (book_id,))
    book = cursor.fetchone()
    conn.close()
    
    if book:
        return {"message": "✅ Book updated successfully!", "book": {"ID": book[0], "Title": book[1], "Author": book[2], "Price": book[3]}}
    return {"error": "Book not found"}

# Route to delete a book by its ID
@app.delete("/books/{book_id}")
async def delete_book(book_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if the book exists before trying to delete
    print(f"Trying to delete book with ID: {book_id}")  # Debugging line
    cursor.execute("SELECT * FROM Books WHERE BookID = ?", (book_id,))
    book = cursor.fetchone()
    
    if book:
        print(f"Book found: {book}")  # Debugging line
        # Delete the book from the Books table
        cursor.execute("DELETE FROM Books WHERE BookID = ?", (book_id,))
        conn.commit()
        conn.close()
        return {"message": f"✅ Book with ID {book_id} deleted successfully!"}
    
    conn.close()
    return {"error": f"Book with ID {book_id} not found"}