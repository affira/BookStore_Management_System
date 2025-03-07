# book_controller.py
from fastapi import APIRouter, HTTPException
from app.models.book import get_all_books, get_book_by_id, add_book, update_book, delete_book
from app.views.book_schema import Book, BookCreate

router = APIRouter()

@router.post("/", response_model=Book)
async def create_book(book: BookCreate):  # Changed from Book to BookCreate
    # Add the book to the database
    added_book_id = add_book(book.title, book.author, book.price)
    # Get the newly added book by its ID
    new_book = get_book_by_id(added_book_id)
    if new_book is None:
        raise HTTPException(status_code=404, detail="Book not found after creation")
    # Return the book as a Pydantic model
    return Book(id=new_book['BookID'], title=new_book['Title'], author=new_book['Author'], price=new_book['Price'])

# Get all books
@router.get("/", response_model=list[Book])
async def read_books():
    books = get_all_books()
    # Convert the query result to a list of Pydantic models
    return [Book(id=book['BookID'], title=book['Title'], author=book['Author'], price=book['Price']) for book in books]

# Get a single book by ID
@router.get("/{book_id}", response_model=Book)
async def read_book(book_id: int):
    book = get_book_by_id(book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return Book(id=book['BookID'], title=book['Title'], author=book['Author'], price=book['Price'])

@router.put("/{book_id}", response_model=Book)
async def update_book_details(book_id: int, book_update: BookCreate):  # Renamed parameter for clarity
    updated = update_book(book_id, book_update.title, book_update.author, book_update.price)
    updated_book = get_book_by_id(book_id)  # Get the updated book
    if not updated_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return Book(id=updated_book['BookID'], title=updated_book['Title'], author=updated_book['Author'], price=updated_book['Price'])

@router.delete("/{book_id}")
async def delete_book_details(book_id: int):
    book = get_book_by_id(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    delete_book(book_id)
    return {"message": "Book deleted successfully!"}