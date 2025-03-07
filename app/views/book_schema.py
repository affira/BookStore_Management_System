from pydantic import BaseModel

# Pydantic model for creating a new book
class BookCreate(BaseModel):
    title: str
    author: str
    price: float

# Pydantic model for the full book data (used in responses)
class Book(BaseModel):
    id: int
    title: str
    author: str
    price: float

    class Config:
        orm_mode = True 
