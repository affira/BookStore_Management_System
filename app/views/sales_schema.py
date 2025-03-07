from datetime import date as date_type
from pydantic import BaseModel
from typing import Optional

class SaleCreate(BaseModel):
    book_id: int
    customer_id: int
    date: date_type
    quantity: int

class Sale(BaseModel):
    id: int
    book_id: int
    customer_id: int
    date: date_type
    quantity: int

    class Config:
        orm_mode = True

# For returning detailed information with book and customer data
class SaleDetail(BaseModel):
    id: int
    book_id: int
    book_title: str
    book_price: float  
    customer_id: int
    customer_name: str
    date: date_type
    quantity: int
    total_amount: float  # This will be calculated (quantity * book price)

    class Config:
        orm_mode = True